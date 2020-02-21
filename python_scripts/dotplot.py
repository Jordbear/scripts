import pandas
pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_rows', None)
pandas.set_option('display.width', 1000)





data = pandas.read_csv('Sizes and Speeds.csv', na_values = ['-'])
print(data)


