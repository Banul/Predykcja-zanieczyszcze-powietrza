import pandas as pd
import sqlite3

#   Skrypt ktory pobiera dane dot. zanieczyszczen z pliku CSV, umieszcza je w bazie danych
#
#
#

conn = sqlite3.connect("dane.db")

dfNO2 = pd.read_csv('NO2-targowek.csv', sep=';')
dfNO2=dfNO2.drop(dfNO2.index[[0]])
dfNO2.columns = ['Date', 'NO2']

dfSO2 = pd.read_csv('SO2-targowek.csv',sep=';')
dfSO2=dfSO2.drop(dfSO2.index[[0]])
dfSO2.columns = ['Date', 'SO2']

dfO3 = pd.read_csv('targowek-ozon.csv',sep=';')
dfO3=dfO3.drop(dfO3.index[[0]])
dfO3.columns = ['Date', 'O3']

dfPM10 = pd.read_csv('PM10-targowek.csv',sep=';')
dfPM10=dfPM10.drop(dfPM10.index[[0]])
dfPM10.columns = ['Date', 'PM10']

dfPM25 = pd.read_csv('targowek-pm25.csv',sep=';')
dfPM25=dfPM25.drop(dfPM25.index[[0]])
dfPM25.columns = ['Date', 'PM25']

dfMerged = dfNO2.merge(dfSO2, on="Date").merge(dfO3, on="Date").merge(dfPM10, on="Date").merge(dfPM25,on="Date")

dfMerged.to_sql('zancsv', conn, if_exists='append')
