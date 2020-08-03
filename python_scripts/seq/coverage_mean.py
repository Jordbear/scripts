import re
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



interval='synthetic_N5mCNN'


files = sorted(glob.glob('*_wgs-'+interval+'.tsv'))
print(files)
print('')

samples = [i.replace('_wgs-'+interval+'.tsv', '') for i in files]
print(samples)
print('')

# groups = [re.sub(r'_L.*_mCtoT_all.stats', '', i) for i in files]
# print(groups)
# print('')


dfl = [pd.read_csv(f, sep='\t', skiprows=6, nrows=1) for f in files]
print(dfl)
print('')

count = 0
for i in dfl:
    i['sample'] = samples[count]
    # i['group'] = groups[count]
    print(dfl[count])
    count+=1

dfc = pd.concat(dfl, axis=0)
print(dfc)
print('')

dfc.to_csv('coverage_summary-'+interval+'.tsv', sep='\t')

means=dfc['MEAN_COVERAGE'].tolist()
stdevs=dfc['SD_COVERAGE'].tolist()


fig = plt.figure(figsize=(11, 7))
ax = fig.add_subplot(1, 1, 1)
plot = sns.barplot(x='sample', y='MEAN_COVERAGE', hue='sample', units='sample', dodge=False, ci='sd', data=dfc)

plt.errorbar(x=samples, y=means, yerr=stdevs, fmt='none', ecolor='black', elinewidth=1.5, capsize=5, capthick=1.5)
plot.set_ylim(0, None)

for lb in plot.get_xticklabels():
    lb.set_rotation(90)
# for p in plot.patches:
#     if np.isnan(p.get_height())==False:
#         if p.get_height()>=1:
#             value_format = '{:#.3g}'
#         else:
#             value_format = '{:.2f}'
#         plot.text(p.get_x()+p.get_width()/2, p.get_height()+ax.get_ylim()[1]/200, value_format.format(p.get_height()), fontsize=250/len(names), ha='center')

# ax.set_ylim(top=ax.get_ylim()[1]*(1+(0.8/len(names))))

plot.set_xlabel('')
plot.legend(loc='center right', bbox_to_anchor=(1.11, 0.5), framealpha=1).remove()

plt.savefig('coverage-'+interval+'.png', format='png', dpi=500, bbox_inches='tight')



print('finished')