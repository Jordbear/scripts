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



files = glob.glob('*alignment.tsv')



samples = [i.replace('_dmarked_alignment.tsv', '') for i in files]
print(samples)
print('')


colnames = ['metric1', 'TOTAL_READS', 'metric3', 'metric4', 'metric5', 'metric6', 'PCT_PF_READS_ALIGNED', 'metric8', 'metric9', 'metric10', 'metric11', 'metric12', 'PF_MISMATCH_RATE', 'PF_HQ_ERROR_RATE', 'PF_INDEL_RATE', 'metric16', 'metric17', 'metric18', 'metric19', 'metric20', 'metric21', 'metric22', 'PCT_CHIMERAS', 'PCT_ADAPTER', 'metric25', 'metric26', 'metric27']
unwanted = []
for i in colnames:
    if 'metric' in i:
        unwanted.append(i)
print(unwanted)
print('')

dfl = [pd.read_csv(f, sep='\t', skiprows=9, names=colnames) for f in files]
dfc = pd.concat(dfl, axis=0)
print(dfc)
print('')

dfc.drop(unwanted, axis=1, inplace=True)
print(dfc)
print('')

dfc.PCT_PF_READS_ALIGNED = 1-dfc.PCT_PF_READS_ALIGNED
dfc = dfc.rename(columns={'PCT_PF_READS_ALIGNED': 'PCT_PF_READS_UNALIGNED'})
print(dfc)
print('')

dfc[['PCT_PF_READS_UNALIGNED', 'PF_MISMATCH_RATE', 'PF_HQ_ERROR_RATE', 'PF_INDEL_RATE', 'PCT_CHIMERAS', 'PCT_ADAPTER']]*=100
print(dfc)
print('')

dfc['sample']=samples
print(dfc)
print('')

dfc.to_csv('alignment_summary.tsv', sep='\t')


fig = plt.figure(figsize=(11, 7))
ax = fig.add_subplot(1, 1, 1)
plot = sns.barplot(x='sample', y='TOTAL_READS', hue='sample', dodge=False, data=dfc)

for lb in plot.get_xticklabels():
    lb.set_rotation(90)   

for p in plot.patches:
    if np.isnan(p.get_height())==False:
         plot.text(p.get_x()+p.get_width()/2, ax.get_ylim()[1]/70, '{:,.0f}'.format(p.get_height()), fontsize=10, rotation=90, ha='center', va='bottom')

ax.ticklabel_format(style='plain', axis='y')

def commas(x, pos):
    return '{:,}'.format(int(x))
ax.get_yaxis().set_major_formatter(plt.FuncFormatter(commas))

plot.set_xlabel('')
plot.legend_.remove()

plt.savefig('yield.png', format='png', dpi=500, bbox_inches='tight')


fig = plt.figure(figsize=(11, 7))
ax = fig.add_subplot(1, 1, 1)
plot = sns.barplot(x='sample', y='PCT_PF_READS_UNALIGNED', hue='sample', dodge=False, data=dfc)

for lb in plot.get_xticklabels():
    lb.set_rotation(90)   

for p in plot.patches:
    if np.isnan(p.get_height())==False:
         plot.text(p.get_x()+p.get_width()/2, p.get_height()+ax.get_ylim()[1]/200, '{:.2f}'.format(p.get_height()), fontsize=10, ha='center')

plot.set_xlabel('')
plot.legend_.remove()

plt.savefig('unaligned.png', format='png', dpi=500, bbox_inches='tight')


fig = plt.figure(figsize=(11, 7))
ax = fig.add_subplot(1, 1, 1)
plot = sns.barplot(x='sample', y='PF_MISMATCH_RATE', hue='sample', dodge=False, data=dfc)

for lb in plot.get_xticklabels():
    lb.set_rotation(90)   

for p in plot.patches:
    if np.isnan(p.get_height())==False:
         plot.text(p.get_x()+p.get_width()/2, p.get_height()+ax.get_ylim()[1]/200, '{:.2f}'.format(p.get_height()), fontsize=10, ha='center')

plot.set_xlabel('')
plot.legend_.remove()

plt.savefig('mismatched.png', format='png', dpi=500, bbox_inches='tight')


fig = plt.figure(figsize=(11, 7))
ax = fig.add_subplot(1, 1, 1)
plot = sns.barplot(x='sample', y='PF_HQ_ERROR_RATE', hue='sample', dodge=False, data=dfc)

for lb in plot.get_xticklabels():
    lb.set_rotation(90)   

for p in plot.patches:
    if np.isnan(p.get_height())==False:
         plot.text(p.get_x()+p.get_width()/2, p.get_height()+ax.get_ylim()[1]/200, '{:.2f}'.format(p.get_height()), fontsize=10, ha='center')

plot.set_xlabel('')
plot.legend_.remove()

plt.savefig('errors.png', format='png', dpi=500, bbox_inches='tight')


fig = plt.figure(figsize=(11, 7))
ax = fig.add_subplot(1, 1, 1)
plot = sns.barplot(x='sample', y='PF_INDEL_RATE', hue='sample', dodge=False, data=dfc)

for lb in plot.get_xticklabels():
    lb.set_rotation(90)   

for p in plot.patches:
    if np.isnan(p.get_height())==False:
         plot.text(p.get_x()+p.get_width()/2, p.get_height()+ax.get_ylim()[1]/200, '{:.2f}'.format(p.get_height()), fontsize=10, ha='center')

plot.set_xlabel('')
plot.legend_.remove()

plt.savefig('indels.png', format='png', dpi=500, bbox_inches='tight')


fig = plt.figure(figsize=(11, 7))
ax = fig.add_subplot(1, 1, 1)
plot = sns.barplot(x='sample', y='PCT_CHIMERAS', hue='sample', dodge=False, data=dfc)

for lb in plot.get_xticklabels():
    lb.set_rotation(90)   

for p in plot.patches:
    if np.isnan(p.get_height())==False:
         plot.text(p.get_x()+p.get_width()/2, p.get_height()+ax.get_ylim()[1]/200, '{:.2f}'.format(p.get_height()), fontsize=10, ha='center')

plot.set_xlabel('')
plot.legend_.remove()

plt.savefig('chimeras.png', format='png', dpi=500, bbox_inches='tight')


fig = plt.figure(figsize=(11, 7))
ax = fig.add_subplot(1, 1, 1)
plot = sns.barplot(x='sample', y='PCT_ADAPTER', hue='sample', dodge=False, data=dfc)

for lb in plot.get_xticklabels():
    lb.set_rotation(90)   

for p in plot.patches:
    if np.isnan(p.get_height())==False:
         plot.text(p.get_x()+p.get_width()/2, p.get_height()+ax.get_ylim()[1]/200, '{:.2f}'.format(p.get_height()), fontsize=10, ha='center')

plot.set_xlabel('')
plot.legend_.remove()

plt.savefig('adapter.png', format='png', dpi=500, bbox_inches='tight')





print('finished')