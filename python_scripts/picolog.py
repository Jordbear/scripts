from matplotlib import pyplot as plt
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 200)
import glob
import seaborn as sns
sns.set_style('white', {'axes.grid': True, 'xtick.bottom': True, 'ytick.left': True})
sns.set_context(rc={'patch.linewidth': '0.0'})
sns.set_palette(sns.color_palette(['#ce0e2d', '#005cb9', '#f5a800', '#45c2b1', '#035c67']))

all_log = glob.glob('*.csv')


names = []
for i in all_log:
        names.append(i)
namesx = [i.replace('.csv', '') for i in names]
print(namesx)
print('')

dfm = list(pd.read_csv(f, sep=',', header=None, skiprows=1) for f in all_log)

samno = 0
for i in dfm:
    i['Sample']=namesx[samno]
    samno+=1

dfm = pd.concat(dfm, axis=0, sort=True)

dfm.columns=['Time (seconds)', 'Temperature (celsius)', 'Sample']



plot = sns.lineplot(x='Time (seconds)', y='Temperature (celsius)', hue='Sample', data=dfm)
plot.legend(loc='center right', bbox_to_anchor=(1.25, 0.5), framealpha=1)
plot.set(xlim=(0, None))

plot.figure.savefig('thermal_profile_OldVsNew_plusv4.png', format='png', dpi=1000, bbox_inches='tight')

print(dfm)
print('')
print(dfm.head())
print('')



print('Finish')