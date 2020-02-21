import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


inputfile = 'TransceiverData-2019-02-27_11-30-58.logoperations.txt'
outputfile = 'output.xlsx'


colnames = ['Column1', 'Column2', 'Column3', 'Column4', 'Column5', 'Column6', 'Column7', 'Column8', 'Column9', 'Column10', 'Column11', 'Column12', 'Column13', 'Column14', 'Column15', 'Column16', 'Column17', 'Column18', 'Column19', 'Column20', 'Column21', 'Column22', 'Column23', 'Column24', 'Column25', 'Column26', 'Column27', 'Column28', 'Column29', 'Column30', 'Column31', 'Column32']
df = pd.read_csv(inputfile, names=colnames, dtype=str)

guids = []
for i, row in df.iterrows():
    if 'Status:2' in str(df.loc[i, 'Column3']):
        guids.append(df.loc[i, 'Column1'])

dfshort = df[df['Column1'].isin(guids) == True]

status2 = []
for i in guids:
    for r, row in dfshort.iterrows():
        if 'Status:2' in str(dfshort.loc[r, 'Column3']) and i in dfshort.loc[r, 'Column1']:
            status2.append(dfshort.loc[r, 'Column4'])
        else:
            status2.append('NF')
status6 = []
for i in guids:
    for r, row in dfshort.iterrows():
        if 'Status:6' in str(dfshort.loc[r, 'Column3']) and i in dfshort.loc[r, 'Column1']:
            status6.append(dfshort.loc[r, 'Column4'])
        else:
            status6.append('NF')

status2x = [i[22:35] for i in status2]
status6x = [i[22:35] for i in status6]

dfoutput = pd.DataFrame({'Status:2': status2x, 'Status:6': status6x})

for r, rows in dfoutput.iterrows():
    if dfoutput.loc[r, 'Status:2'] == '' and dfoutput.loc[r, 'Status:6'] == '':
        dfoutput.drop(dfoutput.index(r), inplace=True)

dfoutput.to_excel('test.xlsx')

print(dfoutput)

print('Finish')