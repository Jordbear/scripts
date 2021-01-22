#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 09:13:07 2021

@author: jordanbrown
"""

import re
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 200)
import glob
from matplotlib import pyplot as plt
from matplotlib import ticker as ticker
import seaborn as sns
sns.set_style('white', {'axes.grid': True, 'xtick.bottom': True, 'ytick.left': True})
sns.set_context(rc={'patch.linewidth': '0.0'})
sns.set_palette(sns.color_palette('muted'))

### read file
df = pd.read_csv('/Users/jordanbrown/Downloads/Tet QC Results Modified.csv', sep=',', usecols=['Sequencing date', 'Enzyme Used', 'Tet QC', 'λ (%) CpG'])
print(df)
print('')

### sort by custom order
df['Enzyme Used'] = df['Enzyme Used'].astype('category')
df['Enzyme Used'].cat.set_categories(['FLAG-mTet1-NO2', 'FLAG-mTet1-NO3', 'FLAG-1 (5th)', 'FLAG-2 (18th)', 'Merck-mTet1', 'HIS-mTet1-CO', 'HIS-Nickel-25 mM', 'HIS-Nickel-50 mM', 'HIS-TAL-0', 'HIS-TAL-10', 'Innovate', 'HIS-TAL-10 Batch 3', 'HIS-TAL-10 Batch 4', 'HIS-TAL-10 Batch 5', 'HIS-TAL-10 Batch 6'], inplace=True)
df.sort_values(['Enzyme Used'])
# df.sort_values(['Enzyme Used'], inplace=True)
# df.reindex()
print(df)
print('')

### plot
fig = plt.figure(figsize=(11, 7))
ax = fig.add_subplot(1, 1, 1)
plot = sns.boxplot(x='Enzyme Used', y='λ (%) CpG', whis=10, color='white', data=df)
sns.swarmplot(x='Enzyme Used', y='λ (%) CpG', hue='Tet QC', data=df)
for lb in plot.get_xticklabels():
    lb.set_rotation(90)
# ax.set(ylim=(77, 99))
ax.yaxis.set_major_locator(ticker.MultipleLocator(2))
ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
plt.legend(title='Tet QC', framealpha=1)
plt.savefig('box.png', format='png', dpi=500, bbox_inches='tight')

### sort by date
df['new_date'] = pd.to_datetime(df['Sequencing date'], dayfirst=True)
df.sort_values(['new_date'], inplace=True)
# df = df.iloc[30:]
print(df)
print('')

### plot
fig = plt.figure(figsize=(11, 7))
ax = fig.add_subplot(1, 1, 1)
plot = sns.swarmplot(data=df, x="Sequencing date", y="λ (%) CpG", hue='Enzyme Used')
for lb in plot.get_xticklabels():
    lb.set_rotation(90)
# ax.set(ylim=(77, 99))
ax.yaxis.set_major_locator(ticker.MultipleLocator(2))
ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
plot.legend(loc='center right', bbox_to_anchor=(1.24, 0.5), framealpha=1)#.remove()
plt.savefig('point.png', format='png', dpi=500, bbox_inches='tight')
