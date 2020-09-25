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



df = pd.read_csv('read_totals.tsv', sep='\t', header=None, prefix='X')
print(df)

df = df.set_index('X0').transpose().dropna()
print(df)

df['name'] = [i.split('_S')[0] for i in df['sample'].tolist()]
print(df)

df['condition'] = [re.search('-(.*)-', i)[1] for i in df['sample'].tolist()]
print(df)

df['library'] = [re.search('-(.)_', i)[1] for i in df['sample'].tolist()]
print(df)

df['ratio'] = pd.to_numeric(df['ratio'], downcast='float')

df['percent'] = df['ratio']*100
print(df)

df = df.sort_values(['condition', 'library', 'sample'])
print(df)

df.to_csv('reads_summary.tsv', sep='\t')



fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(1, 1, 1)
plot = sns.barplot(x='name', y='percent', hue='condition', units='sample', ci=None, dodge=False, data=df)

for lb in plot.get_xticklabels():
    lb.set_rotation(90)   

for p in plot.patches:
    if np.isnan(p.get_height())==False:
        if p.get_height()>=1:
            value_format = '{:.0f}'
        else:
            value_format = '{:.2f}'
        plot.text(p.get_x()+p.get_width()/2, p.get_height()+ax.get_ylim()[1]/200, value_format.format(p.get_height()), fontsize=250/len(df['name']), ha='center')

ax.set_ylim(top=ax.get_ylim()[1]*(1+(0.8/len(df['name']))))

plot.set_xlabel('')
plot.set_ylabel('Percent of total reads')
plot.legend(loc='center right', bbox_to_anchor=(1.11, 0.5), framealpha=1).remove()

for p in plot.patches:
    if np.isnan(p.get_height())==False and float('{:.6f}'.format(p.get_height())) in [0.527217, 0.373924, 0.530483, 0.369822, 0.547982, 0.401068, 0.583031, 0.412470]:
        print(p.get_x() + p.get_width() / 2)
        print(p.get_height())
        plot.text(p.get_x() + p.get_width() / 2, p.get_height() - (0.05*plot.get_ylim()[1]), '*', ha='center', fontsize=20, weight=5)

plt.savefig('read_proportion.png', format='png', dpi=500, bbox_inches='tight')



print('finished')
