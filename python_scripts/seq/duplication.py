#!/usr/bin/python3
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 200)
import glob
import seaborn as sns
sns.set_style('white', {'axes.grid': True, 'xtick.bottom': True, 'ytick.left': True})
sns.set_context(rc={'patch.linewidth': '0.0'})
sns.set_palette(sns.color_palette(['#ce0e2d', '#005cb9', '#f5a800', '#45c2b1', '#035c67']))

                                   

files = glob.glob('*dups.tsv')

samples = [i.replace('_dups.tsv', '') for i in files]
samples = [i.replace('_trimmed', '') for i in samples]
print(samples)
print('')



colnames = ['metric1', 'metric2', 'metric3', 'metric4', 'metric5', 'metric6', 'metric7', 'metric8', 'PERCENT_DUPLICATION', 'metric10']
unwanted = []
for i in colnames:
    if 'metric' in i:
        unwanted.append(i)
print(unwanted)
print('')

dfl = [pd.read_csv(f, sep='\t', skiprows=7, nrows=1, names=colnames) for f in files]

dfc = pd.concat(dfl, axis=0)
print(dfc)
print('')

dfc[dfc.select_dtypes(include='number').columns]*=100
print(dfc)
print('')

dfc.drop(unwanted, axis=1, inplace=True)
print(dfc)
print('')

dfc['sample']=samples
print(dfc)
print('')



fig = plt.figure(figsize=(11, 7))
ax = fig.add_subplot(1, 1, 1)
plot = sns.barplot(x='sample', y='PERCENT_DUPLICATION', hue='sample', dodge=False, data=dfc)

for lb in plot.get_xticklabels():
    lb.set_rotation(90)   

for p in plot.patches:
    if np.isnan(p.get_height())==False:
        if p.get_height()>=1:
            value_format = '{:#.3g}'
        else:
            value_format = '{:.2f}'
        plot.text(p.get_x()+p.get_width()/2, p.get_height()+ax.get_ylim()[1]/200, value_format.format(p.get_height()), fontsize=250/len(samples), ha='center')

ax.set_ylim(top=ax.get_ylim()[1]*(1+(0.8/len(samples))))

plot.set_xlabel('')

#plot.legend(loc='center right', bbox_to_anchor=(1.3, 0.5), framealpha=1)
ax.get_legend().remove()

plt.savefig('PERCENT_DUPLICATION.png', format='png', dpi=500, bbox_inches='tight')



print('finished')