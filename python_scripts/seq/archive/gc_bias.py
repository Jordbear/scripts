#!/usr/bin/python3
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
sns.set_palette(sns.color_palette(['#d8874a', '#59aa63', '#c04f50', '#8571b8', '#92795e']))



files = glob.glob('*_gc.tsv')
print(files)
print('')

samples = [i.replace('_dmarked_gc.tsv', '') for i in files]
samples = [i.replace('_trimmed', '') for i in samples]
print(samples)
print('')



dfl = [pd.read_csv(i, sep='\t', skiprows=6) for i in files]

count = 0
for i in dfl:
    i['sample'] = samples[count]
    print(dfl[count])
    count+=1

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



fig = plt.figure(figsize=(7, 5))
ax1 = fig.add_subplot(1, 1, 1)
ax2 = ax1.twinx()

sns.barplot(x='GC', y='WINDOWS', color='#618cd9', data=dfe, ax=ax1)
ax1.set(xlim=(0, 100))
ax1.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax1.xaxis.set_major_formatter(ticker.ScalarFormatter())
ymax = int(total_windows/5)
rounded_ymax = round(ymax, 1-len(str(ymax)))
ax1.set(ylim=(0, rounded_ymax))
ax1.yaxis.set_major_locator(ticker.MultipleLocator(rounded_ymax/8))
ax1.yaxis.set_major_formatter(ticker.ScalarFormatter())
def commas(x, pos):
    return '{:,}'.format(int(x))
ax1.get_yaxis().set_major_formatter(plt.FuncFormatter(commas))
ax1.grid(b=True, axis='both')
ax1.yaxis.tick_right()
ax1.yaxis.set_label_position('right')
ax1.set(xlabel='GC percentage of windows', ylabel='Number of windows')

ax2.axes.axhline(1, color='grey', ls='--')
sns.lineplot(x='GC', y='NORMALIZED_COVERAGE', hue='sample', data=dfc, ax=ax2)
ax2.set(xlim=(0, 100))
ax2.set(ylim=(0, 2))
ax2.legend(loc='center right', bbox_to_anchor=(1.65, 0.5), framealpha=1).texts[0].set_text('Sample')
ax2.grid(False)
ax2.yaxis.tick_left()
ax2.yaxis.set_label_position('left')
ax2.set(xlabel='GC percentage of windows', ylabel='Normalised coverage')

plt.savefig('GC.png', format='png', dpi=500, bbox_inches='tight')



print('finished')