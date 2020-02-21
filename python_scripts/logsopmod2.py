import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', -1)


inputfile = 'input.txt'
outputfile = 'output.xlsx'


colnames = ['Column1', 'Column2', 'Column3', 'Column4', 'Column5', 'Column6', 'Column7', 'Column8', 'Column9', 'Column10', 'Column11', 'Column12', 'Column13', 'Column14', 'Column15', 'Column16', 'Column17', 'Column18', 'Column19', 'Column20', 'Column21', 'Column22', 'Column23', 'Column24', 'Column25', 'Column26', 'Column27', 'Column28', 'Column29', 'Column30', 'Column31', 'Column32']
df = pd.read_csv(inputfile, names=colnames, dtype=str)

guids = []
for i, row in df.iterrows():
    if 'Status:2' in str(df.loc[i, 'Column3']):
        guids.append(df.loc[i, 'Column1'])

dfshort = df[df['Column1'].isin(guids) == True]

dfoutput = pd.DataFrame({'Status:2': '', 'Status:6': ''}, index=guids)

for r, row in dfshort.iterrows():
    if dfshort.loc[r, 'Column3'] == 'Status:2':
        dfoutput.at[dfshort.loc[r, 'Column1'], 'Status:2'] = dfshort.loc[r, 'Column4']
    elif dfshort.loc[r, 'Column3'] == 'Status:6':
        dfoutput.at[dfshort.loc[r, 'Column1'], 'Status:6'] = dfshort.loc[r, 'Column4']

dfoutput.replace(r'Timestamp:"2019-02-28T', '', regex=True, inplace=True)
dfoutput.replace(r'Timestamp:"2019-02-27T', '', regex=True, inplace=True)
dfoutput.replace(r'"}', '', regex=True, inplace=True)

dfoutput.to_excel(outputfile)

print(dfoutput)

print('Finish')