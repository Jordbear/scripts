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
sns.set_palette(sns.color_palette(['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075']))

### get list of files
files = sorted(glob.glob('*_gc_bias.tsv'))
print(files)
print('')

### get sample numbers from file names
number = [i.rsplit('_S', 1)[1] for i in files]
number = [i.replace('_gc_bias.tsv', '') for i in number]
number = [int(i) for i in number]
# number = [1, 2, 3, 4, 5, 6, 7, 8]
print(number)
print('')

### sort file names by numbers
files = [x for _,x in sorted(zip(number, files))]
# files = files[6:10]
print(files)
print('')

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
# dfc = dfc.sort_values(['number'])
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
# def commas(x, pos):
#     return '{:,}'.format(int(x))
# ax1.get_yaxis().set_major_formatter(plt.FuncFormatter(commas))
def human_readable(x, pos):
    if len(str(int(x))) > 6:
        human_label = str(int(x))[:-6]+'m'
    elif len(str(int(x))) > 3:
        human_label = str(int(x))[:-3]+'k'
    else:
        human_label = int(x)
    return human_label
ax1.get_yaxis().set_major_formatter(plt.FuncFormatter(human_readable))
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
ax2.legend(loc='center left', bbox_to_anchor=(1.15, 0.5), framealpha=1)#.remove()
ax2.grid(False)
ax2.yaxis.tick_left()
ax2.yaxis.set_label_position('left')
ax2.set(xlabel='GC percentage of windows', ylabel='Normalised coverage')

### save figure
plt.savefig('gc_bias'+tag+'.png', format='png', dpi=500, bbox_inches='tight')