import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 300)
import glob
import seaborn as sns
sns.set_style('white', {'axes.grid': True, 'xtick.bottom': True, 'ytick.left': True})
sns.set_context(rc={'patch.linewidth': '0.0'})
sns.set_palette(sns.color_palette(['#ce0e2d', '#005cb9', '#f5a800', '#45c2b1', '#035c67']))


                                   
all_ism = glob.glob('*.insert_size_metrics')
print(all_ism)
print('')


names = [i for i in all_ism]
print(names)
print('')
namesx = [i.replace('.insert_size_metrics', '') for i in names]
print(namesx)
print('')


dfm = (pd.read_csv(f, sep='\t', skiprows=10) for f in all_ism)
dfm=list(dfm)
#print(dfm)
#print('')

samno = 0
for i in dfm:
    i['Sample']=namesx[samno]
    samno+=1
#print(dfm)
#print('')

for i in dfm:
    total_reads = i['All_Reads.fr_count'].sum()
    i['All_Reads.fr_count'] = i['All_Reads.fr_count'].div(total_reads)

dfm = pd.concat(dfm, axis=0)
#print(dfm)
#print('')

dfm.columns=['Insert Size (bp)', 'Proportion of Reads', 'Sample']
print(dfm)
print('')


plot = sns.lineplot(x='Insert Size (bp)', y='Proportion of Reads', hue='Sample', data=dfm)
sns.despine()
plot.set(xlim=(0, 405))
plot.set(ylim=(0, None))
plot.legend(loc='center right', bbox_to_anchor=(1.45, 0.5), framealpha=1)
plot.figure.savefig("insert_sizes.png", format='png', dpi=1000, bbox_inches='tight')



print('finish')