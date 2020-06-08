import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 200)
import glob



all_sal = glob.glob('*.tabular')


names = []
for i in all_sal:
    names.append(i)
names = [i.replace('.tabular', '') for i in names]
print(names)
print('')


dfm = [pd.read_csv(f, sep='\t') for f in all_sal]
count = 0
for i in dfm:
    print(names[count])
    count+=1
    print(i.head(5))
    print('')


count = 0
for i in dfm:
    TPM_over_one_tenth = 0
    TPM_over_one = 0
    for r, rows in i.iterrows():
        if i.loc[r, 'TPM'] > 0.1:
            TPM_over_one_tenth+=1
        if i.loc[r, 'TPM'] > 1:
            TPM_over_one+=1
    print(names[count])
    count+=1
    print('>0.1TPM =', TPM_over_one_tenth)
    print('>1TPM =', TPM_over_one)
    print('')



print('finish')