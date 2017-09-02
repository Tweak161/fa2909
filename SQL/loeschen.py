import pandas as pd
csv_file = '/media/thomas/3A7AB40B7AB3C245/EigeneDateien/Programmieren/Python/Forschungsarbeit.git/SQL/iris.csv'
df = pd.read_csv(csv_file)
saved_column = df['sepal_lengtha']
print(saved_column)
#with open('/media/thomas/3A7AB40B7AB3C245/EigeneDateien/Programmieren/Python/Forschungsarbeit.git/SQL/iris.csv', 'r') as csvfile:
#	spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#	for index, row in enumerate(spamreader):
#		print('new row: ')
#		print(row)	
