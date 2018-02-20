import sqlite3
import pandas as pd

# Skrypt tworzacy tabele resultcsv, ktora zawiera polaczone dane pogodowe oraz te dot. zanieczyszczen


conn = sqlite3.connect("dane.db")

dataFramePogoda = pd.read_sql(sql = "select * from pogoda", con =conn)
dataFramePogoda.drop_duplicates(subset='date', inplace=True)
dataFramePogoda.sort_values(by='date', ascending=True)

dataFrameZanieczyszczenia = pd.read_sql(sql = "select * from zancsv", con=conn)
dataFrameZanieczyszczenia.columns = ['index','date','NO2','SO2','O3','PM10','PM25']
dataFrameZanieczyszczenia.drop_duplicates(subset='date',inplace=True)
dataFrameZanieczyszczenia = dataFrameZanieczyszczenia.sort_values(by='date', ascending=True)

mergedDataFrame = pd.merge(dataFramePogoda, dataFrameZanieczyszczenia, how = 'inner', on='date')
mergedDataFrame.to_sql('resultcsv',conn,if_exists='append')
