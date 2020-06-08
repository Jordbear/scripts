#!/usr/bin/python3
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
sns.set_palette(sns.color_palette(['#618cd9', '#d8874a', '#59aa63', '#c04f50', '#8571b8', '#92795e']))



all_asm = glob.glob('*alignment.tsv')


names = []
for i in all_asm:
        names.append(i)
namesx = [i.replace('_dmarked_alignment.tsv', '') for i in names]
print(namesx)
print('')


colnames = ['Metric1', 'Metric2', 'Metric3', 'Metric4', 'Metric5', 'Metric6', 'PCT_PF_READS_ALIGNED', 'Metric8', 'Metric9', 'Metric10', 'Metric11', 'Metric12', 'PF_MISMATCH_RATE', 'PF_HQ_ERROR_RATE', 'PF_INDEL_RATE', 'Metric16', 'Metric17', 'Metric18', 'Metric19', 'Metric20', 'Metric21', 'Metric22', 'PCT_CHIMERAS', 'PCT_ADAPTER', 'Metric25', 'Metric26', 'Metric27']
unwanted = []
for i in colnames:
    if 'Metric' in i:
        unwanted.append(i)
print(unwanted)
print('')

dfm = (pd.read_csv(f, sep='\t', skiprows=9, names=colnames) for f in all_asm)
dfm = pd.concat(dfm, axis=0)
#print(dfm)
#print('')

dfm.drop(unwanted, axis=1, inplace=True)
print(dfm)
print('')

dfm.PCT_PF_READS_ALIGNED = 1-dfm.PCT_PF_READS_ALIGNED
dfm = dfm.rename(columns={'PCT_PF_READS_ALIGNED': 'PCT_PF_READS_UNALIGNED'})
print(dfm)
print('')

dfm[dfm.select_dtypes(include='number').columns]*=100
print(dfm)
print('')

dfm['Sample']=namesx
#print(dfm)
#print('')

dfm = dfm.set_index('Sample')
#print(dfm)
#print('')

dfm = dfm.stack()
#print(dfm)
#print('')

dfm = dfm.reset_index()
#print(dfm)
#print('')

dfm.columns=['Sample', 'Metric', 'Percentage']
#print(dfm)
#print('')


plot = sns.catplot(x='Metric', y='Percentage', col='Sample', kind='bar', aspect=0.5, col_wrap=None, data=dfm)

for ax in plot.axes.flat:
    for lb in ax.get_xticklabels():
        lb.set_rotation(90)
        
for ax in plot.axes.flat:
    ax.set_xlabel('')
plot.set_titles(col_template='{col_name}')

plot.fig.subplots_adjust(wspace=0.01)


plot.savefig('sea.png')


def barplot():
    fig = plt.figure(figsize=(11, 7))
    ax = fig.add_subplot(1, 1, 1)
    plot = sns.barplot(x='Metric', y='Percentage', hue='Metric', dodge=False, data=dfm)
    
    for lb in plot.get_xticklabels():
        lb.set_rotation(90)   
    
    for p in plot.patches:
        if np.isnan(p.get_height())==False:
            if p.get_height()>=1:
                value_format = '{:#.3g}'
            else:
                value_format = '{:.2f}'
            plot.text(p.get_x()+p.get_width()/2, p.get_height()+ax.get_ylim()[1]/200, value_format.format(p.get_height()), fontsize=20, ha='center')
    
    ax.set_ylim(top=ax.get_ylim()[1]*(1+(0.8/6)))
    
    plot.set_xlabel('')
    
    #plot.legend(loc='center right', bbox_to_anchor=(1.3, 0.5), framealpha=1)
    ax.get_legend().remove()
    
    plt.savefig('alignment'+'.png', format='png', dpi=500, bbox_inches='tight')

barplot()


print('finish')