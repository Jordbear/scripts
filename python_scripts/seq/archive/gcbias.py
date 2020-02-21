from matplotlib import pyplot as plt
from matplotlib import ticker as ticker
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 200)
import glob
import seaborn as sns
sns.set_style('white', {'axes.grid': True, 'xtick.bottom': True, 'ytick.left': False})
sns.set_context(rc={'patch.linewidth': '0.0'})
sns.set_palette(sns.color_palette(['#ce0e2d', '#005cb9', '#f5a800', '#45c2b1', '#035c67']))



file_names = glob.glob('*.tabular')
print(file_names)
print('')

sample_names = [i.replace('..fastq.tabular', '') for i in file_names]
print(sample_names)
print('')

dfl = [pd.read_csv(i, sep='\t', skiprows=6) for i in file_names]
count=0
for i in dfl:
    print(dfl[count])
    count+=1
print('')

count = 0
for i in dfl:
    i['sample_name'] = sample_names[count]
    count+=1
count = 0
for i in dfl:
    print(dfl[count])
    count+=1
print('')

dfc = pd.concat(dfl, axis=0)
print(dfc)
print('')

dfe = dfl[0]
print(dfe)
print('')

total_windows = dfe['WINDOWS'].sum()
print(total_windows)
print('')

dfe['Proportion'] = dfe['WINDOWS']/total_windows
print(dfe)
print('')



fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
ax2 = ax1.twinx()


sns.barplot(x='GC', y='Proportion', color='#035c67', data=dfe, ax=ax1)
ax1.set(xlim=(0, 100))
ax1.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax1.xaxis.set_major_formatter(ticker.ScalarFormatter())
ax1.set(ylim=(0, 0.1))
ax1.yaxis.set_major_locator(ticker.MultipleLocator(0.0125))
ax1.yaxis.set_major_formatter(ticker.ScalarFormatter())
ax1.grid(b=True, axis='both')
ax1.yaxis.tick_right()
ax1.yaxis.set_label_position('right')
ax1.set(xlabel='GC percentage of windows', ylabel='Proportion of windows')


ax2.axes.axhline(1, color='grey', ls='--')
sns.lineplot(x='GC', y='NORMALIZED_COVERAGE', hue='sample_name', data=dfc, ax=ax2)
ax2.set(xlim=(0, 100))
ax2.set(ylim=(0, 2))
ax2.legend(loc='center right', bbox_to_anchor=(1.7, 0.5), framealpha=1).texts[0].set_text('Sample')
ax2.grid(False)
ax2.yaxis.tick_left()
ax2.yaxis.set_label_position('left')
ax2.set(xlabel='GC percentage of windows', ylabel='Normalised coverage')


plt.savefig('test.png', format='png', dpi=1000, bbox_inches='tight')



print('finish')