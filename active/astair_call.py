#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 11:58:43 2021

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
import seaborn as sns
sns.set_style('white', {'axes.grid': True, 'xtick.bottom': True, 'ytick.left': True})
sns.set_context(rc={'patch.linewidth': '0.0'})
sns.set_palette(sns.color_palette('deep'))

### get list of files
files = sorted(glob.glob('*_all.mods'))
print(files)
print('')

### get sample names from file names
names = [i.rsplit('_S', 1)[0] for i in files]
print(names)
print('')

### get sample numbers from file names
number = [i.rsplit('_S', 1)[1] for i in files]
number = [i.replace('_mCtoT_all.mods', '') for i in number]
number = ['0'+i for i in number]
number = [i[-2:] for i in number]
print(number)
print('')

### get conditions
# conditions = [i[0:-5] for i in names[:2]] + [i[0:-2] for i in names[2:4]] + [i[0:-5] for i in names[4:]]
# print(conditions)
# print('')

### read data into list of dataframes
dfl = [pd.read_csv(f, sep='\t', usecols=['#CHROM', 'START','MOD_LEVEL', 'MOD', 'UNMOD', 'CONTEXT', 'TOTAL_DEPTH']) for f in files]
print(dfl[0])
print('')

### add data columns to dataframes
count = 0
for i in dfl:

    i['sample'] = names[count]
    print(len(i.index))
    print(i.head())
    print('')

    i['number'] = number[count]
    print(len(i.index))
    print(i.head())
    print('')

    # i['condition'] = conditions[count]
    # print(len(i.index))
    # print(i.head())
    # print('')

    count+=1

### concatenate dataframes and sort by number
dfc = pd.concat(dfl, axis=0)
dfc = dfc.sort_values(['number', '#CHROM', 'START'])
dfc.reset_index(drop=True, inplace=True)
print(len(dfc.index))
print(dfc.head())
print('')

### add percent modification column
dfc['pos_mod_rate'] = dfc['MOD']/(dfc['MOD']+dfc['UNMOD'])*100
print(len(dfc.index))
print(dfc.head())
print(dfc['pos_mod_rate'].isna().sum())
print('')

### remove position modification value where total modification calls is less that 3
less3indexes = dfc.query('MOD + UNMOD < 3').index
print(less3indexes)
dfc.loc[less3indexes, 'pos_mod_rate'] = np.nan
print(len(dfc.index))
print(dfc.head())
print(dfc['pos_mod_rate'].isna().sum())
print('')

### process lambda
nums = dfc['number'].unique()
print(nums)
dfc_lambda = dfc[dfc['#CHROM'] == 'J02459.1']
dfc_lambda = dfc_lambda[dfc_lambda['CONTEXT'] == 'CpG']
dfl_lambda = [dfc_lambda[dfc_lambda['number'] == i] for i in nums]
print(len(dfl_lambda[0].index))
print(dfl_lambda[0].head())

bed = pd.read_csv('/Users/jordanbrown/sequencing/references/spikes/J02459.1/J02459.1_100bpslidingwindows_nuc.bed', sep='\t')
bed.set_index('4_usercol', inplace=True)
print(bed.head())
print('')

dfc_lambda['GC'] = np.nan
for index, row in dfc_lambda.iterrows():
    pos = dfc_lambda.loc[index, 'START']
    if 50 <= pos <= 48389:
        dfc_lambda.loc[index, 'GC'] = bed.loc[pos, '6_pct_gc']
print(dfc_lambda.head())
print('')

for i in dfl_lambda:

    i.reset_index(drop=True, inplace=True)
    print(i.head())
    print('')

    i['avg_read_mod_rate'] = i['MOD'].sum()/(i['MOD'].sum()+i['UNMOD'].sum())*100
    print(len(i.index))
    print(i.head())
    print('')

    i['avg_pos_mod_rate'] = i['pos_mod_rate'].mean()
    print(len(i.index))
    print(i.head())
    print('')

    i['rolling'] = i.rolling(window=100, center=True)['pos_mod_rate'].mean()
    print(len(i.index))
    print(i.head())
    print('')

dfc_lambda_final = pd.concat(dfl_lambda, axis=0)

fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(1, 1, 1)
plot = sns.relplot(x='START', y='pos_mod_rate', kind='scatter', hue='GC', palette='coolwarm', col='sample', col_wrap=6, units='sample', linewidth=0, aspect=1.6, height=5, estimator=None, data=dfc_lambda)
count=0
for ax in plot.axes.flat:
    for i, spine in ax.spines.items():
        spine.set_visible(True)
    # sns.lineplot(x='START', y='rolling', estimator=None, color='black', zorder=1, linewidth=3, legend=False, data=dfl_lambda[count], ax=ax)
    sns.scatterplot(x='START', y='rolling', color='black', zorder=1, size=3, linewidth=0, legend=False, data=dfl_lambda[count], ax=ax)
    if dfl_lambda[count]['pos_mod_rate'].isnull().sum() > 0:
        ax.text(20500, 3, 'Positions uncalled: '+str(dfl_lambda[count]['pos_mod_rate'].isnull().sum()), size=25, weight='bold')
    ax.set_xlabel('Position', size=20)
    ax.set_ylabel('Modification rate (%)' , size=20)
    for i, spine in ax.spines.items():
        spine.set_visible(True)
    count+=1
plot.set_titles("{col_name}", pad=2, size=20)
# plot.set(xlim=(0, dfl_lambda[0]['START'].max()))
# plot.set(ylim=(0, None))
# ax.legend(loc='center right', bbox_to_anchor=(1.2, 0.5), framealpha=1).remove()
# def commas(x, pos):
#     return '{:,}'.format(int(x))
# ax.get_xaxis().set_major_formatter(plt.FuncFormatter(commas))
plt.subplots_adjust(wspace=0.1, hspace=0.12)
# plt.setp(plot._legend.get_texts(), fontsize=30)
plt.savefig('mod_by_pos-lambda.png', format='png', dpi=500, bbox_inches='tight')

### process 2kb
nums = dfc['number'].unique()
print(nums)
dfc_2kb = dfc[dfc['#CHROM'] == 'unmodified_2kb']
dfc_2kb_all = dfc_2kb
dfl_2kb_all = [dfc_2kb_all[dfc_2kb_all['number'] == i] for i in nums]
dfc_2kb = dfc_2kb[dfc_2kb['CONTEXT'] == 'CpG']
dfl_2kb = [dfc_2kb[dfc_2kb['number'] == i] for i in nums]
print(len(dfl_2kb[0].index))
print(dfl_2kb[0].head())

for i in dfl_2kb:

    i.reset_index(drop=True, inplace=True)
    print(i.head())
    print('')

    i['avg_read_mod_rate'] = i['MOD'].sum()/(i['MOD'].sum()+i['UNMOD'].sum())*100
    print(len(i.index))
    print(i.head())
    print('')

    i['avg_pos_mod_rate'] = i['pos_mod_rate'].mean()
    print(len(i.index))
    print(i.head())
    print('')

    i['rolling'] = i.rolling(window=100, center=True)['pos_mod_rate'].mean()
    print(len(i.index))
    print(i.head())
    print('')

dfc_2kb_final = pd.concat(dfl_2kb, axis=0)

for i in dfl_2kb_all:

    i.reset_index(drop=True, inplace=True)
    print(i.head())
    print('')

    i['avg_read_mod_rate'] = i['MOD'].sum()/(i['MOD'].sum()+i['UNMOD'].sum())*100
    print(len(i.index))
    print(i.head())
    print('')

    i['avg_pos_mod_rate'] = i['pos_mod_rate'].mean()
    print(len(i.index))
    print(i.head())
    print('')

    i['rolling'] = i.rolling(window=100, center=True)['pos_mod_rate'].mean()
    print(len(i.index))
    print(i.head())
    print('')

dfc_2kb_all_final = pd.concat(dfl_2kb_all, axis=0)

fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(1, 1, 1)
plot = sns.relplot(x='START', y='pos_mod_rate', kind='scatter', palette='coolwarm', col='sample', col_wrap=6, units='sample', linewidth=0, aspect=1.6, height=5, estimator=None, data=dfc_2kb)
count=0
for ax in plot.axes.flat:
    for i, spine in ax.spines.items():
        spine.set_visible(True)
    # sns.lineplot(x='START', y='rolling', estimator=None, color='black', zorder=1, linewidth=3, legend=False, data=dfl_2kb[count], ax=ax)
    sns.scatterplot(x='START', y='rolling', color='black', zorder=1, size=3, linewidth=0, legend=False, data=dfl_2kb[count], ax=ax)
    if dfl_2kb[count]['pos_mod_rate'].isnull().sum() > 0:
        ax.text(260, 4.1, 'Positions uncalled: '+str(dfl_2kb[count]['pos_mod_rate'].isnull().sum()), size=25, weight='bold')
    ax.set_xlabel('Position', size=20)
    ax.set_ylabel('Modification rate (%)' , size=20)
    for i, spine in ax.spines.items():
        spine.set_visible(True)
    count+=1
plot.set_titles("{col_name}", pad=2, size=20)
# plot.set(xlim=(0, dfl_2kb[0]['START'].max()))
# plot.set(ylim=(0, None))
# ax.legend(loc='center right', bbox_to_anchor=(1.2, 0.5), framealpha=1).remove()
# def commas(x, pos):
#     return '{:,}'.format(int(x))
# ax.get_xaxis().set_major_formatter(plt.FuncFormatter(commas))
plt.subplots_adjust(wspace=0.1, hspace=0.12)
# plt.setp(plot._legend.get_texts(), fontsize=30)
plt.savefig('mod_by_pos-2kb.png', format='png', dpi=500, bbox_inches='tight')


### process pUC19
nums = dfc['number'].unique()
print(nums)
dfc_pUC19 = dfc[dfc['#CHROM'] == 'pUC19']
dfc_pUC19 = dfc_pUC19[dfc_pUC19['CONTEXT'] == 'CpG']
print(len(dfc_pUC19.index))
print(dfc_pUC19.head())
dfl_pUC19 = [dfc_pUC19[dfc_pUC19['number'] == i] for i in nums]
print(len(dfl_pUC19[0].index))
print(dfl_pUC19[1].head())

for i in dfl_pUC19:

    i.reset_index(drop=True, inplace=True)
    print(i.head())
    print('')

    i['avg_read_mod_rate'] = i['MOD'].sum()/(i['MOD'].sum()+i['UNMOD'].sum())*100
    print(len(i.index))
    print(i.head())
    print('')

    i['avg_pos_mod_rate'] = i['pos_mod_rate'].mean()
    print(len(i.index))
    print(i.head())
    print('')

    i['rolling'] = i.rolling(window=100, center=True)['pos_mod_rate'].mean()
    print(len(i.index))
    print(i.head())
    print('')

dfc_pUC19_final = pd.concat(dfl_pUC19, axis=0)

fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(1, 1, 1)
plot = sns.relplot(x='START', y='pos_mod_rate', kind='scatter', palette='coolwarm', col='sample', col_wrap=6, units='sample', linewidth=0, aspect=1.6, height=5, estimator=None, data=dfc_pUC19)
count=0
for ax in plot.axes.flat:
    for i, spine in ax.spines.items():
        spine.set_visible(True)
    # sns.lineplot(x='START', y='rolling', estimator=None, color='black', zorder=1, linewidth=3, legend=False, data=dfl_pUC19[count], ax=ax)
    sns.scatterplot(x='START', y='rolling', color='black', zorder=1, size=3, linewidth=0, legend=False, data=dfl_pUC19[count], ax=ax)
    if dfl_pUC19[count]['pos_mod_rate'].isnull().sum() > 0:
        ax.text(200, 0, 'Positions uncalled: '+str(dfl_pUC19[count]['pos_mod_rate'].isnull().sum()), size=25, weight='bold')
    ax.set_xlabel('Position', size=20)
    ax.set_ylabel('Modification rate (%)' , size=20)
    for i, spine in ax.spines.items():
        spine.set_visible(True)
    count+=1
plot.set_titles("{col_name}", pad=2, size=20)
# plot.set(xlim=(0, dfl_pUC19[0]['START'].max()))
# plot.set(ylim=(0, None))
# ax.legend(loc='center right', bbox_to_anchor=(1.2, 0.5), framealpha=1).remove()
# def commas(x, pos):
#     return '{:,}'.format(int(x))
# ax.get_xaxis().set_major_formatter(plt.FuncFormatter(commas))
plt.subplots_adjust(wspace=0.1, hspace=0.12)
# plt.setp(plot._legend.get_texts(), fontsize=30)
plt.savefig('mod_by_pos-pUC19.png', format='png', dpi=500, bbox_inches='tight')

### generate summary table
summary = pd.DataFrame(dfc['sample'].unique(), columns=['sample'])
summary.reset_index(drop=True, inplace=True)

sum_lambda = dfc_lambda_final[['number', 'avg_read_mod_rate', 'avg_pos_mod_rate']].drop_duplicates()
sum_lambda.reset_index(drop=True, inplace=True)
summary['lambda reads CpG'] = sum_lambda['avg_read_mod_rate']
summary['lambda positions CpG'] = sum_lambda['avg_pos_mod_rate']

sum_pUC19 = dfc_pUC19_final[['number', 'avg_read_mod_rate', 'avg_pos_mod_rate']].drop_duplicates()
sum_pUC19.reset_index(drop=True, inplace=True)
summary['pUC19 reads CpG'] = sum_pUC19['avg_read_mod_rate']
summary['pUC19 positions CpG'] = sum_pUC19['avg_pos_mod_rate']

sum_2kb = dfc_2kb_final[['number', 'avg_read_mod_rate', 'avg_pos_mod_rate']].drop_duplicates()
sum_2kb.reset_index(drop=True, inplace=True)
summary['2kb reads CpG'] = sum_2kb['avg_read_mod_rate']
summary['2kb positions CpG'] = sum_2kb['avg_pos_mod_rate']

sum_2kb_all = dfc_2kb_all_final[['number', 'avg_read_mod_rate', 'avg_pos_mod_rate']].drop_duplicates()
sum_2kb_all.reset_index(drop=True, inplace=True)
summary['2kb reads CpX'] = sum_2kb_all['avg_read_mod_rate']
summary['2kb positions CpX'] = sum_2kb_all['avg_pos_mod_rate']

print(summary)
summary.to_csv('conversion_summary.tsv', sep='\t', index=False)

### generate summary plots
def summary_plot(metric):
    fig = plt.figure(figsize=(11, 7))
    ax = fig.add_subplot(1, 1, 1)
    plot = sns.barplot(x='sample', y=metric, units='sample', hue='sample', dodge=False, data=summary)
    for lb in plot.get_xticklabels():
        lb.set_rotation(90)
    for p in plot.patches:
        if np.isnan(p.get_height())==False:
            if p.get_height()>=1:
                value_format = '{:#.3g}'
            else:
                value_format = '{:.2f}'
            plot.text(p.get_x()+p.get_width()/2, p.get_height()+ax.get_ylim()[1]/200, value_format.format(p.get_height()), fontsize=250/len(names), ha='center')
    ax.set_ylim(top=ax.get_ylim()[1]*(1+(0.8/len(names))))
    plot.set_xlabel('')
    plot.set_ylabel('Modification rate (%)')
    plot.legend(loc='center right', bbox_to_anchor=(1.24, 0.5), framealpha=1)#.remove()
    # for p in plot.patches:
    #     if np.isnan(p.get_height())==False and float('{:.5f}'.format(p.get_height())) in [95.57517, 95.78446, 95.56830, 95.72392, 95.45698, 95.61916, 95.59885, 95.69544]:
    #         print(p.get_x() + p.get_width() / 2)
    #         print(p.get_height())
    #         plot.text(p.get_x() + p.get_width() / 2, p.get_height() - 5, '*', ha='center', fontsize=20, weight=5)
    plt.savefig('mean_'+metric+'.png', format='png', dpi=500, bbox_inches='tight')

summary_plot('lambda reads CpG')
summary_plot('2kb reads CpG')
summary_plot('pUC19 reads CpG')

#1 sort out legend titles
#2 add support for conditon grouping
#3 add support for subsetting by number
