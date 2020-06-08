from matplotlib import pyplot as plt
from matplotlib import ticker as ticker
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 200)
import glob
import seaborn as sns
sns.set_style('white', {'axes.grid': True, 'xtick.bottom': True, 'ytick.left': True})
sns.set_context(rc={'patch.linewidth': '0.0'})
sns.set_palette(sns.color_palette(['#035c67', '#ce0e2d', '#005cb9', '#f5a800', '#45c2b1']))


files = glob.glob('*rnaseq.tsv')


samples = [i.replace('_trimmed-crop75_dmarked_rnaseq.tsv', '') for i in files]
print(samples)
print('')


dfm = [pd.read_csv(f, sep='\t', skiprows=6, nrows=1) for f in files]
dfc = pd.concat(dfm, axis=0)
print(dfc)
print('')

dfc = dfc[['PF_ALIGNED_BASES', 'RIBOSOMAL_BASES', 'CODING_BASES', 'UTR_BASES', 'INTRONIC_BASES', 'INTERGENIC_BASES']]
print(dfc)
print('')

dfc['RIBOSOMAL_BASES'] = dfc['RIBOSOMAL_BASES'].div(dfc['PF_ALIGNED_BASES'])*100
dfc['CODING_BASES'] = dfc['CODING_BASES'].div(dfc['PF_ALIGNED_BASES'])*100
dfc['UTR_BASES'] = dfc['UTR_BASES'].div(dfc['PF_ALIGNED_BASES'])*100
dfc['INTRONIC_BASES'] = dfc['INTRONIC_BASES'].div(dfc['PF_ALIGNED_BASES'])*100
dfc['INTERGENIC_BASES'] = dfc['INTERGENIC_BASES'].div(dfc['PF_ALIGNED_BASES'])*100
print(dfc)
print('')

dfc['sample'] = samples
print(dfc)
print('')

fig = plt.figure(figsize=(7,5))
ax = fig.add_subplot(1, 1, 1)
plot1 = plt.bar(dfc['sample'], dfc['RIBOSOMAL_BASES'])
plot2 = plt.bar(dfc['sample'], dfc['CODING_BASES'], bottom=dfc['RIBOSOMAL_BASES'])
plot3 = plt.bar(dfc['sample'], dfc['UTR_BASES'], bottom=dfc['RIBOSOMAL_BASES']+dfc['CODING_BASES'])
plot4 = plt.bar(dfc['sample'], dfc['INTRONIC_BASES'], bottom=dfc['RIBOSOMAL_BASES']+dfc['CODING_BASES']+dfc['UTR_BASES'])
plot5 = plt.bar(dfc['sample'], dfc['INTERGENIC_BASES'], bottom=dfc['RIBOSOMAL_BASES']+dfc['CODING_BASES']+dfc['UTR_BASES']+dfc['INTRONIC_BASES'])
plt.legend((plot5[0], plot4[0], plot3[0], plot2[0], plot1[0]), ('INTERGENIC_BASES', 'INTRONIC_BASES', 'UTR_BASES', 'CODING_BASES', 'RIBOSOMAL_BASES'), loc='center right', bbox_to_anchor=(1.4, 0.5), framealpha=1)
ax.set(ylim=(0, 100))
ax.yaxis.set_major_locator(ticker.MultipleLocator(20))
ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
plt.title('Base Assignment')
plt.xticks(rotation=90)
plt.gca().xaxis.grid(False)
plt.ylabel('Percentage')
plt.savefig('rna_base_assignment.png', format='png', dpi=500, bbox_inches='tight')



print('finished')