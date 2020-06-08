import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 200)
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.multivariate.manova import MANOVA


df = pd.read_csv('NFE data.csv')
df = df[df.instrument!='TUBE']
df = df[df.peak_frag_size!=0]
df = df[df.sample_conc_collected_qubit!=0]
print(df)
print('')
print(df.dtypes)
print('')



anova1 = ols('peak_frag_size ~ DNA', data=df).fit()
anova_table1 = sm.stats.anova_lm(anova1, typ=2)
print(anova_table1)
print('')


anova2 = ols('sample_conc_collected_qubit ~ DNA', data=df).fit()
anova_table2 = sm.stats.anova_lm(anova2, typ=2)
print(anova_table2)
print('')


#manova = MANOVA.from_formula('Peak_frag_size + Qubit_conc ~ Exp', data=df)
#print(manova.mv_test())
#print('')

