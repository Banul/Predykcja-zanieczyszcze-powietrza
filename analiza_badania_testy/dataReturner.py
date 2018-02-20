import sqlite3
import pandas as pd
import numpy as np


class dataReturner(object):
    def returnData(self):
        conn = sqlite3.connect('dane.db')
        dataFrame = pd.read_sql_query("SELECT * FROM resultcsv", conn)
        dataFrame = dataFrame.sort_values(by='date')

        dataFrame['PM10'] = dataFrame['PM10'].astype(float)
        dataFrame['cisnienie'] = dataFrame['cisnienie'].astype(str).astype(int)
        dataFrame['temperatura'] = dataFrame['temperatura'].astype(float)
        dataFrame['predkosc wiatru'] = dataFrame['predkosc wiatru'].astype(float)
        dataFrame['date'] = pd.to_datetime(dataFrame['date'])
        dataFrame['wilgotnosc'] = dataFrame['wilgotnosc'].astype(float)
        dataFrame['predkosc wiatru'] = dataFrame['predkosc wiatru'].astype(float)
        dataFrame['kierunek wiatru'] = dataFrame['kierunek wiatru'].astype(str)
        dataFrame['warunki pogodowe'] = dataFrame['warunki pogodowe'].astype(str)
        dataFrame ['PM25'] = dataFrame['PM25'].astype(float)

        mainDataFrame = dataFrame[
            ['PM25','PM10', 'temperatura', 'cisnienie', 'kierunek wiatru', 'warunki pogodowe', 'predkosc wiatru', 'wilgotnosc',
             'date']]
        mainDataFrame = mainDataFrame.dropna(axis=0, how='any')
        mainDataFrame = mainDataFrame.reset_index(drop=True)

        prevHumidity = mainDataFrame['wilgotnosc'][0:-1]
        prevTemperature = mainDataFrame['temperatura'][0:-1]
        prevPressure = mainDataFrame['cisnienie'][0:-1]
        prevWindSpeed = mainDataFrame['predkosc wiatru'][0:-1]
        prevPM10 = mainDataFrame['PM10'][0:-1]
        mainDataFrame = mainDataFrame[1:]
        mainDataFrame = mainDataFrame.reset_index(drop=True)
        mainDataFrame['prevHumidity'] = prevHumidity
        mainDataFrame['prevTemperature'] = prevTemperature
        mainDataFrame['prevPressure'] = prevPressure
        mainDataFrame['prevWindSpeed'] = prevWindSpeed
        mainDataFrame['rain'] = np.where((mainDataFrame['warunki pogodowe'].str.contains("Rain")) | (
        mainDataFrame['warunki pogodowe'].str.contains("Drizzle")) | (
                                         mainDataFrame['warunki pogodowe'].str.contains("Thunderstorm")) | (
                                         mainDataFrame['warunki pogodowe'].str.contains("Hail")), 1, 0)
        mainDataFrame['fog'] = np.where(mainDataFrame['warunki pogodowe'].str.contains("Fog"), 1, 0)
        mainDataFrame['mist'] = np.where(mainDataFrame['warunki pogodowe'].str.contains("Mist"), 1, 0)

        mainDataFrame['snow'] = np.where(mainDataFrame['warunki pogodowe'].str.contains("Snow"), 1, 0)
        mainDataFrame['partly_cloudy'] = np.where(mainDataFrame['warunki pogodowe'].str.contains("Partly Cloudy"), 1, 0)
        mainDataFrame['overcast'] = np.where(mainDataFrame['warunki pogodowe'].str.contains("Overcast"), 1, 0)
        mainDataFrame['clear'] = np.where(mainDataFrame['warunki pogodowe'].str.contains("Clear"), 1, 0)
        mainDataFrame['scattered_clouds'] = np.where(mainDataFrame['warunki pogodowe'].str.contains("Scattered Clouds"),
                                                     1, 0)
        mainDataFrame['mostly_cloudy'] = np.where(mainDataFrame['warunki pogodowe'].str.contains("Mostly Cloudy"), 1, 0)
        mainDataFrame['unknown'] = np.where(mainDataFrame['warunki pogodowe'].str.contains("Unknown"), 1, 0)
        mainDataFrame['onesColumn'] = np.ones((len(mainDataFrame), 1))

        mainDataFrame['west'] = np.where(mainDataFrame['kierunek wiatru'] == ("West"), 1, 0)
        mainDataFrame['wsw'] = np.where(mainDataFrame['kierunek wiatru'] == ("WSW"), 1, 0)
        mainDataFrame['wnw'] = np.where(mainDataFrame['kierunek wiatru'] == ("WNW"), 1, 0)
        mainDataFrame['variable'] = np.where(mainDataFrame['kierunek wiatru'] == ("Variable"), 1, 0)
        mainDataFrame['south'] = np.where(mainDataFrame['kierunek wiatru'] == ("South"), 1, 0)
        mainDataFrame['sw'] = np.where(mainDataFrame['kierunek wiatru'] == ("SW"), 1, 0)
        mainDataFrame['ssw'] = np.where(mainDataFrame['kierunek wiatru'] == ("SSW"), 1, 0)
        mainDataFrame['sse'] = np.where(mainDataFrame['kierunek wiatru'] == ("SSE"), 1, 0)
        mainDataFrame['se'] = np.where(mainDataFrame['kierunek wiatru'] == ("SE"), 1, 0)
        mainDataFrame['north'] = np.where(mainDataFrame['kierunek wiatru'] == ("North"), 1, 0)
        mainDataFrame['nw'] = np.where(mainDataFrame['kierunek wiatru'] == ("NW"), 1, 0)
        mainDataFrame['nnw'] = np.where(mainDataFrame['kierunek wiatru'] == ("NNW"), 1, 0)
        mainDataFrame['nne'] = np.where(mainDataFrame['kierunek wiatru'] == ("NNE"), 1, 0)
        mainDataFrame['ne'] = np.where(mainDataFrame['kierunek wiatru'] == ("NE"), 1, 0)
        mainDataFrame['east'] = np.where(mainDataFrame['kierunek wiatru'] == ("East"), 1, 0)
        mainDataFrame['ese'] = np.where(mainDataFrame['kierunek wiatru'] == ("ESE"), 1, 0)
        mainDataFrame['ene'] = np.where(mainDataFrame['kierunek wiatru'] == ("ENE"), 1, 0)

        mainDataFrame['godzina 0'] = np.where(mainDataFrame['date'].dt.hour == 0, 1, 0)
        mainDataFrame['godzina 1'] = np.where(mainDataFrame['date'].dt.hour == 1, 1, 0)
        mainDataFrame['godzina 2'] = np.where(mainDataFrame['date'].dt.hour == 2, 1, 0)
        mainDataFrame['godzina 3'] = np.where(mainDataFrame['date'].dt.hour == 3, 1, 0)
        mainDataFrame['godzina 4'] = np.where(mainDataFrame['date'].dt.hour == 4, 1, 0)
        mainDataFrame['godzina 5'] = np.where(mainDataFrame['date'].dt.hour == 5, 1, 0)
        mainDataFrame['godzina 6'] = np.where(mainDataFrame['date'].dt.hour == 6, 1, 0)
        mainDataFrame['godzina 7'] = np.where(mainDataFrame['date'].dt.hour == 7, 1, 0)
        mainDataFrame['godzina 8'] = np.where(mainDataFrame['date'].dt.hour == 8, 1, 0)
        mainDataFrame['godzina 9'] = np.where(mainDataFrame['date'].dt.hour == 9, 1, 0)
        mainDataFrame['godzina 10'] = np.where(mainDataFrame['date'].dt.hour == 10, 1, 0)
        mainDataFrame['godzina 11'] = np.where(mainDataFrame['date'].dt.hour == 11, 1, 0)
        mainDataFrame['godzina 12'] = np.where(mainDataFrame['date'].dt.hour == 12, 1, 0)
        mainDataFrame['godzina 13'] = np.where(mainDataFrame['date'].dt.hour == 13, 1, 0)
        mainDataFrame['godzina 14'] = np.where(mainDataFrame['date'].dt.hour == 14, 1, 0)
        mainDataFrame['godzina 15'] = np.where(mainDataFrame['date'].dt.hour == 15, 1, 0)
        mainDataFrame['godzina 16'] = np.where(mainDataFrame['date'].dt.hour == 16, 1, 0)
        mainDataFrame['godzina 17'] = np.where(mainDataFrame['date'].dt.hour == 17, 1, 0)
        mainDataFrame['godzina 18'] = np.where(mainDataFrame['date'].dt.hour == 18, 1, 0)
        mainDataFrame['godzina 19'] = np.where(mainDataFrame['date'].dt.hour == 19, 1, 0)
        mainDataFrame['godzina 20'] = np.where(mainDataFrame['date'].dt.hour == 20, 1, 0)
        mainDataFrame['godzina 21'] = np.where(mainDataFrame['date'].dt.hour == 21, 1, 0)
        mainDataFrame['godzina 22'] = np.where(mainDataFrame['date'].dt.hour == 22, 1, 0)
        mainDataFrame['godzina 23'] = np.where(mainDataFrame['date'].dt.hour == 23, 1, 0)

        mainDataFrame['styczen'] = np.where(mainDataFrame['date'].dt.month == 1, 1, 0)
        mainDataFrame['luty'] = np.where(mainDataFrame['date'].dt.month == 2, 1, 0)
        mainDataFrame['marzec'] = np.where(mainDataFrame['date'].dt.month == 3, 1, 0)
        mainDataFrame['kwiecien'] = np.where(mainDataFrame['date'].dt.month == 4, 1, 0)
        mainDataFrame['maj'] = np.where(mainDataFrame['date'].dt.month == 5, 1, 0)
        mainDataFrame['czerwiec'] = np.where(mainDataFrame['date'].dt.month == 6, 1, 0)
        mainDataFrame['lipiec'] = np.where(mainDataFrame['date'].dt.month == 7, 1, 0)
        mainDataFrame['sierpien'] = np.where(mainDataFrame['date'].dt.month == 8, 1, 0)
        mainDataFrame['wrzesien'] = np.where(mainDataFrame['date'].dt.month == 9, 1, 0)
        mainDataFrame['pazdziernik'] = np.where(mainDataFrame['date'].dt.month == 10, 1, 0)
        mainDataFrame['listopad'] = np.where(mainDataFrame['date'].dt.month == 11, 1, 0)
        mainDataFrame['grudzien'] = np.where(mainDataFrame['date'].dt.month == 12, 1, 0)
        mainDataFrame['prevPM10'] = prevPM10

        mainDataFrame = mainDataFrame.drop('warunki pogodowe', 1)
        mainDataFrame = mainDataFrame.drop('kierunek wiatru', 1)
        mainDataFrame = mainDataFrame.drop('date', 1)

        mainDataFrame = mainDataFrame[0:8092]

        return mainDataFrame