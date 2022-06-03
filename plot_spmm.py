import numpy as np
from numpy import ma
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import scale as mscale
from matplotlib import transforms as mtransforms
from matplotlib.ticker import FixedLocator
import matplotlib.ticker

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
        'size'   : 31}
    matplotlib.rc('font', **font)
    # df = pd.read_csv(".logs/spmm_niagara_final.csv")
    df = pd.read_csv(sys.argv[1])
    names = df.Matrix.unique()
    #bCols = [4,16,64,256,1024]
    bCols = [256]
    for name in names:
        for bCol in bCols:
            df_test = df[( df["Matrix"] == name ) & (df["bCols"] == bCol)]
            df.loc[( df["Matrix"] == name ) & (df["bCols"] == bCol),"speedup"] = (df_test[["SpMM Parallel","SpMM MKL"]].min(axis=1) / df_test[["SpMM Tiled Parallel"]].min(axis=1)).max()
            flops = (df_test["bCols"].values * df_test["NNZ"].values).max()
            df.loc[(df["Matrix"] == name) & (df["bCols"] == bCol), "DDT GFLOPs"] = 1e-9 * flops / (df_test[["SpMM Tiled Parallel", "SpMM DDT"]].min(axis=1)).min()
            df.loc[(df["Matrix"] == name) & (df["bCols"] == bCol), "MKL GFLOPs"] = 1e-9 * flops / (df_test[["SpMM Parallel","SpMM MKL"]].min(axis=1)).min()
    fig, (ax) = plt.subplots()
    fig.set_size_inches(25.5, 10.5)
    avg_speedups = [1.65]
    for col in [64,256,1024]:
        avg_speedups.append(df[( df["mTileSize"] == 32) & (df["bCols"] == col)].speedup.mean())


    df_scatter_256 = df[( df["mTileSize"] == 32) & (df["bCols"] == 256)]
    slower_mkl = np.sum(np.where(np.array(df_scatter_256.speedup) < 1, 1, 0))
    print( "MKL faster: ", slower_mkl/len(df_scatter_256.speedup), " From total: ", len(df_scatter_256.speedup), " slower only: ", slower_mkl)
    print("Max:", df_scatter_256.speedup.max())
    print("Avg:", np.average(df_scatter_256.speedup))
    ax.scatter(df_scatter_256["NNZ"],df_scatter_256["speedup"],color="black")
    ax.set_xscale('log')
#    ax.set_yscale('segmented', points=np.array([0,1,1.5,2,4,10,20]))
    # ax.yaxis.set_major_locator(matplotlib.ticker.LinearLocator(3))
    # ax.set_yticks([1,2,16])
    ax.axhline(y=1.0, color='r', linestyle='-')
    ax.set_xlabel("NNZ", fontsize=40)
    ax.set_ylabel("LCM I/E Speedup over MKL", fontsize=40)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_ylim([0, 7])
    for axis in ['bottom', 'left']:
        ax.spines[axis].set_linewidth(4)

    # trans = mtransforms.ScaledTranslation(-20/72, 7/72, fig.dpi_scale_trans)
    # ax.text(0.0, 1.0, "a)", transform=ax.transAxes + trans,
    #         fontsize='medium', va='bottom',fontweight="bold")

    # ax1.plot([1,64,256,1024],avg_speedups,'--bo',color="black")
    # ax1.set_xscale('log')
    # #ax1.set_yscale('segmented', points=np.array([0,0.25,0.5,0.75,1,1.25,1.5,1.75,2,4]))
    # ax1.set_xlabel("Dense Matrix Column Width")
    # ax1.set_ylabel("Average Speedup")
    # ax1.text(0.0, 1.0, "b)", transform=ax1.transAxes + trans,
    #         fontsize='medium', va='bottom',fontweight="bold")

    #plt.show()
    plt.savefig("SC22_SpMM_scatter.pdf", bbox_inches='tight')

    fig1, ax1 = plt.subplots()
    fig1.set_size_inches(18.5, 10.5)
    ax1.scatter(df_scatter_256["NNZ"],df_scatter_256["DDT GFLOPs"],color="black")
    ax1.scatter(df_scatter_256["NNZ"], df_scatter_256["MKL GFLOPs"], color="red")
    #ax1.set_xscale('log')
    ax1.set_xlabel("NNZ")
    ax1.set_ylabel("GFLOP/s")


    #plt.show()
