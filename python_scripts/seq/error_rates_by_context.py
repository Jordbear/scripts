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



files = sorted(glob.glob('*.pre_adapter_detail_metrics'))
print(files)
print('')

names = [i.split('_S')[0] for i in files]
print(names)
print('')

contigs = [re.search('artifacts-(.*).tsv', i)[1] for i in files]
print(contigs)
print('')



dfl = [pd.read_csv(f, sep='\t', skiprows=6) for f in files]
# print(dfl)
# print('')

count = 0
for i in dfl:
    i['sample'] = names[count]
    # print(dfl[count])
    i['contig'] = contigs[count]
    # print(dfl[count])
    print(dfl[count])
    count+=1


dfc = pd.concat(dfl, axis=0)
print(len(dfc.index))
print(dfc.head())
print('')

dfc = dfc[dfc['REF_BASE'] == 'C']
print(len(dfc.index))
print(dfc.head())
print('')

dfc = dfc[dfc['ALT_BASE'] == 'T']
print(len(dfc.index))
print(dfc.head())
print('')

dfc['context'] = dfc.CONTEXT.str[1:]
print(len(dfc.index))
print(dfc.head())
print('')

dfc = dfc.drop(columns=['SAMPLE_ALIAS', 'LIBRARY', 'REF_BASE', 'ALT_BASE', 'CONTEXT', 'ERROR_RATE', 'QSCORE'])
print(len(dfc.index))
print(dfc.head())
print('')

dfc = dfc.groupby(['sample', 'contig', 'context']).sum().reset_index()
print(len(dfc.index))
print(dfc.head())
print('')

dfc['pct_error_rate'] = (dfc['PRO_ALT_BASES'] - dfc['CON_ALT_BASES']) / (dfc['PRO_REF_BASES'] + dfc['PRO_ALT_BASES'] + dfc['CON_REF_BASES'] + dfc['CON_ALT_BASES']) * 100
print(len(dfc.index))
print(dfc.head())
print('')

dfc['pct_error_rate'] = dfc['pct_error_rate'].mask(dfc['pct_error_rate'] < 0, 0)
print(len(dfc.index))
print(dfc.head())
print('')

# dfc_mm10 = dfc[dfc['sample'].str.contains('mm10')]
# print(len(dfc_mm10.index))
# print(dfc.head())
# print('')

# dfc_unmodified_2kb = dfc[dfc['sample'].str.contains('unmodified_2kb')]
# print(len(dfc_unmodified_2kb.index))
# print(dfc.head())
# print('')


dfc.to_csv('conversion_summary-context.tsv', sep='\t')



fig = plt.figure(figsize=(11, 5))
ax = fig.add_subplot(1, 1, 1)
plot = sns.catplot(x='sample', y='pct_error_rate', hue='context', col='contig', units='sample', dodge=True, height=6, aspect=1.2, kind='bar', data=dfc)
plt.subplots_adjust(wspace=0.1)
for ax in plot.axes.flat:
        for lb in ax.get_xticklabels():
            lb.set_rotation(90)
# for p in plot.patches:
#     if np.isnan(p.get_height())==False:
#         if p.get_height()>=1:
#             value_format = '{:#.3g}'
#         else:
#             value_format = '{:.2f}'
#         plot.text(p.get_x()+p.get_width()/2, p.get_height()+ax.get_ylim()[1]/200, value_format.format(p.get_height()), fontsize=250/len(names), ha='center')
# ax.set_ylim(top=ax.get_ylim()[1]*(1+(0.8/len(names))))
# plot.set_xlabel('')
# plot.legend(loc='center right', bbox_to_anchor=(1.11, 0.5), framealpha=1)
plt.savefig('plot-context.png', format='png', dpi=500, bbox_inches='tight')




print('finished')