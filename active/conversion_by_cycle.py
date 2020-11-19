import re
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 200)
import glob
from matplotlib import pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
sns.set_style('white', {'axes.grid': True, 'xtick.bottom': True, 'ytick.left': True})
sns.set_context(rc={'patch.linewidth': '0.0'})
sns.set_palette(sns.color_palette('deep'))



files = sorted(glob.glob('*_Mbias.txt'))
print(files)
print('')

names = [i.split('_S')[0] for i in files]
print(names)
print('')

# conditions = [re.search('-(.*)-', i)[1] for i in files]
# print(conditions)
# print('')

# libraries = [re.search('-(.)_', i)[1] for i in files]
# print(libraries)
# print('')



dfl = [pd.read_csv(f, sep='\t') for f in files]
# print(dfl)
# print('')

count = 0
for i in dfl:
    i['sample'] = names[count]
    print(len(dfl[count].index))
    print(dfl[count].head())
    # i['condition'] = conditions[count]
    # print(len(dfl[count].index))
    # print(dfl[count].head())
    # i['library'] = libraries[count]
    # print(len(dfl[count].index))
    # print(dfl[count].head())
    # dfl[count] = dfl[count][dfl[count]['CONTEXT'] == 'CpG']
    # print(len(dfl[count].index))
    # print(dfl[count].head())
    # dfl[count] = dfl[count][dfl[count]['TOTAL_DEPTH'] > 3]
    # print(len(dfl[count].index))
    # print(dfl[count].head())
    # dfl[count]['pct_mod_rate'] = dfl[count]['MOD'].sum()/(dfl[count]['MOD'].sum()+dfl[count]['UNMOD'].sum())*100
    # print(len(dfl[count].index))
    # print(dfl[count].head())
    # dfl[count]['pct_mod_rate2'] = dfl[count]['MOD']/(dfl[count]['MOD']+dfl[count]['UNMOD'])*100
    # print(len(dfl[count].index))
    # print(dfl[count].head())
    count+=1


dfc = pd.concat(dfl, axis=0)
print(len(dfc.index))
print(dfc.head())
print('')



dfc.drop(dfc.columns.difference(['#POSITION_(bp)', 'MOD_LVL_CpG_READ_1', 'MOD_LVL_CpG_READ_2', 'sample']), 1, inplace=True)
print(len(dfc.index))
print(dfc.head())
print('')

dfc = pd.melt(dfc, id_vars=['#POSITION_(bp)', 'sample'], value_vars=['MOD_LVL_CpG_READ_1', 'MOD_LVL_CpG_READ_2'])
print(len(dfc.index))
print(dfc.head())
print('')

dfc.to_csv('conversion_summary.tsv', sep='\t')

# dfc = dfc.sort_values(['condition', 'library', 'sample'])

# dfc = dfc[dfc['sample'].isin(['S01-06K01P', 'S04-06C01P', 'S14-PyB-L1', 'S19-BSTL1'])]




fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(1, 1, 1)
plot = sns.relplot(x='#POSITION_(bp)', y='value', hue='variable', kind='line', linewidth=2, col='sample', col_wrap=4, units='sample', aspect=1.6, height=5, estimator=None, data=dfc)
for ax in plot.axes.flat:
    ax.set_xlabel('Cycle', size=20)
    ax.set_ylabel('Conversion rate (%)' , size=20)
    for i, spine in ax.spines.items():
        spine.set_visible(True)
plot.set_titles("{col_name}", pad=2, size=20)
plot.set(xlim=(0, dfl[0]['#POSITION_(bp)'].max()))
plot.set(ylim=(70, 101))
# ax.legend(loc='center right', bbox_to_anchor=(1.2, 0.5), framealpha=1).remove()
def commas(x, pos):
    return '{:,}'.format(int(x))
ax.get_xaxis().set_major_formatter(plt.FuncFormatter(commas))
plt.subplots_adjust(wspace=0.1, hspace=0.12)
# plt.setp(plot._legend.get_texts(), fontsize=30)


plt.savefig('cycles.png', format='png', dpi=500, bbox_inches='tight')

print('finished')
