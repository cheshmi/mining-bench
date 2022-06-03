
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
from matplotlib import rcParams
from matplotlib import rc

import matplotlib.font_manager

flist = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')[:]

rcParams['font.family'] = 'serif'
rcParams['font.serif'] = 'Linux Libertine O'


import matplotlib.gridspec as gridspec
import matplotlib
import sys

matplotlib.style.use('ggplot')

np.random.seed(0)

df = pd.read_csv(sys.argv[1])
dfFinal = pd.DataFrame(columns=["Matrix","Framework","Bar_part","Count"])

rcParams['xtick.major.pad']='20'

counter = 0
matrixCounter = 1
for index, row in df.iterrows():
    dfFinal.loc[counter+0] = [matrixCounter, "LCM", "LCM-BLAS", row['DDF+BLAS']+row['DDF']]
    dfFinal.loc[counter+1] = [matrixCounter, "LCM", "LCM-BLAS+PSC", row['DDF+BLAS+PSC']]
    dfFinal.loc[counter+2] = [matrixCounter, "MKL", "MKL", row['MKL']]
    dfFinal.loc[counter+3] = [matrixCounter, "SPF-ELL", "SPF-ELL", row['ELLPACK']]
    dfFinal.loc[counter+4] = [matrixCounter, "Regular Piece-Wise", "Regular Piece-Wise", row['PIC']]
    counter = counter + 5
    matrixCounter += 1

# df = pd.DataFrame(np.asarray(1+5*np.random.random((10,4)), dtype=int),columns=["Matrix", "Framework", "Bar_part", "Count"])
# df = df.assign(Matrix=['bccstk10', 'bccstk10', 'apache2','apache2', 'apache2', 'bccstk10','apache2', 'sdf', 'sdf','sdf'])
# df = df.assign(Framework=['Framework', 'Framework', 'Framework','Sympiler', 'Framework', 'MKL','Sympiler', 'Framework', 'MKL','MKL'])
# df = df.assign(Bar_part=['Baseline', 'FS-Codelet', 'PS-Codelet','Sympiler', 'Framework', 'MKL','Sympiler', 'Framework', 'MKL','MKL'])

df = dfFinal
df = df.groupby(["Matrix", "Framework", "Bar_part"])["Count"].sum().unstack(fill_value=0)

# plotting

clusters = df.index.levels[0]
inter_graph = 0
maxi = np.max(np.sum(df, axis=1))
total_width = len(df)+inter_graph*(len(clusters)-1)

fig = plt.figure(figsize=(total_width,10),linewidth=0)
fig.set_size_inches(25.5, 10.5)
gridspec.GridSpec(1, total_width)
axes=[]

# Text sizes
SMALL_SIZE  = 14
MEDIUM_SIZE = 18
BIGGER_SIZE = 18

#rcParams['font.serif'] = 'Linux Libertine O'

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
plt.rc('axes', linewidth=2)

cmap = matplotlib.colors.LinearSegmentedColormap.from_list("",
        ['#0747FF','#07ECFF','#069306','#6300E1','#FFA200']
        )

ax_position = 0
for cluster in clusters:
    subset = df.loc[cluster]
    ax = subset.plot(kind="bar",
           colormap=cmap,
            stacked=True, width=0.8, ax=plt.subplot2grid((1,total_width), (0,ax_position), colspan=len(subset.index)))
    axes.append(ax)
    ax.set_title(cluster, y=-0.03,fontsize=14, color="black")
    ax.tick_params(axis='x', which='major', pad=15)
    ax.set_xlabel("")
    ax.set_xticks([])
    ax.set_xticklabels([])
    ax.minorticks_off()
    ax.set_facecolor('white')
    ax.set_ylim(0,maxi+1)
    ax.yaxis.grid()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    for axis in ['bottom', 'left']:
        ax.spines[axis].set_linewidth(4)

    # ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax_position += len(subset.index)+inter_graph
    ax.get_yaxis().set_visible(False)

for i in range(1,len(clusters)):
    axes[i].set_yticklabels("")
    axes[i-1].legend().set_visible(False)
axes[0].set_ylabel("GFlop/s", color="black", fontsize=14)
axes[0].tick_params(axis='y', colors='black')
axes[0].yaxis.grid(False)
axes[0].grid(False)
axes[0].get_yaxis().set_visible(True)

axes[0].spines['right'].set_visible(False)
axes[0].spines['top'].set_visible(False)
for axis in ['bottom', 'left']:
    axes[0].spines[axis].set_linewidth(4)

# fig.suptitle('Big Title', fontsize="x-large")
legend = axes[-1].legend(
       # loc=(-0.5, 0.8),
        loc='upper right',
        fontsize=12, framealpha=1).get_frame()
legend.set_linewidth(3)
legend.set_edgecolor("black")
legend.set_facecolor("white")
#legend.set_color("white")

# Add axes
# plt.plot([-10, 0], [-10, 10], 'k-', lw=2)

# plt.axis('off')

#plt.show()
fig.savefig("spmv_stacked_speedups_SC22.pdf", bbox_inches='tight')