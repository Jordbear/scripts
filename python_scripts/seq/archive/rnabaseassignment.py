from matplotlib import pyplot as plt
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 200)
import glob
import seaborn as sns
sns.set_style('white', {'axes.grid': True, 'xtick.bottom': True, 'ytick.left': True})
sns.set_context(rc={'patch.linewidth': '0.0'})
sns.set_palette(sns.color_palette(['#035c67', '#ce0e2d', '#005cb9', '#f5a800', '#45c2b1']))


all_rsm = glob.glob('*.tabular')


names = []
for i in all_rsm:
        names.append(i)
namesx = [i.replace('.tabular', '') for i in names]
namesx = [i.replace('RnaMetrics', '') for i in namesx]
print(namesx)
print('')


dfm = (pd.read_csv(f, sep='\t', skiprows=6, nrows=1) for f in all_rsm)
dfm = pd.concat(dfm, axis=0)
print(dfm)
print('')

dfm = dfm[['PF_ALIGNED_BASES', 'RIBOSOMAL_BASES', 'CODING_BASES', 'UTR_BASES', 'INTRONIC_BASES', 'INTERGENIC_BASES']]
print(dfm)
print('')

dfm['RIBOSOMAL_BASES'] = dfm['RIBOSOMAL_BASES'].div(dfm['PF_ALIGNED_BASES'])*100
dfm['CODING_BASES'] = dfm['CODING_BASES'].div(dfm['PF_ALIGNED_BASES'])*100
dfm['UTR_BASES'] = dfm['UTR_BASES'].div(dfm['PF_ALIGNED_BASES'])*100
dfm['INTRONIC_BASES'] = dfm['INTRONIC_BASES'].div(dfm['PF_ALIGNED_BASES'])*100
dfm['INTERGENIC_BASES'] = dfm['INTERGENIC_BASES'].div(dfm['PF_ALIGNED_BASES'])*100
print(dfm)
print('')

dfm['Sample'] = namesx
print(dfm)
print('')

#dfm = dfm.set_index('Sample')
print(dfm)
print('')

#dfm = dfm.stack()
print(dfm)
print('')

#dfm = dfm.reset_index()
print(dfm)
print('')

#dfm.columns=['Sample', 'Metric', 'Percentage']
print(dfm)
print('')


plot1 = plt.bar(dfm['Sample'], dfm['RIBOSOMAL_BASES'])
plot2 = plt.bar(dfm['Sample'], dfm['CODING_BASES'], bottom=dfm['RIBOSOMAL_BASES'])
plot3 = plt.bar(dfm['Sample'], dfm['UTR_BASES'], bottom=dfm['RIBOSOMAL_BASES']+dfm['CODING_BASES'])
plot4 = plt.bar(dfm['Sample'], dfm['INTRONIC_BASES'], bottom=dfm['RIBOSOMAL_BASES']+dfm['CODING_BASES']+dfm['UTR_BASES'])
plot5 = plt.bar(dfm['Sample'], dfm['INTERGENIC_BASES'], bottom=dfm['RIBOSOMAL_BASES']+dfm['CODING_BASES']+dfm['UTR_BASES']+dfm['INTRONIC_BASES'])
plt.legend((plot5[0], plot4[0], plot3[0], plot2[0], plot1[0]), ('INTERGENIC_BASES', 'INTRONIC_BASES', 'UTR_BASES', 'CODING_BASES', 'RIBOSOMAL_BASES'), loc='center right', bbox_to_anchor=(1.45, 0.5), framealpha=1)
plt.title('Base Assignment')
plt.gca().xaxis.grid(False)
plt.ylabel('Percentage')
plt.savefig('rna_base_assignment.png', format='png', dpi=1000, bbox_inches='tight')



print('finish')