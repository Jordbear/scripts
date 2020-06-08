import numpy
from matplotlib import pyplot as plt
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 200)
import glob
import seaborn as sns
sns.set_style('white', {'axes.grid': True, 'xtick.bottom': True, 'ytick.left': True})
sns.set_context(rc={'patch.linewidth': '0.0'})
sns.set_palette(sns.color_palette(['#ce0e2d', '#005cb9', '#f5a800', '#45c2b1', '#035c67']))


all_asm = glob.glob('*.alignment_summary_metrics')


names = []
for i in all_asm:
        names.append(i)
namesx = [i.replace('.alignment_summary_metrics', '') for i in names]
namesx = [i.replace('MultipleMetrics', '') for i in namesx]
print(namesx)
print('')


colnames = ['Metric1', 'Metric2', 'Metric3', 'Metric4', 'Metric5', 'Metric6', 'PCT_PF_READS_ALIGNED', 'Metric8', 'Metric9', 'Metric10', 'Metric11', 'Metric12', 'Metric13', 'Metric14', 'Metric15', 'Metric16', 'Metric17', 'Metric18', 'Metric19', 'Metric20', 'Metric21', 'Metric22', 'Metric23', 'PCT_ADAPTER', 'Metric25', 'Metric26', 'Metric27']
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
#print(dfm)
#print('')

dfm.PCT_PF_READS_ALIGNED = 1-dfm.PCT_PF_READS_ALIGNED
dfm = dfm.rename(columns={'PCT_PF_READS_ALIGNED': 'PCT_PF_READS_UNALIGNED'})
#print(dfm)
#print('')

dfm[dfm.select_dtypes(include='number').columns]*=100
#print(dfm)
#print('')

dfm['Sample']=namesx
print(dfm)
print('')

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
print(dfm)
print('')

groups = ['+BRB', '+BRB', '-BRB', '-BRB', '+BRB', '+BRB', '-BRB', '-BRB', 'Tube', 'Tube']
dfm['Group']=groups
print(dfm)
print('')

dfmu = dfm[dfm.Metric == 'PCT_PF_READS_UNALIGNED']
print(dfmu)
print('')

dfma = dfm[dfm.Metric == 'PCT_ADAPTER']
print(dfma)
print('')


plt.figure(figsize=(5,7))
plotu = sns.barplot(x='Sample', y='Percentage', hue='Group', dodge=False, data=dfmu)
for lb in plotu.get_xticklabels():
    lb.set_rotation(90)
plotu.set_xlabel('')
plotu.set_title('% Unaligned')
plotu.legend(loc='center right', bbox_to_anchor=(1.3, 0.5), framealpha=1)
for p in plotu.patches:
    if numpy.isnan(p.get_height())==False:
         plotu.text(p.get_x()+p.get_width()/2, p.get_height()+p.get_height()/100, '{:.2f}'.format(p.get_height()), ha='center')
plotu.figure.savefig('unaligned_grouped.png', format='png', dpi=1000, bbox_inches='tight')

plt.figure(figsize=(5,7))
plota = sns.barplot(x='Sample', y='Percentage', hue='Group', dodge=False, data=dfma)
for lb in plota.get_xticklabels():
    lb.set_rotation(90)   
plota.set_xlabel('')
plota.set_title('% Adapter Dimer')
plota.legend(loc='center right', bbox_to_anchor=(1.3, 0.5), framealpha=1)
for p in plota.patches:
    if numpy.isnan(p.get_height())==False:
         plota.text(p.get_x()+p.get_width()/2, p.get_height()+p.get_height()/100, '{:.2f}'.format(p.get_height()), ha='center')
plota.figure.savefig('adapter_grouped.png', format='png', dpi=1000, bbox_inches='tight')



print('finish')