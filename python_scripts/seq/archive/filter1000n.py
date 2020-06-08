import pandas as pd

columns = ['chromosome', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7', 'GC', 'col9', 'col10', 'col11', 'col12', 'N', 'col14', 'length']

df = pd.read_csv('hg19-canon-sort-nuc.bed', sep='\t', skiprows=1, header=None, names=columns)
print(df)
print(df.head())

df = df[df.length>999]
print(df)
print(df.head())

df = df[df.N==0]
print(df)
print(df.head())

df.to_csv('hg19-canon-sort-nuc-1000N.bed', sep='\t', index=False, header=False)