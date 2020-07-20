from matplotlib import pyplot as plt
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 200)
import glob
import seaborn as sns
sns.set_style('white', {'axes.grid': True, 'xtick.bottom': True, 'ytick.left': True})
sns.set_context(rc={'patch.linewidth': '0.0'})
sns.set_palette(sns.color_palette(['#28215D', '#706F6F', '#DE6752', '#DC4B72']))



files = sorted(glob.glob('*.csv'))
print(files)
print('')

names = [i.replace('.csv', '') for i in files]
print(names)
print('')

dfl = [pd.read_csv(f, sep=',', skiprows=0, index_col=False) for f in files]

group = ['Cycler1', 'Cycler2']
count = 0
for i in dfl:
    i['sample'] = names[count]
    print(dfl[count])
    print('')
    i['group'] = group[count]
    print((dfl[count]).head())
    print('')
    dfl[count] = dfl[count].melt(id_vars=['Unnamed: 0', 'sample', 'group'])
    print(dfl[count])
    print('')
    count+=1

dfc = pd.concat(dfl, axis=0, sort=True)
print(head(dfc))
print('')


fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(1, 1, 1)
plot = sns.lineplot(x='time', y='value', hue='variable', units='sample', estimator=None, data=dfc)
handles, labels = plot.get_legend_handles_labels()
plot.legend(loc='center right', bbox_to_anchor=(1.2, 0.5), framealpha=1, title='Position', handles=handles[1:], labels=labels[1:])
plot.set(xlim=(0, None))
plot.set(xlabel='Time (s)', ylabel='Temperature (\u00B0C)')
plot.figure.savefig('plot.png', format='png', dpi=1000, bbox_inches='tight')



print('finished')