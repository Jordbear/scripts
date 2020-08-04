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
sns.set_palette(sns.color_palette(['#ce0e2d', '#005cb9', '#f5a800', '#45c2b1', '#035c67']))



files = sorted(glob.glob('*_mCtoT_all.mods'))
print(files)
print('')

names = [i.replace('_mCtoT_all.mods', '') for i in files]
print(names)
print('')




# colnames = ['metric1', 'TOTAL_READS', 'metric3', 'metric4', 'metric5', 'metric6', 'PCT_PF_READS_ALIGNED', 'metric8', 'metric9', 'metric10', 'metric11', 'metric12', 'PF_MISMATCH_RATE', 'PF_HQ_ERROR_RATE', 'PF_INDEL_RATE', 'metric16', 'metric17', 'metric18', 'metric19', 'metric20', 'metric21', 'metric22', 'PCT_CHIMERAS', 'PCT_ADAPTER', 'metric25', 'metric26', 'metric27']
# unwanted = []
# for i in colnames:
#     if 'metric' in i:
#         unwanted.append(i)
# print(unwanted)
# print('')

dfl = [pd.read_csv(f, sep='\t') for f in files]
# print(dfl)
# print('')

count = 0
for i in dfl:
    i['sample'] = names[count]
    print(len(dfl[count].index))
    print(dfl[count].head())
    dfl[count] = dfl[count][dfl[count]['CONTEXT'] == 'CpG']
    print(len(dfl[count].index))
    print(dfl[count].head())
    dfl[count] = dfl[count][dfl[count]['TOTAL_DEPTH'] > 3]
    print(len(dfl[count].index))
    print(dfl[count].head())
    dfl[count]['mod_rate'] = dfl[count]['MOD'].sum()/(dfl[count]['MOD'].sum()+dfl[count]['UNMOD'].sum())*100
    print(len(dfl[count].index))
    print(dfl[count].head())
    count+=1


dfc = pd.concat(dfl, axis=0)
print(len(dfc.index))
print(dfc.head())
print('')


# dfc['sample']=names
# print(dfc)
# print('')

# dfc['group']=group
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

dfc.to_csv('conversion_summary.tsv', sep='\t')



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
    plot = sns.barplot(x='sample', y=y, hue=variable, units='sample', dodge=False, data=dfc)
    
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
    
    plt.savefig(y+'.png', format='png', dpi=500, bbox_inches='tight')


barplot('mod_rate', variable)
# barplot('MEAN_MODIFICATION_RATE_PERCENT', variable)
# barplot('PF_HQ_ERROR_RATE', variable)
# barplot('PF_INDEL_RATE', variable)
# barplot('PCT_CHIMERAS', variable)
# barplot('PCT_ADAPTER', variable)



print('finished')