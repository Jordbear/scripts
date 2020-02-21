#import numpy
from matplotlib import pyplot as plt
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 200)
import seaborn as sns
sns.set_style('white', {'axes.grid': True, 'xtick.bottom': True, 'ytick.left': True})
sns.set_context(rc={'patch.linewidth': '0.0'})
sns.set_palette(sns.color_palette(['#ce0e2d', '#005cb9', '#f5a800', '#45c2b1', '#035c67']))



df = pd.read_excel('SLS1+SLS2_ENR_3.1.0_picard_22Mr - Copy.xlsx')
df = df[df['Repeat']!='y']
df['PCT_PF_DUPS'] = (1-df.PCT_PF_UQ_READS)*100
print(df)



plt.figure(figsize=(5,7))
plot = sns.barplot(x='Instrument', y='PCT_PF_DUPS', hue='Instrument', dodge=False, data=df)
#for lb in plot.get_xticklabels():
#    lb.set_rotation(90)
plot.set_xlabel('')
plot.set_title('% Duplicates')
plot.legend(loc='center right', bbox_to_anchor=(1.3, 0.5), framealpha=1)
#for p in plot.patches:
#    if numpy.isnan(p.get_height())==False:
#         plot.text(p.get_x()+p.get_width()/2, p.get_height()+0.1, '{:.2f}'.format(p.get_height()), ha='center')
plot.figure.savefig('Duplication.png', format='png', dpi=1000, bbox_inches='tight')



print('finish')