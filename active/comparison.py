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


df = pd.read_csv('/Users/jordanbrown/Downloads/Pic-Borane Results (1).csv')
print(df)
print('')

fig = plt.figure(figsize=(11, 7))
ax = fig.add_subplot(1, 1, 1)
plot = sns.stripplot(data=df, x="Sequencing date", y="λ (%) CpG", hue='Baseline', jitter=0.15)
plot.legend(loc='center right', bbox_to_anchor=(1.25, 0.5), framealpha=1).set_title('Baseline')
plot.yaxis.set_major_locator(ticker.MultipleLocator(5))
plot.yaxis.set_major_formatter(ticker.ScalarFormatter())
plot.set_xticklabels(plot.get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor', size=14)
plot.set(ylim=(None, 101))
plot.set_yticklabels(plot.get_yticks(), size=14)
ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
plot.set_xlabel('')
plot.set_ylabel('Lambda conversion (%)', size=16)
plt.savefig('conversion_time.png', format='png', dpi=500, bbox_inches='tight')


fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(1, 1, 1)
plot = sns.scatterplot(data=df, x="λ (%) CpG", y="Gel", hue='Sequencing date')
ax.set(xlim=(70, 100))
ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
ax.set(ylim=(70, 100))
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
ax.plot([0, 100], [0, 100], linestyle='--', linewidth=1, zorder=0.9, color='grey')
plot.legend(framealpha=1)
plt.savefig('conversion_comparison.png', format='png', dpi=500, bbox_inches='tight')


# df2 = df[df['λ (%) CpG'] >= 95]
# df2 = df2[df2['2kb (%) CpG'] <= 0.5]

fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(1, 1, 1)
plot = sns.scatterplot(data=df, x="λ (%) CpG", y="2kb (%) CpG", hue='Baseline')
plot.legend(framealpha=1)
ax.set(xlim=(90, 100))
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
ax.set(ylim=(0, 1))
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
plt.savefig('conversion_ratio.png', format='png', dpi=500, bbox_inches='tight')




import sys
sys.exit()



fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(1, 1, 1)
plot1 = sns.stripplot(x='Sequencing date', y='λ (%) CpG', hue='Sequencing date', jitter=0.2, linewidth=0.5, edgecolor='white', size=10, data=dfl[0])
plot1.legend(loc='center right', bbox_to_anchor=(1.11, 0.5), framealpha=1).remove()
plot1.set(ylim=(None, 101))
plot1.yaxis.set_major_locator(ticker.MultipleLocator(5))
plot1.yaxis.set_major_formatter(ticker.ScalarFormatter())
plot1.set_xticklabels(plot1.get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor', size=14)
plot1.set_yticklabels(plot1.get_yticks(), size=14)
ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
plot1.set_xlabel('')
plot1.set_ylabel('Conversion (%)', size=16)
plt.savefig('conversion_time1.png', format='png', dpi=500, bbox_inches='tight')


dfl[0]['a'] = 'a'

count=0
for i in dfl:
    print(dfl[count])
    fig = plt.figure(figsize=(11, 7))
    ax = fig.add_subplot(1, 1, 1)
    plot = sns.relplot(x='Sequencing date', y='λ (%) CpG', ci=None, col='a', hue='Sequencing date', col_wrap=(1), kind='scatter', linewidth=0.2, x_jitter=100000, height=3, aspect=1.5, s=30, legend=False, data=dfl[count])


    for ax in plot.axes.flat:
        # ax.set(xlim=(70, 100))
        # ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
        # ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
        
        ax.set(ylim=(None, 101))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
        ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
        
    #     # ax.grid(b=True, which='major')
        
    #     ax.plot([0, 100], [0, 100], linestyle='--', linewidth=1, zorder=0.9, color='grey')
        
    plot.set_titles("", pad=2)
    
    # plt.plot([0, 100], [0, 100], linestyle='--')
    
    for ax in plot.axes.flat:
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor')
        # for lb in ax.get_xticklabels():
        #     lb.set_xticklabels(plot.get_xticklabels(), rotation=90, ha='right')

    # for p in plot.patches:
    #     if np.isnan(p.get_height())==False:
    #         if p.get_height()>=1:
    #             value_format = '{:#.3g}'
    #         else:
    #             value_format = '{:.2f}'
    #         plot.text(p.get_x()+p.get_width()/2, p.get_height()+ax.get_ylim()[1]/200, value_format.format(p.get_height()), fontsize=250/len(names), ha='center')

    # ax.set_ylim(top=ax.get_ylim()[1]*(1+(0.8/len(names))))

    for ax in plot.axes.flat:
        ax.set_xlabel('')
        ax.set_ylabel('Conversion')
    # plot.set_xlabel('')
    # plot.axes.legend(loc='center right', bbox_to_anchor=(1.11, 0.5), framealpha=1).remove()

    plt.subplots_adjust(wspace=0.15, hspace=0.15)

    plt.savefig('conversion_time.png', format='png', dpi=500, bbox_inches='tight')
    count+=1


dfl[0] = dfl[0].dropna()

correlation_matrix = np.corrcoef(dfl[0]['λ (%) CpG'].tolist(), dfl[0]['Gel'].tolist())
correlation_xy = correlation_matrix[0,1]
r_squared = correlation_xy**2
print(r_squared)

slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(dfl[0]['λ (%) CpG'].tolist(), dfl[0]['Gel'].tolist())
print(r_value**2)
print(std_err)

print(scipy.stats.linregress(dfl[0]['λ (%) CpG'].tolist(), dfl[0]['Gel'].tolist()))


print('finished')
