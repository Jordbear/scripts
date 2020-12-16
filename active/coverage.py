import re
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 200)
import glob
from matplotlib import pyplot as plt
import seaborn as sns
sns.set_style('white', {'axes.grid': True, 'xtick.bottom': True, 'ytick.left': True})
sns.set_context(rc={'patch.linewidth': '0.0'})
sns.set_palette(sns.color_palette('deep'))



files = sorted(glob.glob('*_coverage.tsv'))


names = [i.split('_S')[0] for i in files]
print(names)
print('')

names = [i.rsplit('_S', 1)[0] for i in files]
print(names)
print('')

conditions = [i[7:-2] for i in names]
print(conditions)
print('')

number = [i.split('_S')[1] for i in files]
number = [i.replace('_001_mCtoT_all.mods', '') for i in number]
number = ['0'+i for i in number]
number = [i[-2:] for i in number]
print(number)
print('')



# colnames = ['metric1', 'TOTAL_READS', 'metric3', 'metric4', 'metric5', 'metric6', 'PCT_PF_READS_ALIGNED', 'metric8', 'metric9', 'metric10', 'metric11', 'metric12', 'PF_MISMATCH_RATE', 'PF_HQ_ERROR_RATE', 'PF_INDEL_RATE', 'metric16', 'metric17', 'metric18', 'metric19', 'metric20', 'metric21', 'metric22', 'PCT_CHIMERAS', 'PCT_ADAPTER', 'metric25', 'metric26', 'metric27']
# unwanted = []
# for i in colnames:
#     if 'metric' in i:
#         unwanted.append(i)
# print(unwanted)
# print('')

dfl = [pd.read_csv(f, sep='\t', header=None, prefix='X') for f in files]
# for i in dfl:
#     print(i.head())
#     print('')

count = 0
for i in dfl:
    i['sample'] = names[count]
    i['condition'] = conditions[count]
    # i['library'] = libraries[count]
    print(len(dfl[count].index))
    print(dfl[count].head())
    count+=1

dfc = pd.concat(dfl, axis=0)
print(dfc.head())
print('')

print(dfl[0]['X3'].max())

# dfc = dfc[dfc.X0=='all']
# print(dfc)
# print('')

# print(dfc['X2'].max()/200)
# print(dfc['X1'].mean())
# dfc = dfc[(dfc.X2>(dfc['X2'].max()/200)) | (dfc.X1<(dfc['X1'].mean()))]
# print(len(dfc.index))
# print(dfc.head())
# print('')


dfc.to_csv('coverage_summary.tsv', sep='\t')

# dfc = dfc.sort_values(['condition', 'library', 'sample'])



# count=0
# for df in dfl:
#     fig = plt.figure(figsize=(7, 5))
#     ax = fig.add_subplot(1, 1, 1)
#     plot = sns.lineplot(x='X3', y='X4', hue='sample', units='sample', estimator=None, data=df)
#     # sns.despine()
#     ax.set_xlabel('Position')
#     ax.set_ylabel('Coverage Depth')
#     plot.set(xlim=(0, dfl[0]['X3'].max()))
#     plot.set(ylim=(0, None))
#     plot.legend(loc='center right', bbox_to_anchor=(1.2, 0.5), framealpha=1).remove()
#     def commas(x, pos):
#         return '{:,}'.format(int(x))
#     ax.get_xaxis().set_major_formatter(plt.FuncFormatter(commas))
#     plt.savefig('plot-'+names[count]+'.png', format='png', dpi=500, bbox_inches='tight')
#     count+=1


fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(1, 1, 1)
plot = sns.relplot(x='X3', y='X4', kind='line', hue='condition', col='sample', col_wrap=6, units='sample', aspect=1.6, height=5, estimator=None, data=dfc)
for ax in plot.axes.flat:
    ax.set_xlabel('Position', size=20)
    ax.set_ylabel('Coverage Depth' , size=20)
    for i, spine in ax.spines.items():
        spine.set_visible(True)
plot.set_titles("{col_name}", pad=2, size=20)
plot.set(xlim=(0, dfl[0]['X3'].max()))
plot.set(ylim=(0, None))
# ax.legend(loc='center right', bbox_to_anchor=(1.2, 0.5), framealpha=1).remove()
def commas(x, pos):
    return '{:,}'.format(int(x))
ax.get_xaxis().set_major_formatter(plt.FuncFormatter(commas))
plt.subplots_adjust(wspace=0.1, hspace=0.12)
# plt.setp(plot._legend.get_texts(), fontsize=30)
plt.savefig('coverage.png', format='png', dpi=500, bbox_inches='tight')

# barplot('X4', variable)
# barplot('PF_MISMATCH_RATE', variable)
# barplot('PF_HQ_ERROR_RATE', variable)
# barplot('PF_INDEL_RATE', variable)
# barplot('PCT_CHIMERAS', variable)
# barplot('PCT_ADAPTER', variable)



print('finished')
