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
sns.set_palette(sns.color_palette(['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075']))

### get list of files
files = sorted(glob.glob('*_all.mods'))
print(files)
print('')

### get sample numbers from file names
number = [i.rsplit('_S', 1)[1] for i in files]
number = [i.replace('_mCtoT_all.mods', '') for i in number]
number = [int(i) for i in number]
# number = [3,12,5,7,6,10,8,14,9,16,17,19,18,21,22,24,23,26,27,28,1,11,2,15,20,25,4,13]
print(number)
print('')

### sort file names by numbers
files = [x for _,x in sorted(zip(number, files))]
print(files)

### get sample names from file names
names = [i.rsplit('_S', 1)[0] for i in files]
print(names)
print('')

### get conditions
conditions = ['Alfa50-133','Alfa50-133','Alfa50-133','Alfa50-133','Alfa50-133','Alfa50-133','Alfa50-133','Alfa5-133','Alfa5-133','Alfa5-133','Alfa5-133','Alfa10-028','Alfa10-028','Alfa10-930','Alfa10-930','Alfa10-931','Acros-321','Acros-321','Acros-321','Acros-321','Acros-145','Sigma-042','Sigma-042','Sigma-042','Sigma-042','MO-133','TCI-B3M','ABCR-255']
print(conditions)
print('')

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

    i['condition'] = conditions[count]
    print(len(i.index))
    print(i.head())
    print('')

    count+=1

### concatenate dataframes
dfc = pd.concat(dfl, axis=0)
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
dfc_lambda = dfc[dfc['#CHROM'] == 'J02459.1']
dfc_lambda = dfc_lambda[dfc_lambda['CONTEXT'] == 'CpG']
dfl_lambda = [dfc_lambda[dfc_lambda['sample'] == i] for i in names]
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
    
    i['194mer_conversion'] = ( i.loc[i['START'] == 17656, 'MOD'].iloc[0] + i.loc[i['START'] == 17657, 'MOD'].iloc[0] ) / ( i.loc[i['START'] == 17656, 'MOD'].iloc[0] + i.loc[i['START'] == 17657, 'MOD'].iloc[0] + i.loc[i['START'] == 17656, 'UNMOD'].iloc[0] + i.loc[i['START'] == 17657, 'UNMOD'].iloc[0] ) * 100
    print(len(i.index))
    print(i.head())
    print('')
    
    i['194mer_calls'] = i.loc[i['START'] == 17656, 'MOD'].iloc[0] + i.loc[i['START'] == 17657, 'MOD'].iloc[0] + i.loc[i['START'] == 17656, 'UNMOD'].iloc[0] + i.loc[i['START'] == 17657, 'UNMOD'].iloc[0]
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
        ax.text(20500, 12, 'Positions uncalled: '+str(dfl_lambda[count]['pos_mod_rate'].isnull().sum()), size=25, weight='bold')
    if dfl_lambda[count].loc[0, '194mer_calls'] == 0:
        ax.text(20500, 2, '194mer: uncalled', size=25, weight='bold')
    else:
        ax.text(20500, 2, '194mer: '+str("{:.1f}".format(dfl_lambda[count].loc[0, '194mer_conversion']))+'% from '+str(dfl_lambda[count].loc[0, '194mer_calls']), size=25, weight='bold')
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
dfc_2kb = dfc[dfc['#CHROM'] == 'unmodified_2kb']
dfc_2kb_all = dfc_2kb
dfl_2kb_all = [dfc_2kb_all[dfc_2kb_all['sample'] == i] for i in names]
dfc_2kb = dfc_2kb[dfc_2kb['CONTEXT'] == 'CpG']
dfl_2kb = [dfc_2kb[dfc_2kb['sample'] == i] for i in names]
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
dfc_pUC19 = dfc[dfc['#CHROM'] == 'pUC19']
dfc_pUC19 = dfc_pUC19[dfc_pUC19['CONTEXT'] == 'CpG']
print(len(dfc_pUC19.index))
print(dfc_pUC19.head())
dfl_pUC19 = [dfc_pUC19[dfc_pUC19['sample'] == i] for i in names]
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
        ax.text(0, 0, 'Positions uncalled: '+str(dfl_pUC19[count]['pos_mod_rate'].isnull().sum()), size=25, weight='bold')
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

sum_condition = dfc_lambda_final[['sample', 'condition']].drop_duplicates()
sum_condition.reset_index(drop=True, inplace=True)
summary['condition'] = sum_condition['condition']

sum_lambda = dfc_lambda_final[['sample', 'avg_read_mod_rate', 'avg_pos_mod_rate', '194mer_conversion', '194mer_calls']].drop_duplicates()
sum_lambda.reset_index(drop=True, inplace=True)
summary['lambda_reads_CpG'] = sum_lambda['avg_read_mod_rate']
summary['lambda_positions_CpG'] = sum_lambda['avg_pos_mod_rate']

sum_pUC19 = dfc_pUC19_final[['sample', 'avg_read_mod_rate', 'avg_pos_mod_rate']].drop_duplicates()
sum_pUC19.reset_index(drop=True, inplace=True)
summary['pUC19_reads_CpG'] = sum_pUC19['avg_read_mod_rate']
summary['pUC19_positions_CpG'] = sum_pUC19['avg_pos_mod_rate']

sum_2kb = dfc_2kb_final[['sample', 'avg_read_mod_rate', 'avg_pos_mod_rate']].drop_duplicates()
sum_2kb.reset_index(drop=True, inplace=True)
summary['2kb_reads_CpG'] = sum_2kb['avg_read_mod_rate']
summary['2kb positions CpG'] = sum_2kb['avg_pos_mod_rate']

sum_2kb_all = dfc_2kb_all_final[['sample', 'avg_read_mod_rate', 'avg_pos_mod_rate']].drop_duplicates()
sum_2kb_all.reset_index(drop=True, inplace=True)
summary['2kb_reads_CpX'] = sum_2kb_all['avg_read_mod_rate']
summary['2kb positions_CpX'] = sum_2kb_all['avg_pos_mod_rate']

summary['194mer_conversion'] = sum_lambda['194mer_conversion']
summary['194mer_calls'] = sum_lambda['194mer_calls']

print(summary)
summary.to_csv('conversion_summary.tsv', sep='\t', index=False)

### generate summary plots
def summary_plot(metric):
    fig = plt.figure(figsize=(11, 7))
    ax = fig.add_subplot(1, 1, 1)
    plot = sns.barplot(x='sample', y=metric, units='sample', hue='condition', dodge=False, data=summary)
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
    plot.legend(loc='center left', bbox_to_anchor=(1, 0.5), framealpha=1)#.remove()
    # for p in plot.patches:
    #     if np.isnan(p.get_height())==False and float('{:.5f}'.format(p.get_height())) in [95.57517, 95.78446, 95.56830, 95.72392, 95.45698, 95.61916, 95.59885, 95.69544]:
    #         print(p.get_x() + p.get_width() / 2)
    #         print(p.get_height())
    #         plot.text(p.get_x() + p.get_width() / 2, p.get_height() - 5, '*', ha='center', fontsize=20, weight=5)
    plt.savefig('mean_'+metric+'.png', format='png', dpi=500, bbox_inches='tight')

summary_plot('lambda_reads_CpG')
summary_plot('2kb_reads_CpG')
summary_plot('pUC19_reads_CpG')

### generate overall vs 194mer plot
fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(1, 1, 1)
plot = sns.scatterplot(data=summary, x='lambda_reads_CpG', y='194mer_conversion', hue='194mer_calls')
ax.set(xlim=(-5, 105))
# ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
# ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
ax.set(ylim=(-5, 105))
# ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
# ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
ax.plot([-5, 105], [-5, 105], linestyle='--', linewidth=1, zorder=0.9, color='grey')
plot.legend(loc='center left', bbox_to_anchor=(1, 0.5), framealpha=1)#.remove()
plt.savefig('conversion_comparison.png', format='png', dpi=500, bbox_inches='tight')

#1 sort out legend titles
#2 make text positions proportion of axis max instead of absolute value