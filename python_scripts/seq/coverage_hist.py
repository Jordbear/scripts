import re
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 200)
import glob
from matplotlib import pyplot as plt
from matplotlib import ticker as ticker
import seaborn as sns
sns.set_style('white', {'axes.grid': True, 'xtick.bottom': True, 'ytick.left': True})
sns.set_context(rc={'patch.linewidth': '0.0'})
sns.set_palette(sns.color_palette(['#ce0e2d', '#005cb9', '#f5a800', '#45c2b1', '#035c67']))



files = sorted(glob.glob('*_coverage_hist.tsv'))


names = [i.replace('_coverage_hist.tsv', '') for i in files]
names = [i.replace('_dmarked_coverage_hist.tsv', '') for i in names]
print(names)
print('')

groups = [re.sub(r'_L.*_coverage.tsv', '', i) for i in files]
print(groups)
print('')



# colnames = ['metric1', 'TOTAL_READS', 'metric3', 'metric4', 'metric5', 'metric6', 'PCT_PF_READS_ALIGNED', 'metric8', 'metric9', 'metric10', 'metric11', 'metric12', 'PF_MISMATCH_RATE', 'PF_HQ_ERROR_RATE', 'PF_INDEL_RATE', 'metric16', 'metric17', 'metric18', 'metric19', 'metric20', 'metric21', 'metric22', 'PCT_CHIMERAS', 'PCT_ADAPTER', 'metric25', 'metric26', 'metric27']
# unwanted = []
# for i in colnames:
#     if 'metric' in i:
#         unwanted.append(i)
# print(unwanted)
# print('')

dfl = [pd.read_csv(f, sep='\t', header=None, prefix='X') for f in files]
for i in dfl:
    print(i.head())
    print('')

count = 0
for i in dfl:
    i['sample'] = names[count]
    i['group'] = groups[count]
    print(dfl[count].head())
    count+=1

dfc = pd.concat(dfl, axis=0)
print(dfc.head())
print('')

dfc = dfc[dfc.X0=='all']
print(len(dfc.index))
print(dfc.head())
print('')

# print(dfc['X2'].max()/200)
# print(dfc['X1'].mean())
# dfc = dfc[(dfc.X2>(dfc['X2'].max()/200)) | (dfc.X1<(dfc['X1'].mean()))]
# print(len(dfc.index))
# print(dfc.head())
# print('')

print(dfc['X2'].max())
print(dfc['X2'].max()/50)
dfq = dfc[(dfc.X2>(dfc['X2'].max()/50))]
print(len(dfq.index))
print(dfq.head())
print('')

xmax = dfq['X1'].max()
print(xmax)


variable = 'sample'


# fig = plt.figure(figsize=(11, 7))
# ax = fig.add_subplot(1, 1, 1)
# plot = sns.barplot(x='sample', y='TOTAL_READS', hue=variable, units='sample', dodge=False, data=dfc)

# for lb in plot.get_xticklabels():
#     lb.set_rotation(90)

# for p in plot.patches:
#     if np.isnan(p.get_height())==False:
#          plot.text(p.get_x()+p.get_width()/2, ax.get_ylim()[1]/5/len(names), '{:,.0f}'.format(p.get_height()), fontsize=250/len(names), rotation=90, ha='center', va='bottom')

# ax.ticklabel_format(style='plain', axis='y')

# def commas(x, pos):
#     return '{:,}'.format(int(x))
# ax.get_yaxis().set_major_formatter(plt.FuncFormatter(commas))

# plot.set_xlabel('')
# plot.legend(loc='center right', bbox_to_anchor=(1.11, 0.5), framealpha=1).remove()

# plt.savefig('TOTAL_READS-grouped_by_'+variable+'.png', format='png', dpi=500, bbox_inches='tight')


def barplot(y, variable):
    fig = plt.figure(figsize=(11, 7))
    ax = fig.add_subplot(1, 1, 1)
    plot = sns.catplot(x='X1', y=y, hue=variable, units='sample', dodge=False, col='sample', col_wrap=4, kind='bar', height=2, aspect=2, data=dfc)
   
    # for ax in plot.axes.flat:
    #     for lb in ax.get_xticklabels():
    #         lb.set_rotation(90)
    
    # for p in plot.patches:
    #     if np.isnan(p.get_height())==False:
    #         if p.get_height()>=1:
    #             value_format = '{:#.3g}'
    #         else:
    #             value_format = '{:.2f}'
    #         plot.text(p.get_x()+p.get_width()/2, p.get_height()+ax.get_ylim()[1]/200, value_format.format(p.get_height()), fontsize=250/len(names), ha='center')
    
    # ax.set_ylim(top=ax.get_ylim()[1]*(1+(0.8/len(names))))
    
    plot.set_axis_labels('Coverage Depth', 'Frequency')
    
    # plot.set_xlabel('Coverage Depth')
    # plot.set_ylabel('')
    
    # for ax in plot.axes.flat:
    #     ax.set_xlabel('')
    #     ax.set_ylabel('')
    
    for ax in plot.axes.flat:
        ax.set(xlim=(None, xmax))
        ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
        ax.xaxis.set_major_formatter(ticker.ScalarFormatter())


    # plot.set_xlabel('')
    # plot.legend(loc='center right', bbox_to_anchor=(1.11, 0.5), framealpha=1)#.remove()
    
    plt.subplots_adjust(wspace=0.1)
    
    plt.savefig(y+'_split.png', format='png', dpi=500, bbox_inches='tight')


barplot('X2', variable)
# barplot('PF_MISMATCH_RATE', variable)
# barplot('PF_HQ_ERROR_RATE', variable)
# barplot('PF_INDEL_RATE', variable)
# barplot('PCT_CHIMERAS', variable)
# barplot('PCT_ADAPTER', variable)



print('finished')
