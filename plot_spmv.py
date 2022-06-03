import numpy as np
from numpy import ma
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import scale as mscale
from matplotlib import transforms as mtransforms
from matplotlib.ticker import FixedLocator
import matplotlib.ticker
import sys

class SegmentedScale(mscale.ScaleBase):
    name = 'segmented'

    def __init__(self, axis, **kwargs):
        mscale.ScaleBase.__init__(self,axis)
        self.points = kwargs.get('points',[0,1])
        self.lb = self.points[0]
        self.ub = self.points[-1]

    def get_transform(self):
        return self.SegTrans(self.lb, self.ub, self.points)

    def set_default_locators_and_formatters(self, axis):
        axis.set_major_locator(FixedLocator(self.points))

    def limit_range_for_scale(self, vmin, vmax, minpos):
        return max(vmin, self.lb), min(vmax, self.ub)

    class SegTrans(mtransforms.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def __init__(self, lb, ub, points):
            mtransforms.Transform.__init__(self)
            self.lb = lb
            self.ub = ub
            self.points = points

        def transform_non_affine(self, a):
            masked = a # ma.masked_where((a < self.lb) | (a > self.ub), a)
            return np.interp(masked, self.points, np.arange(len(self.points)))

        def inverted(self):
            return SegmentedScale.InvertedSegTrans(self.lb, self.ub, self.points)

    class InvertedSegTrans(SegTrans):

        def transform_non_affine(self, a):
            return np.interp(a, np.arange(len(self.points)), self.points)
        def inverted(self):
            return SegmentedScale.SegTrans(self.lb, self.ub, self.points)

# Now that the Scale class has been defined, it must be registered so
# that ``matplotlib`` can find it.
mscale.register_scale(SegmentedScale)

if __name__ == '__main__':
    font = {'family' : 'serif',
        'size'   : 29}
    matplotlib.rc('font', **font)

    df = pd.read_csv(sys.argv[1])
    # df_ell = pd.read_csv(sys.argv[2])
    # df_piece = pd.read_csv(sys.argv[3])
    # df_piecewise = pd.read_csv(sys.argv[3])
    names = df["Matrix"].unique()
    ellpack_names = df_ell["Matrix"].unique()
    piece_names = df_piece["matrix_name"].unique()
    csr5_speedup = []
    mkl_speedup = []
    ellpack_speedup = []
    piecewise_speedup = []
    nnz_list = []
    ellpack_nnz_list = []
    piecewise_nnz_list = []
    for name in names:
        df_test = df[df["Matrix"] == name]
        mkl_speedup.append ((df_test[[" SpMV MKL Parallel Executor", " SpMV Parallel Base"]].min(axis=1) / df_test[[" SpMV Vec 1_4 Parallel", "SpMV DDT Parallel Executor"]].min(axis=1)).max())
        csr5_speedup.append ((df_test[["SpMVCSR5 Parallel Executor"]].min(axis=1) / df_test[[" SpMV Vec 1_4 Parallel", "SpMV DDT Parallel Executor"]].min(axis=1)).max())
        nnz_list.append(df_test["NNZ"].unique()[0])
        #df.loc[df["Matrix"] == name,'MKL Speedup'] = (df_test[[" SpMV MKL Parallel Executor"," SpMV Parallel Base"]].min(axis=1) / df_test[[" SpMV Vec 1_4 Parallel","SpMV DDT Parallel Executor"]].min(axis=1)).max()
        #df.loc[df["Matrix"] == name,'CSR5 Speedup'] = (df_test[["SpMVCSR5 Parallel Executor"]].min(axis=1) / df_test[[" SpMV Vec 1_4 Parallel","SpMV DDT Parallel Executor"]].min(axis=1)).max()
    for index,name in enumerate(ellpack_names):
        df_test = df_ell[df_ell["Matrix"] == name]
        ellpack_speedup.append ((df_test[["ELLPACK"]].min(axis=1) / df_test[[" SpMV Vec 1_4 Parallel", "DDT MT"]].min(axis=1)).max())
        df_test_original = df[df["Matrix"] == name]
        ellpack_nnz_list.append(index)
        # ellpack_nnz_list.append(df_test_original["NNZ"])
    for index, name in enumerate(piece_names):
        df_test_piece = df_piece[df_piece["matrix_name"] == name]
        changed_name = '/' + name + '/' + name + '.mtx'
        df_test = df[df["Matrix"] == changed_name]
        piecewise_speedup.append(df_test_piece["EXECUTION_TIME"] / df_test["SpMVDDT Serial Executor"].min())
        piecewise_nnz_list.append(index)

    print(len(piecewise_speedup))
    print(len(piecewise_nnz_list))
    # print(piecewise_speedup)
    # print(piecewise_nnz_list)

    fig, (ax,ax1,ax2,ax3) = plt.subplots(4,1)
    fig.set_size_inches(15.5, 30.5)

    slower_csr = np.sum(np.where(np.array(csr5_speedup) < 1, 1, 0))
    slower_mkl = np.sum(np.where(np.array(mkl_speedup) < 1, 1, 0))
    print("CSR5 faster: ", slower_csr/len(csr5_speedup), "MKL faster: ", slower_mkl/len(mkl_speedup) )
    print("CSR5 avg speedup: ", np.average(np.where(np.array(csr5_speedup)<7, csr5_speedup, 7)) )
    print("MKL avg speedup: ", np.average(np.where(np.array(mkl_speedup)<7, mkl_speedup, 7)) )
    df = df[( df[" size_cutoff"] == 1 ) & ( df[" col_threshold"] == 1 )]
    ax.scatter(nnz_list, mkl_speedup, color="black")
    ax.set_xscale('log')
    ax.set_ylim([0, 7])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)


    #ax.set_yscale('segmented', points=np.array([0.9,1,1.25,1.5,2,10,20]))
    # ax.yaxis.set_major_locator(matplotlib.ticker.LinearLocator(3))
    # ax.set_yticks([1,2,16])
    #ax.set_xlabel("NNZ")
    ax.set_ylabel("LCM I/E Speedup over MKL")
    trans = mtransforms.ScaledTranslation(-20/72, 7/72, fig.dpi_scale_trans)
    # ax.text(0.0, 1.0, "a)", transform=ax.transAxes + trans,
    #         fontsize='medium', va='bottom',fontweight="bold")

    ax.axhline(y=1.0,color='r',linestyle='-')
    #ax1.scatter(df["NNZ"],df["CSR5 Speedup"],color="black")
    ax1.scatter(nnz_list, csr5_speedup, color="black")
    ax1.set_ylim([0, 5.5])
    ax1.set_xscale('log')
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    #ax1.set_yscale('segmented', points=np.array([0.2,0.5,1,1.25,1.5,2,4,5]))
    # ax.yaxis.set_major_locator(matplotlib.ticker.LinearLocator(3))
    # ax.set_yticks([1,2,16])
    #ax1.set_xlabel("NNZ")
    ax1.set_ylabel("LCM I/E Speedup over CSR5")
    # ax1.text(0.0, 1.0, "b)", transform=ax1.transAxes + trans,
    #         fontsize='medium', va='bottom',fontweight="bold")
    ax1.axhline(y=1.0, color='r', linestyle='-')

    # Ellpack Speedup
    ax2.scatter(ellpack_nnz_list, ellpack_speedup, color="black")
    ax2.set_ylim([0, 9.5])
    ax2.set_xscale('log')
    ax2.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    #ax2.set_xlabel("NNZ")
    ax2.set_ylabel("LCM I/E Speedup over SPF-ELL")
    ax2.axhline(y=1.0,color='r',linestyle='-')
    print("SPF avg speedup: ", np.average(np.where(np.array(ellpack_speedup) < 10, ellpack_speedup, 7)))

    # Piecewise Speedup
    ax3.scatter(piecewise_nnz_list, piecewise_speedup, color="black")
    ax3.set_ylim([0, 10])
    ax3.set_xscale('log')
    ax3.spines['right'].set_visible(False)
    ax3.spines['top'].set_visible(False)
    ax3.set_xlabel("NNZ")
    ax3.set_ylabel("LCM I/E Speedup over RPW")
    ax3.set_yscale('log')
    ax3.axhline(y=1.0,color='r',linestyle='-')
    print("RPW avg speedup: ", np.average(np.where(np.array(piecewise_speedup) < 100, piecewise_speedup, 7)))

    for axis in ['bottom', 'left']:
        ax.spines[axis].set_linewidth(4)
        ax1.spines[axis].set_linewidth(4)
        ax2.spines[axis].set_linewidth(4)
        ax3.spines[axis].set_linewidth(4)

    plt.savefig("SC22_SpMV_scatter.pdf", bbox_inches = 'tight')
    plt.show()
