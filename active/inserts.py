#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 11:58:43 2021

@author: jordanbrown
"""

import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 300)
import glob
from matplotlib import pyplot as plt
import seaborn as sns
sns.set_style('white', {'axes.grid': True, 'xtick.bottom': True, 'ytick.left': True})
sns.set_context(rc={'patch.linewidth': '0.0'})
sns.set_palette(sns.color_palette('muted'))

### get list of files
files = sorted(glob.glob('*_inserts.tsv'))
print(files)
print('')

### get sample names from file names
names = [i.rsplit('_S', 1)[0] for i in files]
print(names)
print('')

### get sample numbers from file names
number = [i.split('_S')[-1] for i in files]
number = [i.replace('_inserts.tsv', '') for i in number]
number = ['0'+i for i in number]
number = [i[-2:] for i in number]
print(number)
print('')

### get conditions
conditions = [i[4:8] for i in names]
print(conditions)
print('')

### read in dataframes
dfl = [pd.read_csv(f, sep='\t', skiprows=10, index_col=False) for f in files]

### check each dataframe for split reads and format appropriately
count=0
for i in dfl:
    if i.columns[0] == '## HISTOGRAM':
        i = pd.read_csv(files[count], sep='\t', skiprows=11, index_col=False)
        i['Reads'] = i['All_Reads.fr_count']+i['All_Reads.rf_count']
        i.drop(columns=['All_Reads.fr_count', 'All_Reads.rf_count'], inplace=True)
    else:
        i.rename(columns={'All_Reads.fr_count': 'Reads', 'insert_size': 'Insert Size'}, inplace=True)
    print(i.head())

### add sample information to dataframes individually
count = 0
for i in dfl:
    i['sample'] = names[count]
    i['number'] = number[count]
    i['condition'] = conditions[count]
    print(len(i.index))
    print(i.head())
    print(i)
    count+=1

### concatenate dataframes
dfc = pd.concat(dfl, axis=0)
print(dfc.head())
print('')

### plot
fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(1, 1, 1)
plot = sns.lineplot(x='Insert Size', y='Reads', hue='condition', units='sample', estimator=None, data=dfc)
sns.despine()
plot.set(xlim=(0, None))
plot.set(ylim=(0, None))
plot.legend(loc='center right', bbox_to_anchor=(1.2, 0.5), framealpha=1)
# def commas(x, pos):
#     return '{:,}'.format(int(x))
# ax.get_yaxis().set_major_formatter(plt.FuncFormatter(commas))
def human_readable(x, pos):
    if len(str(int(x))) > 6:
        human_label = str(int(x))[:-6]+'m'
    elif len(str(int(x))) > 3:
        human_label = str(int(x))[:-3]+'k'
    else:
        human_label = int(x)
    return human_label
ax.get_yaxis().set_major_formatter(plt.FuncFormatter(human_readable))
plt.savefig('inserts.png', format='png', dpi=500, bbox_inches='tight')