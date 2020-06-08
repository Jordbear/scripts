from matplotlib import pyplot as plt
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 200)
import seaborn as sns
sns.set_style('white', {'axes.grid': True, 'xtick.bottom': True, 'ytick.left': True})
sns.set_context(rc={'patch.linewidth': '0.0'})
sns.set_palette(sns.color_palette(['#035c67', '#ce0e2d', '#005cb9', '#f5a800', '#45c2b1', '#678990', '#d7736a', '#5088c9']))



df = pd.read_excel('Copy of Failure modes.xlsx')
print(df)



plt.rcParams['font.family']='Century Gothic'
#plt.rcParams['text.color']='#035c67'
#plt.rcParams['axes.edgecolor']='#035c67'
#plt.rcParams['axes.labelcolor']='#035c67'
#plt.rcParams['xtick.color']='#035c67'
#plt.rcParams['ytick.color']='#035c67'
#plt.rcParams['grid.color']='#bbcacd'


plot1 = plt.bar(df['Script iteration'], df['Blocked Operation'])
plot2 = plt.bar(df['Script iteration'], df['Dispense Failure'], bottom=df['Blocked Operation'])
plot3 = plt.bar(df['Script iteration'], df['Unwanted Merge'], bottom=df['Blocked Operation']+df['Dispense Failure'])
plot4 = plt.bar(df['Script iteration'], df['Reagent Mobility'], bottom=df['Blocked Operation']+df['Dispense Failure']+df['Unwanted Merge'])
plot5 = plt.bar(df['Script iteration'], df['Wash Error'], bottom=df['Blocked Operation']+df['Dispense Failure']+df['Unwanted Merge']+df['Reagent Mobility'])
plot6 = plt.bar(df['Script iteration'], df['None'], bottom=df['Blocked Operation']+df['Dispense Failure']+df['Unwanted Merge']+df['Reagent Mobility']+df['Wash Error'])
plt.legend((plot1[0], plot2[0], plot3[0], plot4[0], plot5[0], plot6[0]), ('Blocked Operation', 'Dispense Failure', 'Unwanted Merge', 'Reagent Mobility', 'Wash Error', 'None'), fontsize=9, loc='center right', bbox_to_anchor=(1.4, 0.5), framealpha=1)
plt.title('Failure Mode Analysis')
plt.ylabel('Runs')
plt.gca().xaxis.grid(False)
plt.xticks(fontsize=9)
plt.yticks(fontsize=9)
plt.savefig('Failure Mode over Iterations on Black.png', format='png', dpi=1000, bbox_inches='tight')



print('finish')