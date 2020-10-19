import re
import scipy
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 200)
import glob
from matplotlib import pyplot as plt
from matplotlib import ticker as ticker
import seaborn as sns
sns.set_style('white', {'axes.grid': True, 'xtick.bottom': True, 'ytick.left': True})
sns.set_context(rc={'patch.linewidth': '0.0'})
sns.set_palette(sns.color_palette('muted'))


dfl = [pd.read_csv('Book2.csv')]
print(dfl)
print('')


count=0
for i in dfl:
    print(dfl[count])
    fig = plt.figure(figsize=(11, 7))
    ax = fig.add_subplot(1, 1, 1)
    plot = sns.relplot(x='λ (%) CpG', y='BioA', ci=None, col='a', hue='Date', col_wrap=(1), kind='scatter', linewidth=0.2, height=3, aspect=1.05, s=30, data=dfl[count])


    for ax in plot.axes.flat:
        ax.set(xlim=(70, 100))
        ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
        ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
        
        ax.set(ylim=(70, 100))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
        ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
        
        # ax.grid(b=True, which='major')
        
        ax.plot([0, 100], [0, 100], linestyle='--', linewidth=1, zorder=0.9, color='grey')
        
    plot.set_titles("", pad=2)
    
    # plt.plot([0, 100], [0, 100], linestyle='--')
    # for ax in plot.axes.flat:
    #     for lb in ax.get_xticklabels():
    #         lb.set_rotation(90)

    # for p in plot.patches:
    #     if np.isnan(p.get_height())==False:
    #         if p.get_height()>=1:
    #             value_format = '{:#.3g}'
    #         else:
    #             value_format = '{:.2f}'
    #         plot.text(p.get_x()+p.get_width()/2, p.get_height()+ax.get_ylim()[1]/200, value_format.format(p.get_height()), fontsize=250/len(names), ha='center')

    # ax.set_ylim(top=ax.get_ylim()[1]*(1+(0.8/len(names))))

    for ax in plot.axes.flat:
        ax.set_xlabel('Sequencing')
        ax.set_ylabel('Bioanalyzer')
    # plot.set_xlabel('')
    # plot.legend(loc='center right', bbox_to_anchor=(1.11, 0.5), framealpha=1).remove()

    plt.subplots_adjust(wspace=0.15, hspace=0.15)

    # plt.savefig('piccy2.png', format='png', dpi=500, bbox_inches='tight')
    count+=1


dfl[0] = dfl[0].dropna()

correlation_matrix = np.corrcoef(dfl[0]['λ (%) CpG'].tolist(), dfl[0]['gel'].tolist())
correlation_xy = correlation_matrix[0,1]
r_squared = correlation_xy**2
print(r_squared)

slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(dfl[0]['λ (%) CpG'].tolist(), dfl[0]['gel'].tolist())
print(r_value**2)
print(std_err)

print(scipy.stats.linregress(dfl[0]['λ (%) CpG'].tolist(), dfl[0]['gel'].tolist()))


print('finished')
