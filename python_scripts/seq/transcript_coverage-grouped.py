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



files = glob.glob('*_rnaseq.tsv')
print(files)
print('')


samples = [i.replace('_trimmed-crop75_dmarked_rnaseq.tsv', '') for i in files]
print(samples)
print('')



dfl = [pd.read_csv(f, sep='\t', skiprows=10) for f in files]
#print(dfl)
#print('')

count = 0
for i in dfl:
    i['sample']=samples[count]
    count+=1
#print(dfl)
#print('')

box = ['BO', 'OR', 'UM', 'OR', 'BO', 'UM', 'SI']
count = 0
for i in dfl:
    i['box'] = box[count]
    print(dfl[count])
    count+=1

pos = ['None', 'None', 'None', 'None', 'None', 'None', 'None']
count = 0
for i in dfl:
    i['pos'] = pos[count]
    print(dfl[count])
    count+=1

dfc = pd.concat(dfl, axis=0)
print(dfc)
print('')

dfc.columns=["Transcript position (5'-3' %)", 'Normalised coverage', 'Sample', 'box', 'pos']
print(dfc)
print('')



plot = sns.lineplot(x="Transcript position (5'-3' %)", y='Normalised coverage', hue='box', units='Sample', estimator=None, data=dfc)

plot.set(xlim=(0, 100))
plot.set(ylim=(0, None))
plot.axes.axhline(1, color='grey', ls='--', zorder=1)
plot.legend(framealpha=1)

plt.savefig("transcript_coverage-grouped_by_box.png", format='png', dpi=500, bbox_inches='tight')



print('finished')