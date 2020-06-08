import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 300)
import glob
import seaborn as sns
sns.set_style('white', {'axes.grid': True, 'xtick.bottom': True, 'ytick.left': True})



all_rsm = glob.glob('*.rna')
print(all_rsm)
print('')

names = [i.replace('.rna', '') for i in all_rsm]
print(names)
print('')


dfm = (pd.read_csv(f, sep='\t', skiprows=7) for f in all_rsm)
dfm=list(dfm)
#print(dfm)
#print('')

samno = 0
for i in dfm:
    i['Sample']=names[samno]
    samno+=1
#print(dfm)
#print('')

dfm = pd.concat(dfm, axis=0)
#print(dfm)
#print('')

unwanted = []
for i in dfm.columns:
    if 'Unnamed' in i:
        unwanted.append(i)
print(unwanted)
print('')

dfm = dfm.drop(unwanted, axis=1)
print(dfm)
print('')


plot = sns.lineplot(x='Percentile', y='Coverage', hue='Sample', data=dfm)

plot.set(xlim=(0, 100))
plot.set(ylim=(0, None))
plot.axes.axhline(1, color='grey', ls='--')


plot.figure.savefig("5'-3'coverage.png")



print('finish')