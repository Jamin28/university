import pandas
import csv,sqlite3

conn = sqlite3.connect('db.sqlite3')

# csv 文件路径
mv = pandas.read_csv('movie5.csv')

# movie为表名
mv.to_sql('movie',conn,if_exists='append',index=False)

print('ok')