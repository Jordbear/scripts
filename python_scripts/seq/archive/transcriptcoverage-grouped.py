import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 300)
import glob
import seaborn as sns
sns.set_style('white', {'axes.grid': True, 'xtick.bottom': True, 'ytick.left': True})
sns.set_palette(sns.color_palette(['#ce0e2d', '#005cb9', '#f5a800', '#45c2b1', '#035c67']))



all_rsm = glob.glob('*.tabular')
print(all_rsm)
print('')

names = [i for i in all_rsm]
print(names)
print('')
namesx = [i.replace('.tabular', '') for i in names]
print(namesx)
print('')

dfm = (pd.read_csv(f, sep='\t', skiprows=10) for f in all_rsm)
dfm=list(dfm)
#print(dfm)
#print('')

samno = 0
for i in dfm:
    i['Sample']=namesx[samno]
    samno+=1
#print(dfm)
#print('')
 
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

dfm.columns=["Transcript position (5'-3' %)", 'Normalised Coverage', 'Sample', 'Group']
#print(dfm)
#print('')


plot = sns.lineplot(x="Transcript position (5'-3' %)", y='Normalised Coverage', hue='Group', units='Sample', estimator=None, data=dfm)

plot.set(xlim=(0, 100))
plot.set(ylim=(0, None))
plot.axes.axhline(1, color='grey', ls='--')
plot.legend(loc='center right', bbox_to_anchor=(1.25, 0.5), framealpha=1)


plot.figure.savefig("5'-3'coverage_grouped.png", format='png', dpi=1000, bbox_inches='tight')



print('finish')