#!/usr/bin/python3
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 300)
import glob
from matplotlib import pyplot as plt
import seaborn as sns
sns.set_style('white', {'axes.grid': True, 'xtick.bottom': True, 'ytick.left': True})
sns.set_context(rc={'patch.linewidth': '0.0'})
sns.set_palette(sns.color_palette(['#ce0e2d', '#005cb9', '#f5a800', '#45c2b1', '#035c67']))


                                   
files = glob.glob('*inserts.tsv')
print(files)
print('')

samples = [i.replace('_dmarked_inserts.tsv', '') for i in files]
samples = [i.replace('_trimmed', '') for i in samples]
print(samples)
print('')



dfl = [pd.read_csv(f, sep='\t', skiprows=10, index_col=False) for f in files]
for i in dfl:
    print(i.head())

count=0
for i in dfl:
    if i.columns[0] == '## HISTOGRAM':
        dfl[count] = pd.read_csv(files[count], sep='\t', skiprows=11, index_col=False)
        dfl[count]['Reads'] = dfl[count]['All_Reads.fr_count']+dfl[count]['All_Reads.rf_count']
        dfl[count].drop(columns=['All_Reads.fr_count', 'All_Reads.rf_count'], inplace=True)
    else:
        dfl[count].rename(columns={'All_Reads.fr_count': 'Reads'}, inplace=True)
    count+=1

for i in dfl:
    print(i.head())

count = 0
for i in dfl:
    i['sample']=samples[count]
    print(i.head())
    count+=1

dfc = pd.concat(dfl, axis=0)
print(dfc)
print('')



fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(1, 1, 1)
plot = sns.lineplot(x='insert_size', y='Reads', hue='sample', data=dfc)
sns.despine()
plot.set(xlim=(0, 1250))
plot.set(ylim=(0, None))
plot.legend(loc='center right', bbox_to_anchor=(1.5, 0.5), framealpha=1).texts[0].set_text('Sample')
def commas(x, pos):
    return '{:,}'.format(int(x))
ax.get_yaxis().set_major_formatter(plt.FuncFormatter(commas))
plt.savefig('insert_size.png', format='png', dpi=500, bbox_inches='tight')



print('finished')