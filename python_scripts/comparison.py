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



files = sorted(glob.glob('*dedup.csv'))
print(files)
print('')

names = [i.replace('.csv', '') for i in files]
print(names)
print('')

# groups = [re.sub(r'_L.*_mCtoT_positions.mods', '', i) for i in files]
# print(groups)
# print('')



# colnames = ['metric1', 'TOTAL_READS', 'metric3', 'metric4', 'metric5', 'metric6', 'PCT_PF_READS_ALIGNED', 'metric8', 'metric9', 'metric10', 'metric11', 'metric12', 'PF_MISMATCH_RATE', 'PF_HQ_ERROR_RATE', 'PF_INDEL_RATE', 'metric16', 'metric17', 'metric18', 'metric19', 'metric20', 'metric21', 'metric22', 'PCT_CHIMERAS', 'PCT_ADAPTER', 'metric25', 'metric26', 'metric27']
# unwanted = []
# for i in colnames:
#     if 'metric' in i:
#         unwanted.append(i)
# print(unwanted)
# print('')

dfl = [pd.read_csv(f) for f in files]
print(dfl)
print('')


count=0
for i in dfl:
    print(i)
    # i = i.drop('sample', axis=1)
    # print(i)
    # i = i.set_index('pipeline')
    # print(i)
    # i = i.transpose()
    # print(i)
    # i = i.reset_index()
    # print(i)
    dfl[count] = pd.wide_to_long(dfl[count], stubnames=['OMDC', 'BG'], i='sample', j='context', sep='_', suffix='\w+')
    print(i)
    dfl[count] = dfl[count].reset_index()
    print(i)
    count+=1


# count = 0
# for i in dfl:
#     i['sample'] = names[count]
#     i['group'] = groups[count]
#     print(dfl[count])
#     count+=1

# dfc = pd.concat(dfl, axis=0)
# print(dfc)
# print('')

# dfc['conversion'] = dfc['MODIFIED']/(dfc['MODIFIED']+dfc['UNMODIFIED'])*100
# print(dfc)
# print('')

# dfc['sample']=names
# print(dfc)
# print('')

# dfc['group']=groups
# print(dfc)
# print('')

# box = ['BO', 'OR', 'UM', 'OR', 'BO', 'UM', 'SI']
# dfc['box']=box
# print(dfc)
# print('')

# pos = ['None', 'None', 'None', 'None', 'None', 'None', 'None']
# dfc['pos']=pos
# print(dfc)
# print('')

# dfc.to_csv('conversion_summary.tsv', sep='\t')





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

count=0
for i in dfl:
    print(dfl[count])
    fig = plt.figure(figsize=(11, 7))
    ax = fig.add_subplot(1, 1, 1)
    plot = sns.relplot(x='BG', y='OMDC', ci=None, col='context', col_wrap=(4), kind='scatter', height=3, aspect=1.0, s=30, legend=False, data=dfl[count])


    for ax in plot.axes.flat:
        ax.set(xlim=(0, 100))
        ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
        ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
        
        ax.set(ylim=(0, 100))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(20))
        ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
        
        # ax.grid(b=True, which='major')
        
        ax.plot([0, 100], [0, 100], linestyle='--', linewidth=1, color='grey')
        
    plot.set_titles("{col_name}", pad=2)
    
    # plt.plot([0, 100], [0, 100], linestyle='--')
    # for ax in plot.axes.flat:
    #     for lb in ax.get_xticklabels():
    #         lb.set_rotation(90)

    # for p in plot.patches:
    #     if np.isnan(p.get_height())==False:
    #         if p.get_height()>=1:
    #             value_format = '{:#.3g}'
    #         else:
    #             value_format = '{:.2f}'
    #         plot.text(p.get_x()+p.get_width()/2, p.get_height()+ax.get_ylim()[1]/200, value_format.format(p.get_height()), fontsize=250/len(names), ha='center')

    # ax.set_ylim(top=ax.get_ylim()[1]*(1+(0.8/len(names))))

    # for ax in plot.axes.flat:
    #     ax.set_xlabel('')
    # plot.set_xlabel('')
    # plot.legend(loc='center right', bbox_to_anchor=(1.11, 0.5), framealpha=1).remove()

    plt.subplots_adjust(wspace=0.15, hspace=0.15)

    plt.savefig(names[count]+'.png', format='png', dpi=500, bbox_inches='tight')
    count+=1




print('finished')
