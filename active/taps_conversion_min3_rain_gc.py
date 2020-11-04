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

# conditions = [re.search('-(.*)-', i)[1] for i in files]
# print(conditions)
# print('')

# libraries = [re.search('-(.)_', i)[1] for i in files]
# print(libraries)
# print('')



dfl = [pd.read_csv(f, sep='\t') for f in files]
# print(dfl)
# print('')

bed = pd.read_csv('/Users/jordanbrown/sequencing/references/spikes/J02459.1_100bpslidingwindows_nuc.bed', sep='\t')
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
    # i['condition'] = conditions[count]
    # print(len(dfl[count].index))
    # print(dfl[count].head())
    # i['library'] = libraries[count]
    # print(len(dfl[count].index))
    # print(dfl[count].head())
    dfl[count] = dfl[count][dfl[count]['CONTEXT'] == 'CpG']
    print(len(dfl[count].index))
    print(dfl[count].head())
    dfl[count] = dfl[count][dfl[count]['TOTAL_DEPTH'] > 3]
    print(len(dfl[count].index))
    print(dfl[count].head())
    dfl[count]['pct_mod_rate'] = dfl[count]['MOD'].sum()/(dfl[count]['MOD'].sum()+dfl[count]['UNMOD'].sum())*100
    print(len(dfl[count].index))
    print(dfl[count].head())
    dfl[count]['pct_mod_rate2'] = dfl[count]['MOD']/(dfl[count]['MOD']+dfl[count]['UNMOD'])*100
    print(len(dfl[count].index))
    print(dfl[count].head())
    count+=1


dfc = pd.concat(dfl, axis=0)
print(len(dfc.index))
print(dfc.head())
print('')


dfc.to_csv('conversion_summary.tsv', sep='\t')

# dfc = dfc.sort_values(['condition', 'library', 'sample'])

variable = 'sample'


# fig = plt.figure(figsize=(11, 7))
# ax = fig.add_subplot(1, 1, 1)
# plot = sns.barplot(x='sample', y='TOTAL_READS', hue=variable, units='sample', dodge=False, data=dfc)

# for lb in plot.get_xticklabels():
#     lb.set_rotation(90)

# for p in plot.patches:
#     if np.isnan(p.get_height())==False:
#          plot.text(p.get_x()+p.get_width()/2, ax.get_ylim()[1]/5/len(names), '{:,.0f}'.format(p.get_height()), fontsize=250/len(names), rotation=90, ha='center', va='bottom')

# ax.ticklabel_format(style='plain', axis='y')

# def commas(x, pos):
#     return '{:,}'.format(int(x))
# ax.get_yaxis().set_major_formatter(plt.FuncFormatter(commas))

# plot.set_xlabel('')
# plot.legend(loc='center right', bbox_to_anchor=(1.11, 0.5), framealpha=1)

# plt.savefig('TOTAL_READS-grouped_by_'+variable+'.png', format='png', dpi=500, bbox_inches='tight')


def barplot(y, variable):
    fig = plt.figure(figsize=(11, 7))
    ax = fig.add_subplot(1, 1, 1)
    plot = sns.barplot(x='sample', y=y, units='sample', dodge=False, data=dfc)

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
    plot.legend(loc='center right', bbox_to_anchor=(1.11, 0.5), framealpha=1).remove()

    for p in plot.patches:
        if np.isnan(p.get_height())==False and float('{:.5f}'.format(p.get_height())) in [95.57517, 95.78446, 95.56830, 95.72392, 95.45698, 95.61916, 95.59885, 95.69544]:
            print(p.get_x() + p.get_width() / 2)
            print(p.get_height())
            plot.text(p.get_x() + p.get_width() / 2, p.get_height() - 5, '*', ha='center', fontsize=20, weight=5)

    plt.savefig(y+'.png', format='png', dpi=500, bbox_inches='tight')


# barplot('pct_mod_rate', variable)
# barplot('MEAN_MODIFICATION_RATE_PERCENT', variable)
# barplot('PF_HQ_ERROR_RATE', variable)
# barplot('PF_INDEL_RATE', variable)
# barplot('PCT_CHIMERAS', variable)
# barplot('PCT_ADAPTER', variable)



fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(1, 1, 1)
plot = sns.relplot(x='START', y='pct_mod_rate2', kind='scatter', hue='GC', palette='seismic', col='sample', col_wrap=5, units='sample', linewidth=0, aspect=1.6, height=5, estimator=None, data=dfc)
for ax in plot.axes.flat:
    ax.set_xlabel('Position', size=20)
    ax.set_ylabel('Modification rate (%)' , size=20)
    for i, spine in ax.spines.items():
        spine.set_visible(True)
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
