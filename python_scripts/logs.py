import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)
pd.set_option('display.expand_frame_repr', False)



inputfile = 'input.txt'
outputfile = 'output.xlsx'



colnames = ['Column1', 'Column2', 'Column3', 'Column4', 'Column5', 'Column6', 'Column7', 'Column8', 'Column9', 'Column10', 'Column11', 'Column12', 'Column13', 'Column14', 'Column15', 'Column16', 'Column17', 'Column18', 'Column19', 'Column20', 'Column21', 'Column22', 'Column23', 'Column24', 'Column25', 'Column26', 'Column27', 'Column28', 'Column29', 'Column30', 'Column31', 'Column32']
df = pd.read_csv(inputfile, names=colnames, dtype=str)


df98 = df[df['Column12'].str.contains('98}}') == True]

df65 = df[df['Column12'].str.contains('65}}') == True]


list98 = df98['Column2'].tolist()
#print("")
#print(list98)
list98x = ["{" + '"' + i[:11] + '"' + i[11:] for i in list98]
#print(list98x)

list65 = df65['Column2'].tolist()
#print("")
#print(list65)
list65x = ["{" + '"' + i[:11] + '"' + i[11:] for i in list65]
#print(list65x)


df98full = df[df['Column1'].isin(list98x) == True]
#print(df98full)

df65full = df[df['Column1'].isin(list65x) == True]
#print(df65full)


dfs = [df98full, df65full]
dfcombo = pd.concat(dfs)
#print(dfcombo)


dfcomboreduced = dfcombo.loc[:, ['Column3', 'Column4']]
dfcomboreduced.sort_index(inplace=True)
#print(dfcomboreduced)


dffinal = dfcomboreduced[dfcomboreduced.Column3 != 'Status:0']
#print(dffinal)
#dffinal.to_excel('stuff.xlsx')


dfs2 = dffinal[dffinal.Column3 == 'Status:2']
print(dfs2)

dfs6 = dffinal[dffinal.Column3 == 'Status:6']
print(dfs6)


list2 = dfs2['Column4'].tolist()
list2x = [i[22:35] for i in list2]
print(list2x)

list6 = dfs6['Column4'].tolist()
list6x = [i[22:35] for i in list6]
print(list6x)


dfoutput = pd.DataFrame({'Status 2': list2x, 'Status 6': list6x})
print(dfoutput)


dfoutput.to_excel(outputfile)


print("")
print("Finish")