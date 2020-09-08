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



files = sorted(glob.glob('*.error_summary_metrics'))
print(files)
print('')

names = [i.split('_S')[0] for i in files]
print(names)
print('')

contigs = [re.search('artifacts-(.*).err', i)[1] for i in files]
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
    i['error_rate'] = i['SUBSTITUTION_RATE'] * 100
    print(dfl[count])
    count+=1


dfc = pd.concat(dfl, axis=0)
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


dfc.to_csv('conversion_summary.tsv', sep='\t')



fig = plt.figure(figsize=(11, 5))
ax = fig.add_subplot(1, 1, 1)
plot = sns.catplot(x='sample', y='error_rate', hue='SUBSTITUTION', col='contig', units='sample', dodge=True, height=6, aspect=1.2, kind='bar', data=dfc)
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
plt.savefig('plot.png', format='png', dpi=500, bbox_inches='tight')




print('finished')