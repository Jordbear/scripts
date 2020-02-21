from matplotlib import pyplot as plt
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 200)
import seaborn as sns
sns.set_style('white', {'axes.grid': True, 'xtick.bottom': True, 'ytick.left': True})
sns.set_context(rc={'patch.linewidth': '0.0'})
sns.set_palette(sns.color_palette(['#ce0e2d', '#005cb9', '#f5a800', '#45c2b1', '#035c67']))



df = pd.read_csv('NFE data 2.csv')
df = df[df.instrument!='TUBE']
df = df[df.peak_frag_size!=0]
df = df[df.sample_conc_collected_qubit!=0]
df = df[df.sample_conc_collected_qubit<=7]
print(df)
print(df.dtypes)



#plot = sns.FacetGrid(df, col='DNA', hue='Position on chip')
#plot = (plot.map(plt.scatter, 'Peak frag size (bp)', 'Qubit conc (ng/ul)').add_legend())

#plot.savefig('HD Colibri libraries DNA facet.png', format='png', dpi=1000, bbox_inches='tight')



plot = sns.scatterplot(x='input_peak_frag_size', y='input_DNA_conc', hue='sample_conc_collected_qubit', size='sample_conc_collected_qubit', data=df)
plot.legend(loc='center right', bbox_to_anchor=(1.55, 0.5), framealpha=1)
plot.set(ylim=(0, None))
sns.despine()

#plot.figure.savefig('input3.png', format='png', dpi=1000, bbox_inches='tight')



#plot = sns.scatterplot(x='input_peak_frag_size', y='input_DNA_conc', data=df)
#plot.legend(framealpha=1)
#plot.set(ylim=(0, None))
#plot.set(xlim=(0, None))
#sns.despine()

#plot.figure.savefig('correlation.png', format='png', dpi=1000, bbox_inches='tight')

print(df['input_DNA_conc'].corr(df['sample_conc_collected_qubit']))