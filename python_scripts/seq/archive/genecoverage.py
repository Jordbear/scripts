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


columns = ['Chromosome', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7', 'gc', 'col9', 'col10', 'col11', 'col12', 'col13', 'col14', 'col15', 'Mean Coverage Depth']

df = pd.read_csv('gene-coverage-badgc.tabular', sep='\t', header=None, names=columns)
print(df.head())

order = ['chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9', 'chr10', 'chr11', 'chr12', 'chr13', 'chr14', 'chr15', 'chr16', 'chr17', 'chr18', 'chr19', 'chr20', 'chr21', 'chr22', 'chrX', 'chrY']
cmap = 'coolwarm'
cmap2 = sns.diverging_palette(10, 255, s=90, l=40, n=df['gc'].nunique())

plot = sns.stripplot(x='Chromosome', y='Mean Coverage Depth', hue='gc', palette=cmap2, orient='v', jitter=0.3, size=1, order=order, data=df)
plot.set(ylim=(0, 15))
plot.set_xticklabels(plot.get_xticklabels(), rotation=90)
plot.get_legend().remove()

plot.figure.savefig('test-strip4.png', format='png', dpi=1000, bbox_inches='tight')