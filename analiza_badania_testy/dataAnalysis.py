#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sqlite3
import pandas as pd
from scipy.stats.stats import pearsonr
import numpy as np
import matplotlib.pyplot as plt
conn = sqlite3.connect('dane.db')

#
#Skrypt który został wykorzystany do przeprowadzenia analizy danych (rozdział 4 w pracy).
#Używałem pythona 2.7.13
#
#

wiosnaPocz = '21-03-2016'
wiosnaKon = '21-06-2016'
latoPocz = '22-06-2016'
latoKon = '22-09-2016'
jesienPocz = '23-09-2016'
jesienKon = '22-12-2016'
zimaPocz = '23-12-2016'
zimaKon = '20-03-2016'

dataFrame = pd.read_sql_query("SELECT * FROM resultcsv", conn)
dataFrame = dataFrame.sort_values(by='date')

dataFrame['cisnienie'] = dataFrame['cisnienie'].astype(str).astype(int)
dataFrame['PM10'] = dataFrame['PM10'].astype(float)
dataFrame['PM25'] = dataFrame['PM25'].astype(float)
dataFrame['temperatura'] = dataFrame['temperatura'].astype(float)
dataFrame['predkosc wiatru'] = dataFrame['predkosc wiatru'].astype(float)
dataFrame['date'] = pd.to_datetime(dataFrame['date'])
dataFrame ['wilgotnosc'] = dataFrame['wilgotnosc'].astype(float)
dataFrame ['predkosc wiatru'] = dataFrame['predkosc wiatru'].astype(float)
dataFrame ['kierunek wiatru'] = dataFrame['kierunek wiatru'].astype(str)
dataFrame ['warunki pogodowe'] = dataFrame['warunki pogodowe'].astype(str)


PM10 = dataFrame ['PM10']
cisn = dataFrame['cisnienie']
PM25 = dataFrame ['PM25']
temp = dataFrame ['temperatura']
predk = dataFrame ['predkosc wiatru']
date = dataFrame['date']
wilgotnosc = dataFrame['wilgotnosc']
windSpeed = dataFrame ['predkosc wiatru']
weatherCond = dataFrame ['warunki pogodowe']
windDirNames = set(dataFrame['kierunek wiatru'])
weatherCondNames = ['fog', 'snow', 'rain', 'mist', 'partly cloudy', 'overcast', 'clear', 'scattered clouds', 'mostly cloudy']

percentiles = ['5','25','50','75','95']

dictionaryForWindDirection = {listName:[] for listName in windDirNames }
dictionaryForWindDirectionStats = {listName:[] for listName in windDirNames }
dictionaryForWindDirectionPercentiles = {listName:[] for listName in percentiles }

###################################### LICZENIE KORELACJI ######################################################

dataFrameCisnPM = dataFrame[['cisnienie','PM10']].copy()
dataFrameCisnPM = dataFrameCisnPM.dropna(axis = 0, how ='any')

dataFramePM10PM25 = dataFrame[['PM10','PM25']].copy()
dataFramePM10PM25 = dataFramePM10PM25.dropna(axis = 0, how='any')

dataFrametempPM10 = dataFrame[['temperatura','PM10']].copy()
dataFrametempPM10 = dataFrametempPM10.dropna(axis = 0, how = 'any')

dataFramePredkPM10 = dataFrame[['predkosc wiatru','PM10']]
dataFramePredkPM10 = dataFramePredkPM10.dropna(axis = 0, how='any')
dataFramePredkPM10 = dataFramePredkPM10.reset_index(drop=True)


dataFrameDatePM10 = dataFrame[['date','PM10']]
dataFrameDatePM10 = dataFrameDatePM10.dropna(axis=0, how='any')
dataFrameDatePM10 = dataFrameDatePM10.reset_index(drop=True)

dataFrameWeatherCondPM10 = dataFrame[['date','warunki pogodowe','PM10']]
dataFrameWeatherCondPM10 = dataFrameWeatherCondPM10.dropna(axis = 0, how = 'any')
dataFrameWeatherCondPM10 = dataFrameWeatherCondPM10.reset_index(drop=True)

dataFrameWeatherCondPM10Zima = dataFrameWeatherCondPM10.loc[(dataFrameWeatherCondPM10['date'] >= zimaPocz) | (dataFrameWeatherCondPM10['date'] <= zimaKon)]
dataFrameWeatherCondPM10Wiosna = dataFrameWeatherCondPM10.loc[(dataFrameWeatherCondPM10['date'] >= wiosnaPocz) & (dataFrameWeatherCondPM10['date'] <= wiosnaKon)]
dataFrameWeatherCondPM10Lato = dataFrameWeatherCondPM10.loc[(dataFrameWeatherCondPM10['date'] >= latoPocz) & (dataFrameWeatherCondPM10['date'] <= latoKon)]
dataFrameWeatherCondPM10Jesien = dataFrameWeatherCondPM10.loc[(dataFrameWeatherCondPM10['date'] >= jesienPocz) & (dataFrameWeatherCondPM10['date'] <= jesienKon)]


dataFrameWilgotnoscPM10 = dataFrame[['wilgotnosc','PM10']].copy()
dataFrameWilgotnoscPM10 = dataFrameWilgotnoscPM10.dropna(axis = 0, how = 'any')
dataFrameWilgotnoscPM10 = dataFrameWilgotnoscPM10.reset_index(drop = True)

dataFrameWindDirPM10 = dataFrame[['kierunek wiatru', 'PM10']].copy()
dataFrameWindDirPM10 = dataFrameWindDirPM10.dropna(axis = 0, how = 'any')
dataFrameWindDirPM10 = dataFrameWindDirPM10.reset_index(drop=True)

#############################WYPISZ KORELACJE#############################################
print pearsonr(dataFrameCisnPM['cisnienie'],dataFrameCisnPM['PM10'])
print pearsonr(dataFramePM10PM25['PM10'], dataFramePM10PM25['PM25'])
print pearsonr(dataFrametempPM10['temperatura'],dataFrametempPM10['PM10'])
print pearsonr(dataFramePredkPM10['predkosc wiatru'],dataFramePredkPM10['PM10'])
print pearsonr(dataFrameWilgotnoscPM10['wilgotnosc'],dataFrameWilgotnoscPM10['PM10'])

############################################### KONIEC LICZENIA KORELACJI, LICZENIE DLA GODZIN #######################################

dateSize = len (dataFrameDatePM10)
numberOfLists = 366
itemsInList = 24

categorizedData = [[-1 for x in range(numberOfLists)] for y in range(itemsInList)]


for index, row  in dataFrameDatePM10.iterrows():
    date = row['date']
    PM10 = row['PM10']
    hour = date.hour

    dayNumber = date.timetuple().tm_yday
    categorizedData[hour][dayNumber-1] = PM10

average = []
percentiles_5th = []
percentiles_25th = []
percentiles_50th = []
percentiles_75th = []
percentiles_95th = []


##############################PERCENTYLE DLA GODZINY###############################
for item in categorizedData:
    item = filter(lambda a: a != -1, item)
    avg = sum(item)/len(item)
    average.append(avg)
    percentiles_5th.append(np.percentile(item,5))
    percentiles_25th.append(np.percentile(item,25))
    percentiles_50th.append(np.percentile(item,50))
    percentiles_75th.append(np.percentile(item,75))
    percentiles_95th.append(np.percentile(item,95))



x = range(0,24)
x_pos = np.arange(len(x))

plt.bar(x,average, align = 'center')
plt.xticks(x_pos, x_pos, fontsize = 12 )
plt.xlabel('Godzina', fontsize = 20)
plt.ylabel('Średnie stężenie pyłu $PM_{10}$ $[ug/m^3]$', fontsize = 24)

plt.show()

############################################## PERCENTYLE MEDIANA I SREDNIA DLA KIERUNKU WIATRU ##############################
#
for index, row in dataFrameWindDirPM10.iterrows():
    wind_direction = row['kierunek wiatru']
    PM10 = row ['PM10']
    dictionaryForWindDirection[wind_direction].append(PM10)


dictionaryForWindDirection.pop('', None)
dictionaryForWindDirectionStats.pop('',None)
nameOfDirection = []
valueOfAverage = []


for listName in dictionaryForWindDirection:
    statisticsList = []  # zawiera kolejno elementy: srednia, 5 perc, 25 perc, 50 perc(mediana), 75 perc, 95 perc
    print "######################",listName,"#########################"
    valuesList = dictionaryForWindDirection[listName]
    print dictionaryForWindDirection[listName]
    print sum(dictionaryForWindDirection[listName])
    print len(dictionaryForWindDirection[listName])
    average = sum(dictionaryForWindDirection[listName])/len(dictionaryForWindDirection[listName])
    print average
    centile_5th = np.percentile(valuesList, 5)
    centile_25th = np.percentile(valuesList, 25)
    centile_50th = np.percentile(valuesList, 50)
    centile_75th = np.percentile(valuesList, 75)
    centile_95th = np.percentile(valuesList, 95)

    if (listName == "Variable"):
        listName = "Zmienny"
    if (listName == "South"):
        listName = "S"
    if (listName == "West"):
        listName = "W"
    if (listName == "East"):
        listName = "E"
    if (listName == "North"):
        listName = "N"

    nameOfDirection.append(listName)
    valueOfAverage.append(average)

    statisticsList.extend([average,centile_5th,centile_25th,centile_50th,centile_75th,centile_95th])
    dictionaryForWindDirectionStats[listName] = statisticsList


#####################################SORTOWANIE WYNIKOW######################
sortedDictionary = dict(zip(nameOfDirection,valueOfAverage))
print "###########################################################"

sortedValues = sorted(sortedDictionary.values())
sortedKeys = sorted(sortedDictionary, key=sortedDictionary.__getitem__)


plt.bar(range(len(sortedKeys)),sortedValues, align='center')
plt.xticks(range(len(sortedKeys)), sortedKeys)
plt.xlabel("Kierunek wiatru", fontsize = 20)
plt.ylabel('Średnie stężenie pyłu $PM_{10}$ $[ug/m^3]$', fontsize = 24)
plt.show()

#################################################ZALEZNOSC STEZENIA OD MIESIACA################################################


monthsNumbers = range(1,13)
mainMonthList = []
monthlyList = []
previousMonthNumber = 1

for index, row in dataFrameDatePM10.iterrows():
    currentMonthNumber = row['date'].month
    PM10 = row['PM10']
    if currentMonthNumber == previousMonthNumber:
        monthlyList.append(PM10)
    elif currentMonthNumber != previousMonthNumber:
        mainMonthList.append(monthlyList)
        monthlyList = []
        monthlyList.append(PM10)
        previousMonthNumber = currentMonthNumber

mainMonthList.append(monthlyList) ##DODAJEMY GRUDZIEN DO GLOWNEJ LISTY

monthsDictionary = {MonthNum:[] for MonthNum in monthsNumbers} # Tworzymy slownik dla kazdego miesaca
iterationNumber = 0

for item in mainMonthList:
    monthsStatistics = []
    iterationNumber += 1
    average = sum(item)/len(item)
    percentiles_5th = np.percentile(item, 5)
    percentiles_25th = np.percentile(item, 25)
    percentiles_50th = np.percentile(item, 50)
    percentiles_75th = np.percentile(item, 75)
    percentiles_95th = np.percentile(item, 95)
    monthsStatistics.extend([average,percentiles_5th,percentiles_25th,percentiles_50th,percentiles_75th,percentiles_95th])
    monthsDictionary [iterationNumber] = average


sortedValues = sorted(monthsDictionary.values())
sortedKeys = sorted(monthsDictionary, key=monthsDictionary.__getitem__)
nazwyMiesiecy = ['lipiec', 'czerwiec', 'sierpień', 'maj', 'kwiecień', 'luty',
                 'październik','marzec','wrzesień','grudzień','listopad','styczeń']

plt.bar(range(len(sortedKeys)),sortedValues, align='center')
plt.xticks(range(len(sortedKeys)), nazwyMiesiecy, fontsize = 12)
plt.xlabel("Nazwa miesiąca", fontsize = 20)
plt.title ("Badanie średniego stężenia pyłu $PM_{10}$ dla danego miesiąca w roku 2016 w warszawskiej dzielnicy Targówek", fontsize = 14)
plt.ylabel('Średnie stężenie pyłu $PM_{10}$ $[ug/m^3]$', fontsize = 24)
plt.show()


###################################################### WARUNKI POGODOWE ########################################################

dictionaryForWeatherConditionStatsZima = {listName:[] for listName in weatherCondNames }
dictionaryForWeatherConditionStatsWiosna = {listName:[] for listName in weatherCondNames }
dictionaryForWeatherConditionStatsLato = {listName:[] for listName in weatherCondNames }
dictionaryForWeatherConditionStatsJesien = {listName:[] for listName in weatherCondNames }



mainWeatherCondDictZima = {listName:[] for listName in weatherCondNames}
mainWeatherCondDictWiosna = {listName:[] for listName in weatherCondNames}
mainWeatherCondDictLato= {listName:[] for listName in weatherCondNames}
mainWeatherCondDictJesien= {listName:[] for listName in weatherCondNames}



#######################################################ZIMA##############################################3

for index, row in dataFrameWeatherCondPM10Zima.iterrows():
    weatherCond = str(row['warunki pogodowe'])
    weatherCond = weatherCond.lower()
    PM10 = row['PM10']
    if weatherCond in weatherCondNames:
        mainWeatherCondDictZima[weatherCond].append(PM10)
    elif 'drizzle' in weatherCond:
        mainWeatherCondDictZima['rain'].append(PM10)
    elif 'rain' in weatherCond:
        mainWeatherCondDictZima['rain'].append(PM10)
    elif 'fog' in weatherCond:
        mainWeatherCondDictZima['fog'].append(PM10)
    elif 'snow' in weatherCond:
        mainWeatherCondDictZima['snow'].append(PM10)
    elif 'thunderstorm' in weatherCond:
        mainWeatherCondDictZima['rain'].append(PM10)
    elif 'hail' in weatherCond:
        mainWeatherCondDictZima['rain'].append(PM10)
    elif 'mist' in weatherCond:
        mainWeatherCondDictZima['mist'].append(PM10)

###########################################################WIOSNA############################################

for index, row in dataFrameWeatherCondPM10Wiosna.iterrows():
    weatherCond = str(row['warunki pogodowe'])
    weatherCond = weatherCond.lower()
    PM10 = row['PM10']
    if weatherCond in weatherCondNames:
        mainWeatherCondDictWiosna[weatherCond].append(PM10)
    elif 'drizzle' in weatherCond:
        mainWeatherCondDictWiosna['rain'].append(PM10)
    elif 'rain' in weatherCond:
        mainWeatherCondDictWiosna['rain'].append(PM10)
    elif 'fog' in weatherCond:
        mainWeatherCondDictWiosna['fog'].append(PM10)
    elif 'snow' in weatherCond:
        mainWeatherCondDictWiosna['snow'].append(PM10)
    elif 'thunderstorm' in weatherCond:
        mainWeatherCondDictWiosna['rain'].append(PM10)
    elif 'hail' in weatherCond:
        mainWeatherCondDictWiosna['rain'].append(PM10)
    elif 'mist' in weatherCond:
        mainWeatherCondDictWiosna['mist'].append(PM10)


#################################################################LATO#######################################

for index, row in dataFrameWeatherCondPM10Lato.iterrows():
    weatherCond = str(row['warunki pogodowe'])
    weatherCond = weatherCond.lower()
    PM10 = row['PM10']
    if weatherCond in weatherCondNames:
        mainWeatherCondDictLato[weatherCond].append(PM10)
    elif 'drizzle' in weatherCond:
        mainWeatherCondDictLato['rain'].append(PM10)
    elif 'rain' in weatherCond:
        mainWeatherCondDictLato['rain'].append(PM10)
    elif 'fog' in weatherCond:
        mainWeatherCondDictLato['fog'].append(PM10)
    elif 'snow' in weatherCond:
        mainWeatherCondDictLato['snow'].append(PM10)
    elif 'thunderstorm' in weatherCond:
        mainWeatherCondDictLato['rain'].append(PM10)
    elif 'hail' in weatherCond:
        mainWeatherCondDictLato['rain'].append(PM10)
    elif 'mist' in weatherCond:
        mainWeatherCondDictLato['mist'].append(PM10)

###################################################################JESIEN#######################################################
for index, row in dataFrameWeatherCondPM10Jesien.iterrows():
    weatherCond = str(row['warunki pogodowe'])
    weatherCond = weatherCond.lower()
    PM10 = row['PM10']
    if weatherCond in weatherCondNames:
        mainWeatherCondDictJesien[weatherCond].append(PM10)
    elif 'drizzle' in weatherCond:
        mainWeatherCondDictJesien['rain'].append(PM10)
    elif 'rain' in weatherCond:
        mainWeatherCondDictJesien['rain'].append(PM10)
    elif 'fog' in weatherCond:
        mainWeatherCondDictJesien['fog'].append(PM10)
    elif 'snow' in weatherCond:
        mainWeatherCondDictJesien['snow'].append(PM10)
    elif 'thunderstorm' in weatherCond:
        mainWeatherCondDictJesien['rain'].append(PM10)
    elif 'hail' in weatherCond:
        mainWeatherCondDictJesien['rain'].append(PM10)
    elif 'mist' in weatherCond:
        mainWeatherCondDictJesien['mist'].append(PM10)

#################################################################PERCENYLE###################################
for item in mainWeatherCondDictZima:
    if (len(mainWeatherCondDictZima[item])!=0):
        avg = sum (mainWeatherCondDictZima[item])/len(mainWeatherCondDictZima[item])
        perentile_5th = np.percentile(mainWeatherCondDictZima[item],5)
        perentile_25th = np.percentile(mainWeatherCondDictZima[item],25)
        percentile_50th = np.percentile(mainWeatherCondDictZima[item],50)
        percentile_75th = np.percentile(mainWeatherCondDictZima[item],75)
        percentile_95th = np.percentile(mainWeatherCondDictZima[item],95)
        dictionaryForWeatherConditionStatsZima[item] = avg

for item in mainWeatherCondDictWiosna:
    if (len(mainWeatherCondDictWiosna[item])!=0):
        avg = sum (mainWeatherCondDictWiosna[item])/len(mainWeatherCondDictWiosna[item])
        perentile_5th = np.percentile(mainWeatherCondDictWiosna[item],5)
        perentile_25th = np.percentile(mainWeatherCondDictWiosna[item],25)
        percentile_50th = np.percentile(mainWeatherCondDictWiosna[item],50)
        percentile_75th = np.percentile(mainWeatherCondDictWiosna[item],75)
        percentile_95th = np.percentile(mainWeatherCondDictWiosna[item],95)
        dictionaryForWeatherConditionStatsWiosna[item] = avg

for item in mainWeatherCondDictLato:
    if (len(mainWeatherCondDictLato[item]) != 0):
        avg = sum(mainWeatherCondDictLato[item]) / len(mainWeatherCondDictLato[item])
        perentile_5th = np.percentile(mainWeatherCondDictLato[item], 5)
        perentile_25th = np.percentile(mainWeatherCondDictLato[item], 25)
        percentile_50th = np.percentile(mainWeatherCondDictLato[item], 50)
        percentile_75th = np.percentile(mainWeatherCondDictLato[item], 75)
        percentile_95th = np.percentile(mainWeatherCondDictLato[item], 95)
        dictionaryForWeatherConditionStatsLato[item] = avg

for item in mainWeatherCondDictJesien:
    if (len(mainWeatherCondDictJesien[item]) != 0):
        avg = sum(mainWeatherCondDictJesien[item]) / len(mainWeatherCondDictJesien[item])
        perentile_5th = np.percentile(mainWeatherCondDictJesien[item], 5)
        perentile_25th = np.percentile(mainWeatherCondDictJesien[item], 25)
        percentile_50th = np.percentile(mainWeatherCondDictJesien[item], 50)
        percentile_75th = np.percentile(mainWeatherCondDictJesien[item], 75)
        percentile_95th = np.percentile(mainWeatherCondDictJesien[item], 95)
        dictionaryForWeatherConditionStatsJesien[item] = avg

############################################################SPRAWDZENIE ŻEBY NIE BYŁO PUSTYCH WARTOŚCI################

for x in list(dictionaryForWeatherConditionStatsWiosna.keys()):
    if dictionaryForWeatherConditionStatsWiosna[x] == []:
        dictionaryForWeatherConditionStatsWiosna[x] = 0

for x in list(dictionaryForWeatherConditionStatsLato.keys()):
    if dictionaryForWeatherConditionStatsLato[x] == []:
        dictionaryForWeatherConditionStatsLato[x] = 0

for x in list(dictionaryForWeatherConditionStatsJesien.keys()):
    if dictionaryForWeatherConditionStatsLato[x] == []:
        dictionaryForWeatherConditionStatsLato[x] = 0


valuesZima = (dictionaryForWeatherConditionStatsZima.values())
valuesWiosna = (dictionaryForWeatherConditionStatsWiosna.values())
valuesLato = dictionaryForWeatherConditionStatsLato.values()
valuesJesien = dictionaryForWeatherConditionStatsJesien.values()


index = np.arange(7)
bar_width = 0.1
opacity = 0.8

valuesToPlotZima = [valuesZima[1], valuesZima[6], valuesZima[2],valuesZima[3],valuesZima[4],valuesZima[7],valuesZima[5]]
valuesToPlotWiosna = [valuesWiosna[1], valuesWiosna[6], valuesWiosna[2],valuesWiosna[3],valuesWiosna[4],valuesWiosna[7],valuesWiosna[5]]
valuesToPlotLato = [valuesLato[1], valuesLato[6], valuesLato[2],valuesLato[3],valuesLato[4],valuesLato[7],valuesLato[5]]
valuesToPlotJesien = [valuesJesien[1], valuesJesien[6], valuesJesien[2],valuesJesien[3],valuesJesien[4],valuesJesien[7],valuesJesien[5]]



plt.bar(index + bar_width, valuesToPlotWiosna,bar_width,
        alpha=opacity,
        color='g',
        label='wiosna'
        )

plt.bar(index + 2*bar_width, valuesToPlotLato,bar_width,
        alpha=opacity,
        color='y',
        label='lato'
        )

plt.bar(index + 3*bar_width, valuesToPlotJesien,bar_width,
        alpha=opacity,
        color='orange',
        label='jesień'
        )

plt.bar(index, valuesToPlotZima, bar_width,
                 alpha=opacity,
                 color='b',
                 label='zima')

plt.xlabel('Warunki pogodowe', fontsize = 24)
plt.ylabel('Średnie stężenie pyłu $PM_{10}$ $[ug/m^3]$', fontsize = 24)
plt.xticks(index+0.2, ('brak chmur','zachm. średnie', 'zachm. całkowite','śnieg','deszcz','rzadka mgła','gęsta mgła' ), fontsize = 12)
title = r'Średnie stężenie pyłu $PM_{10}$ dla danych warunków pogodowych w roku 2016 w warszawskiej dzielnicy Targówek'
plt.title(title)

plt.legend(loc='best',fontsize = 14 )
plt.show()


