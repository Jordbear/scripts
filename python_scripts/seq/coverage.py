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
sns.set_palette(sns.color_palette(['#ce0e2d', '#005cb9', '#f5a800', '#45c2b1', '#035c67']))



files = sorted(glob.glob('*_coverage.tsv'))


names = [i.replace('_coverage.tsv', '') for i in files]
names = [i.replace('_dmarked_coverage.tsv', '') for i in names]
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
# for i in dfl:
#     print(i.head())
#     print('')

count = 0
for i in dfl:
    i['sample'] = names[count]
    i['group'] = groups[count]
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

count=0
for df in dfl:
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(1, 1, 1)
    plot = sns.lineplot(x='X3', y='X4', hue='sample', units='sample', estimator=None, data=df)
    # sns.despine()
    ax.set_xlabel('Position')
    ax.set_ylabel('Coverage Depth')
    plot.set(xlim=(0, dfl[0]['X3'].max()))
    plot.set(ylim=(0, None))
    plot.legend(loc='center right', bbox_to_anchor=(1.2, 0.5), framealpha=1).remove()
    def commas(x, pos):
        return '{:,}'.format(int(x))
    ax.get_xaxis().set_major_formatter(plt.FuncFormatter(commas))
    plt.savefig('plot-'+names[count]+'.png', format='png', dpi=500, bbox_inches='tight')
    count+=1


# barplot('X4', variable)
# barplot('PF_MISMATCH_RATE', variable)
# barplot('PF_HQ_ERROR_RATE', variable)
# barplot('PF_INDEL_RATE', variable)
# barplot('PCT_CHIMERAS', variable)
# barplot('PCT_ADAPTER', variable)



print('finished')
