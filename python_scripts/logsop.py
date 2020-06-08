import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


inputfile = 'input.txt'
outputfile = 'output.xlsx'


colnames = ['Column1', 'Column2', 'Column3', 'Column4', 'Column5', 'Column6', 'Column7', 'Column8', 'Column9', 'Column10', 'Column11', 'Column12', 'Column13', 'Column14', 'Column15', 'Column16', 'Column17', 'Column18', 'Column19', 'Column20', 'Column21', 'Column22', 'Column23', 'Column24', 'Column25', 'Column26', 'Column27', 'Column28', 'Column29', 'Column30', 'Column31', 'Column32']
df = pd.read_csv(inputfile, names=colnames, dtype=str)

guidlist = []
for i, row in df.iterrows():
    if '\": 98}}"}' in str(df.loc[i, 'Column12']) or '\": 65}}"}' in str(df.loc[i, 'Column12']):
        guidlist.append(df.loc[i, 'Column2'])

guidlistx = ["{" + '"' + i[:11] + '"' + i[11:] for i in guidlist]

dfshort = df[df['Column1'].isin(guidlistx) == True]

list2 = []
for i, row in dfshort.iterrows():
    if 'Status:2' in str(dfshort.loc[i, 'Column3']):
        list2.append(df.loc[i, 'Column4'])
list6 = []
for i, row in dfshort.iterrows():
    if 'Status:6' in str(dfshort.loc[i, 'Column3']):
        list6.append(df.loc[i, 'Column4'])

list2x = [i[22:35] for i in list2]
list6x = [i[22:35] for i in list6]

dfoutput = pd.DataFrame({'Status:2': list2x, 'Status:6': list6x})

dfoutput.to_excel(outputfile)

print(dfoutput)

print('Finish')