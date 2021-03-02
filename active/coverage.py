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
sns.set_palette(sns.color_palette(['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075']))



### get list of files
files = sorted(glob.glob('*_coverage.tsv'))
print(files)
print('')

### get sample numbers from file names
number = [i.rsplit('_S', 1)[1] for i in files]
number = [i.replace('_coverage.tsv', '') for i in number]
number = [int(i) for i in number]
# number = [1, 2, 3, 4, 5, 6, 7, 8]
print(number)
print('')

### sort file names by numbers
files = [x for _,x in sorted(zip(number, files))]
# files = files[:10]
print(files)

### set tag if desired
tag = ''

### get sample names from file names
names = [i.rsplit('_S', 1)[0] for i in files]
print(names)
print('')

### get conditions
conditions = [i[4:] for i in names]
print(conditions)
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



dfc.to_csv('coverage_summary'+tag+'.tsv', sep='\t')



fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(1, 1, 1)
plot = sns.relplot(x='X3', y='X4', kind='line', hue='condition', col='sample', col_wrap=6, units='sample', aspect=1.6, height=5, estimator=None, facet_kws={'sharey': False, 'sharex': True}, data=dfc)
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
plt.savefig('coverage'+tag+'.png', format='png', dpi=500, bbox_inches='tight')

# barplot('X4', variable)
# barplot('PF_MISMATCH_RATE', variable)
# barplot('PF_HQ_ERROR_RATE', variable)
# barplot('PF_INDEL_RATE', variable)
# barplot('PCT_CHIMERAS', variable)
# barplot('PCT_ADAPTER', variable)



print('finished')
