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



files = sorted(glob.glob('*_all.mods'))
print(files)
print('')

names = [i.split('_S')[0] for i in files]
print(names)
print('')

conditions = [i[4:] for i in names]
print(conditions)
print('')

number = [i.split('_S')[1] for i in files]
number = [i.replace('_001_mCtoT_all.mods', '') for i in number]
number = ['0'+i for i in number]
number = [i[-2:] for i in number]
print(number)
print('')



dfl = [pd.read_csv(f, sep='\t', usecols=['START','MOD_LEVEL', 'MOD', 'UNMOD', 'CONTEXT', 'TOTAL_DEPTH']) for f in files]
# print(dfl)
# print('')

bed = pd.read_csv('/Users/jordanbrown/sequencing/references/spikes/J02459.1/J02459.1_100bpslidingwindows_nuc.bed', sep='\t')
print(bed.head())
print('')
bed.set_index('4_usercol', inplace=True)
print(bed.head())
print('')

for df in dfl:
    df['GC'] = np.nan
    for index, row in df.iterrows():
        pos = df.loc[index, 'START']
        if 50 <= pos <= 48389:
            df.loc[index, 'GC'] = bed.loc[pos, '6_pct_gc']
    print(df.head())


count = 0
for i in dfl:
    i['sample'] = names[count]
    print(len(dfl[count].index))
    print(dfl[count].head())

    i['condition'] = conditions[count]
    print(len(dfl[count].index))
    print(dfl[count].head())

    i['number'] = number[count]
    print(len(dfl[count].index))
    print(dfl[count].head())

    dfl[count] = dfl[count][dfl[count]['CONTEXT'] == 'CpG']
    print(len(dfl[count].index))
    print(dfl[count].head())

    dfl[count]['mean_call_rate'] = dfl[count]['MOD'].sum()/(dfl[count]['MOD'].sum()+dfl[count]['UNMOD'].sum())*100
    print(len(dfl[count].index))
    print(dfl[count].head())

    dfl[count]['pos_mod_rate'] = dfl[count]['MOD']/(dfl[count]['MOD']+dfl[count]['UNMOD'])*100
    print(len(dfl[count].index))
    print(dfl[count].head())

    for index, row in dfl[count].iterrows():
        if dfl[count].loc[index, 'MOD'] + dfl[count].loc[index, 'UNMOD'] < 3:
            print('happened')
            dfl[count].loc[index, 'pos_mod_rate'] = np.nan

    dfl[count]['mean_pos_rate'] = dfl[count]['pos_mod_rate'].mean()
    print(len(dfl[count].index))
    print(dfl[count].head())

    dfl[count]['rolling'] = dfl[count].rolling(window=100, center=True)['pos_mod_rate'].mean()
    print(len(dfl[count].index))
    print(dfl[count].head())

    count+=1


# print(dfl[4])
# dfl[4].to_csv('test.tsv', sep='\t')

dfc = pd.concat(dfl, axis=0)
print(len(dfc.index))
print(dfc.head())
print('')

# dfc = dfc.sort_values(['number'])
dfc.to_csv('conversion_summary.tsv', sep='\t')

# dfc = dfc.sort_values(['condition', 'library', 'sample'])

variable = 'sample'

dfc1 = dfc[dfc['sample'].isin(['S01-PyB-AL50', 'S02-PyB-AL50', 'S03-PyB-AL5', 'S04-PyB-AL5', 'S05-PyB-ACR', 'S06-PyB-ACR', 'S07-PyB-SIG', 'S08-PyB-SIG'])]
dfc2 = dfc[dfc['sample'].isin(['S09-FLAG-NO2', 'S10-FLAG-NO3', 'S11-HIS-TAL0', 'S12-HIS-TAL10', 'S13-FLAG-1', 'S14-FLAG-2', 'S15-MERCK', 'S16-Inn-HIS-Tal0', 'S17-HIS-CO-1'])]
dfc3 = dfc[dfc['sample'].isin(['S17-HIS-CO-1', 'S18-HIS-CO-05', 'S19-HIS-CO-2', 'S20-HIS-CO-5'])]



comparison = pd.melt(dfc, id_vars=['sample', 'condition'], value_vars=['mean_call_rate', 'mean_pos_rate'])
print(comparison.head())

fig = plt.figure(figsize=(11, 7))
ax = fig.add_subplot(1, 1, 1)
plot = sns.barplot(x='sample', y='mean_call_rate', units='sample', hue='condition', dodge=False, data=dfc)
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
plot.legend(loc='center right', bbox_to_anchor=(1.18, 0.5), framealpha=1)#.remove()
# for p in plot.patches:
#     if np.isnan(p.get_height())==False and float('{:.5f}'.format(p.get_height())) in [95.57517, 95.78446, 95.56830, 95.72392, 95.45698, 95.61916, 95.59885, 95.69544]:
#         print(p.get_x() + p.get_width() / 2)
#         print(p.get_height())
#         plot.text(p.get_x() + p.get_width() / 2, p.get_height() - 5, '*', ha='center', fontsize=20, weight=5)
plt.savefig('mean_mod.png', format='png', dpi=500, bbox_inches='tight')




fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(1, 1, 1)
plot = sns.relplot(x='START', y='pos_mod_rate', kind='scatter', hue='GC', palette='coolwarm', col='sample', col_wrap=4, units='sample', linewidth=0, aspect=1.6, height=5, estimator=None, data=dfc)
count=0
for ax in plot.axes.flat:
    for i, spine in ax.spines.items():
        spine.set_visible(True)
    # sns.lineplot(x='START', y='rolling', estimator=None, color='black', zorder=1, linewidth=3, legend=False, data=dfl[count], ax=ax)
    sns.scatterplot(x='START', y='rolling', color='black', zorder=1, size=3, linewidth=0, legend=False, data=dfl[count], ax=ax)
    if dfl[count]['pos_mod_rate'].isnull().sum() > 0:
        ax.text(20500, 3, 'Positions uncalled: '+str(dfl[count]['pos_mod_rate'].isnull().sum()), size=25, weight='bold')
    ax.set_xlabel('Position', size=20)
    ax.set_ylabel('Modification rate (%)' , size=20)
    for i, spine in ax.spines.items():
        spine.set_visible(True)
    count+=1
plot.set_titles("{col_name}", pad=2, size=20)
# plot.set(xlim=(0, dfl[0]['START'].max()))
# plot.set(ylim=(0, None))
# ax.legend(loc='center right', bbox_to_anchor=(1.2, 0.5), framealpha=1).remove()
# def commas(x, pos):
#     return '{:,}'.format(int(x))
# ax.get_xaxis().set_major_formatter(plt.FuncFormatter(commas))
plt.subplots_adjust(wspace=0.1, hspace=0.12)
# plt.setp(plot._legend.get_texts(), fontsize=30)
plt.savefig('mod_by_pos.png', format='png', dpi=500, bbox_inches='tight')

print('finished')
