#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 11:58:43 2021

@author: jordanbrown
"""

from matplotlib import pyplot as plt
from matplotlib import ticker as ticker
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 200)
import glob
import seaborn as sns
sns.set_style('white', {'axes.grid': True, 'xtick.bottom': True, 'ytick.left': False})
sns.set_context(rc={'patch.linewidth': '0.0'})
sns.set_palette(sns.color_palette('muted'))

### get list of files
files = sorted(glob.glob('*_gc.tsv'))
print(files)
print('')

### get sample names from file names
names = [i.rsplit('_S', 1)[0] for i in files]
print(names)
print('')

### get sample numbers from file names
number = [i.split('_S')[-1] for i in files]
number = [i.replace('_gc.tsv', '') for i in number]
number = ['0'+i for i in number]
number = [i[-2:] for i in number]
print(number)
print('')

### get conditions
conditions = [i[4:9] for i in names]
print(conditions)
print('')

### read in list of dataframes
dfl = [pd.read_csv(i, sep='\t', skiprows=6) for i in files]

### add sample information to dataframes individually
count = 0
for i in dfl:
    i['sample'] = names[count]
    i['number'] = number[count]
    i['condition'] = conditions[count]
    print(len(dfl[count].index))
    print(dfl[count].head())
    print(dfl[count])
    count+=1

### concatenate dataframes
dfc = pd.concat(dfl, axis=0)
print(dfc)
print('')

### get total number of windows
total_windows = dfl[0]['WINDOWS'].sum()
print(total_windows)
print('')

### sort values by numbers and create subset dataframes
dfc = dfc.sort_values(['number'])
# dfc1 = dfc[dfc['number'].isin(['01', '02', '03', '04', '05', '11'])]
# dfc2 = dfc[dfc['number'].isin(['05', '06', '07', '08', '09', '10'])]
# dfc3 = dfc[dfc['number'].isin(['11', '12', '13', '14', '15', '16', '17', '18'])]

### create figure with twin axes
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
ax2 = ax1.twinx()

### plot the histogram
sns.barplot(x='GC', y='WINDOWS', color='#035c67', data=dfl[0], ax=ax1)
ax1.set(xlim=(0, 100))
ax1.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax1.xaxis.set_major_formatter(ticker.ScalarFormatter())
ymax = int(total_windows/8)
rounded_ymax = round(ymax, 1-len(str(ymax)))
ax1.set(ylim=(0, rounded_ymax))
ax1.yaxis.set_major_locator(ticker.MultipleLocator(rounded_ymax/8))
ax1.yaxis.set_major_formatter(ticker.ScalarFormatter())
def commas(x, pos):
    return '{:,}'.format(int(x))
def mill(x, pos):
    if len(str(x)) > 6:
        mill_label = str(int(x))[:-6]+'M'
    else:
        mill_label = int(x)
    return mill_label
ax1.get_yaxis().set_major_formatter(plt.FuncFormatter(mill))
ax1.grid(b=True, axis='both')
ax1.yaxis.tick_right()
ax1.yaxis.set_label_position('right')
ax1.set(xlabel='GC percentage of windows', ylabel='Number of windows')
ax1.legend(loc='center right', bbox_to_anchor=(1.5, 0.5), framealpha=1).remove()

### plot normalised coverage
ax2.axes.axhline(1, color='grey', ls='--')
sns.lineplot(x='GC', y='NORMALIZED_COVERAGE', hue='condition', units='sample', estimator=None, data=dfc, ax=ax2)
ax2.set(xlim=(0, 100))
ax2.set(ylim=(0, 2))
ax2.legend(loc='center right', bbox_to_anchor=(1.55, 0.5), framealpha=1)#.remove()
ax2.grid(False)
ax2.yaxis.tick_left()
ax2.yaxis.set_label_position('left')
ax2.set(xlabel='GC percentage of windows', ylabel='Normalised coverage')

### save figure
plt.savefig('gc_bias.png', format='png', dpi=500, bbox_inches='tight')