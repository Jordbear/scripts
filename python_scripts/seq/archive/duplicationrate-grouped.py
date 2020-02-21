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


all_asm = glob.glob('*.tabular')


names = []
for i in all_asm:
        names.append(i)
namesx = [i.replace('.tabular', '') for i in names]
namesx = [i.replace('Duplicates', '') for i in namesx]
print(namesx)
print('')


colnames = ['Metric1', 'Metric2', 'Metric3', 'Metric4', 'Metric5', 'Metric6', 'Metric7', 'Metric8', 'PERCENT_DUPLICATION', 'Metric10']
unwanted = []
for i in colnames:
    if 'Metric' in i:
        unwanted.append(i)
#print(unwanted)
#print('')

dfm = (pd.read_csv(f, sep='\t', skiprows=7, nrows=1, names=colnames) for f in all_asm)
dfm=list(dfm)

groups = ['+BRB', '-BRB', '+BRB', '-BRB', 'Tube'] 

grpno = 0
for i in dfm:
    i['Group']=groups[grpno]
    grpno+=1
#print(dfm)
#print('')

dfm = pd.concat(dfm, axis=0)
#print(dfm)
#print('')

dfm[dfm.select_dtypes(include='number').columns]*=100
#print(dfm)
#print('')

dfm.drop(unwanted, axis=1, inplace=True)
#print(dfm)
#print('')

dfm['Sample']=namesx
#print(dfm)
#print('')

dfm.columns=['Percentage', 'Group', 'Sample']
print(dfm)
print('')


plt.figure(figsize=(5,7))
plot = sns.barplot(x='Sample', y='Percentage', hue='Group', dodge=False, data=dfm)
for lb in plot.get_xticklabels():
    lb.set_rotation(90)   
plot.set_xlabel('')
plot.set_title('% Duplication')
plot.legend(loc='center right', bbox_to_anchor=(1.3, 0.5), framealpha=1)
for p in plot.patches:
    if numpy.isnan(p.get_height())==False:
         plot.text(p.get_x()+p.get_width()/2, p.get_height()+p.get_height()/100, '{:.2f}'.format(p.get_height()), ha='center')
plot.figure.savefig('duplication_rate.png', format='png', dpi=1000, bbox_inches='tight')



print('finish')