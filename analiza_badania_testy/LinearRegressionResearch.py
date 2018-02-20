# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sqlite3
import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from sklearn import linear_model
from tendencies import TendencyCreator
from sklearn.metrics import accuracy_score

# Ten skrypt zawiera badania związane z regresją liniową, opisane w rozdziale 5

# implementacja tego pliku związana z regresją czerpała z:
# https://github.com/lazyprogrammer/machine_learning_examples/blob/master/linear_regression_class/lr_2d.py
#
#

def policzBladWzgledny(outputHat, outputTest):
    blWzglArr = []
    for i in range(0, len(dataFrameOutputTest)):
        blBezwzgl = abs(outputHat[i] - outputTest[i])
        blWzgl = (blBezwzgl / outputTest[i]) * 100
        blWzglArr.append(blWzgl)
    return sum(blWzglArr)/len(blWzglArr)

def policzW(dataFrameInput, dataFrameOutput):
    return np.linalg.solve(np.dot(dataFrameInput.T, dataFrameInput),np.dot(dataFrameInput.T,dataFrameOutput))

def policzPredykcje(w, dataFrameInputTest):
    dataFrameOutputHat = np.dot(dataFrameInputTest, w)
    return dataFrameOutputHat

def policzR2 (dataFrameOutpTest, dataFrameOutpHat):
    d1 = dataFrameOutpTest - dataFrameOutpHat
    d2 = dataFrameOutpTest - dataFrameOutpTest.mean()
    r2 = 1 - d1.dot(d1) / d2.dot(d2)
    return r2

conn = sqlite3.connect('dane.db')
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
dataFrameShuffled = shuffle(dataFrame)

mainDataFrame = dataFrame[['temperatura','cisnienie','kierunek wiatru','warunki pogodowe','predkosc wiatru','wilgotnosc','PM10','date','PM25']]
mainDataFrame = mainDataFrame.dropna(axis=0, how='any')
mainDataFrame = mainDataFrame.reset_index(drop=True)
#############################################Obliczenie wspolczynnika dla pm25#######################################
PM10Sum = sum(mainDataFrame['PM10'])
PM25Sum = sum(mainDataFrame['PM25'])
print "wspolczynnik : ", PM25Sum/PM10Sum


###############################################SAMA POGODA BIEZACA########################################3

dataFrameFirst = mainDataFrame[['temperatura','predkosc wiatru','wilgotnosc', 'PM10', 'cisnienie']]
onesColumn = np.ones((len(dataFrameFirst),1))
dataFrameFirst['ones'] = onesColumn
dataFrameFirst = shuffle(dataFrameFirst)


dataFrameInputFirst = dataFrameFirst[['temperatura','predkosc wiatru','wilgotnosc','ones']]
dataFrameOutputFirst = dataFrameFirst['PM10']

dataFrameInputFirst = np.array(dataFrameInputFirst)
dataFrameOutputFirst = np.array(dataFrameOutputFirst)

dataFrameInputTrain = dataFrameInputFirst[0:7000]
dataFrameOutputTrain = dataFrameOutputFirst[0:7000]

dataFrameInputTest = dataFrameInputFirst[7000:]
dataFrameOutputTest = dataFrameOutputFirst[7000:]

##1. MOJE

w = policzW(dataFrameInputTrain, dataFrameOutputTrain)
dataFrameOutputHat = policzPredykcje(w,dataFrameInputTest)
r2 = policzR2(dataFrameOutputTest, dataFrameOutputHat)

print "rsquared pierwsze", r2
print "blWzgl pogoda ciagla moje:", policzBladWzgledny(dataFrameOutputHat, dataFrameOutputTest)


##implementacja ich
regr = linear_model.LinearRegression()
regr.fit(dataFrameInputTest, dataFrameOutputTest)
predictedOutput = regr.predict(dataFrameInputTest)


print "rsquared pierwsze implementacja ich",regr.score(dataFrameInputTest, dataFrameOutputTest)
print "blad wzgledny pierwsze implementacja ich",policzBladWzgledny(predictedOutput, dataFrameOutputTest)

###REGUL:

regr = linear_model.Ridge()
regr.fit(dataFrameInputTest, dataFrameOutputTest)
predictedOutput = regr.predict(dataFrameInputTest)
print "Lasso",regr.score(dataFrameInputTest, dataFrameOutputTest)
print "Lasso",policzBladWzgledny(predictedOutput, dataFrameOutputTest)


#############################################################2. POGODA BIEZACA I POPRZEDNIA#######################################
tempPoprzednia = mainDataFrame[0:-1]['temperatura']
wilgPoprzednia = mainDataFrame[0:-1]['wilgotnosc']
predkoscWiatruPoprzednia = mainDataFrame[0:-1]['predkosc wiatru']
cisnPoprzednie = mainDataFrame[0:-1]['cisnienie']


DataFrameSecond = pd.DataFrame()
DataFrameSecond = mainDataFrame[1:][['temperatura','predkosc wiatru','wilgotnosc', 'PM10']]


onesColumn = np.ones((len(DataFrameSecond),1))
DataFrameSecond['ones'] = onesColumn

DataFrameSecond = DataFrameSecond.reset_index(drop=True)
DataFrameSecond['temperaturaPoprzednia'] = tempPoprzednia
DataFrameSecond['wilgotnoscPoprzednia'] = wilgPoprzednia
DataFrameSecond['predkoscWiatruPoprzednia'] = predkoscWiatruPoprzednia
DataFrameSecond['cisnPoprzednie'] = cisnPoprzednie

DataFrameSecond = shuffle(DataFrameSecond)

dataFrameInputSecond = DataFrameSecond[['temperatura','predkosc wiatru','wilgotnosc',
                                        'temperaturaPoprzednia','wilgotnoscPoprzednia',
                                        'predkoscWiatruPoprzednia','ones']]

dataFrameOutputSecond = DataFrameSecond['PM10']

dataFrameInputSecond = np.array(dataFrameInputSecond)
dataFrameOutputSecond = np.array(dataFrameOutputSecond)

dataFrameInputTrain = dataFrameInputSecond[0:7000]
dataFrameOutputTrain = dataFrameOutputSecond[0:7000]

dataFrameInputTest = dataFrameInputSecond[7000:]
dataFrameOutputTest = dataFrameOutputSecond[7000:]


##1. MOJE

w = policzW(dataFrameInputTrain, dataFrameOutputTrain)
dataFrameOutputHat = policzPredykcje(w,dataFrameInputTest)
r2 = policzR2(dataFrameOutputTest, dataFrameOutputHat)

print "2.rsquared implementacja moje", r2
print "2. blWzgl pogoda ciagla plus historyczne moje:", policzBladWzgledny(dataFrameOutputHat, dataFrameOutputTest)

##2. ICH
regr = linear_model.LinearRegression()
regr.fit(dataFrameInputTest, dataFrameOutputTest)
predictedOutput = regr.predict(dataFrameInputTest)

print "2.rsquared implementacja ich",regr.score(dataFrameInputTest, dataFrameOutputTest)
print "2.blad wzgledny implementacja ich",policzBladWzgledny(predictedOutput, dataFrameOutputTest)

###REGUL:

regr = linear_model.Ridge()
regr.fit(dataFrameInputTest, dataFrameOutputTest)
predictedOutput = regr.predict(dataFrameInputTest)
print "Lasso",regr.score(dataFrameInputTest, dataFrameOutputTest)
print "Lasso",policzBladWzgledny(predictedOutput, dataFrameOutputTest)

##############################3.POGODABIEZACA+ POGODA HISTORYCZNA + WAR POGODOWE######################

tempPoprzednia = mainDataFrame[0:-1]['temperatura']
wilgPoprzednia = mainDataFrame[0:-1]['wilgotnosc']
predkoscWiatruPoprzednia = mainDataFrame[0:-1]['predkosc wiatru']
cisnPoprzednie = mainDataFrame[0:-1]['cisnienie']
DataFrameThird = pd.DataFrame()

DataFrameThird = mainDataFrame[1:][['temperatura','predkosc wiatru','wilgotnosc', 'warunki pogodowe','PM10']]
DataFrameThird = DataFrameThird.reset_index(drop=True)
DataFrameThird['tempPoprzednia'] = tempPoprzednia
DataFrameThird['wilgPoprzednia'] = wilgPoprzednia
DataFrameThird['predkPoprzednia'] = predkoscWiatruPoprzednia
DataFrameThird['cisnPoprzednie'] = cisnPoprzednie


onesColumn = np.ones((len(DataFrameThird),1))
DataFrameThird['rain'] = np.where((DataFrameThird['warunki pogodowe'].str.contains("Rain")) | (DataFrameThird['warunki pogodowe'].str.contains("Drizzle")) | (DataFrameThird['warunki pogodowe'].str.contains("Thunderstorm")) | (DataFrameThird['warunki pogodowe'].str.contains("Hail")),1,0)
DataFrameThird['fog'] = np.where( DataFrameThird['warunki pogodowe'].str.contains("Fog"),1, 0)
DataFrameThird['mist'] = np.where(DataFrameThird['warunki pogodowe'].str.contains("Mist"),1, 0)
DataFrameThird['ones'] = onesColumn
DataFrameThird = DataFrameThird.drop('warunki pogodowe',1)

DataFrameThird = shuffle(DataFrameThird)


dataFrameThirdInput = DataFrameThird[['temperatura', 'wilgotnosc', 'predkosc wiatru','rain','fog','mist','ones',
                                      'tempPoprzednia','wilgPoprzednia','predkPoprzednia'
                                     ]]

dataFrameThirdOutput = DataFrameThird['PM10']

dataFrameInputThird = np.array(dataFrameThirdInput)
dataFrameThirdOutput = np.array(dataFrameThirdOutput)

dataFrameInputTrain = dataFrameThirdInput[0:7000]
dataFrameOutputTrain = dataFrameThirdOutput[0:7000]

dataFrameInputTest = dataFrameThirdInput[7000:]
dataFrameOutputTest = dataFrameThirdOutput[7000:]

w = policzW(dataFrameInputTrain, dataFrameOutputTrain)
dataFrameOutputHat = policzPredykcje(w,dataFrameInputTest)


r2 = policzR2(dataFrameOutputTest, dataFrameOutputHat)

print "3. Moje r_squared pogoda + pogoda_hist + warunki:", r2
print "3. Moje blWzgl pogoda + pogoda_hist + warunki",  policzBladWzgledny(dataFrameOutputHat, dataFrameOutputTest)

##2. ICH
regr = linear_model.LinearRegression()
regr.fit(dataFrameInputTest, dataFrameOutputTest)
predictedOutput = regr.predict(dataFrameInputTest)

print "3.rsquared implementacja ich",regr.score(dataFrameInputTest, dataFrameOutputTest)
print "3.blWzgl pogoda + pogoda_hist + warunki implementacja ich",policzBladWzgledny(predictedOutput, dataFrameOutputTest)

###REGUL:

regr = linear_model.Ridge()
regr.fit(dataFrameInputTest, dataFrameOutputTest)
predictedOutput = regr.predict(dataFrameInputTest)
print "Lasso",regr.score(dataFrameInputTest, dataFrameOutputTest)
print "Lasso",policzBladWzgledny(predictedOutput, dataFrameOutputTest)

#
# ################################################PODODA + POGODA_HIST, WARUNKI+WARUNKI_HIST+ ###########################################

DataFrameFourth= mainDataFrame[['temperatura','predkosc wiatru','wilgotnosc', 'warunki pogodowe','PM10']]
onesColumn = np.ones((len(DataFrameFourth),1))
DataFrameFourth['rain'] = np.where((DataFrameFourth['warunki pogodowe'].str.contains("Rain")) | (DataFrameFourth['warunki pogodowe'].str.contains("Drizzle")) | (DataFrameFourth['warunki pogodowe'].str.contains("Thunderstorm")) | (DataFrameFourth['warunki pogodowe'].str.contains("Hail")),1,0)
DataFrameFourth['fog'] = np.where( DataFrameFourth['warunki pogodowe'].str.contains("Fog"),1, 0)
DataFrameFourth['mist'] = np.where(DataFrameFourth['warunki pogodowe'].str.contains("Mist"),1, 0)
DataFrameFourth['ones'] = onesColumn
DataFrameFourth = DataFrameFourth.drop('warunki pogodowe',1)

tempPoprzednia = DataFrameFourth[0:-1]['temperatura']
wilgPoprzednia = DataFrameFourth[0:-1]['wilgotnosc']
predkoscWiatruPoprzednia = DataFrameFourth[0:-1]['predkosc wiatru']
rainPoprz = DataFrameFourth[0:-1]['rain']
fogPoprz = DataFrameFourth[0:-1]['fog']
mistPoprz = DataFrameFourth[0:-1]['mist']
DataFrameFourth = DataFrameFourth[1:]
DataFrameFourth = DataFrameFourth.reset_index(drop=True)

DataFrameFourth['tempPoprzednia'] = tempPoprzednia
DataFrameFourth['wilgPoprzednia'] = wilgPoprzednia
DataFrameFourth['predkPoprzednia'] = predkoscWiatruPoprzednia
DataFrameFourth['rainPoprz'] = rainPoprz
DataFrameFourth['fogPoprz'] = fogPoprz
DataFrameFourth['mistPoprz'] = mistPoprz


DataFrameFourth = shuffle(DataFrameFourth)

DataFrameFourthInput = DataFrameFourth[['temperatura', 'wilgotnosc', 'predkosc wiatru','rain','fog','mist','ones',
                                      'tempPoprzednia','wilgPoprzednia','predkPoprzednia','rainPoprz', 'fogPoprz',
                                      'mistPoprz'
                                     ]]

DataFrameFourthOutput = DataFrameFourth['PM10']

DataFrameFourthInput = np.array(DataFrameFourthInput)
DataFrameFourthOutput = np.array(DataFrameFourthOutput)

dataFrameInputTrain = DataFrameFourthInput[0:7000]
dataFrameOutputTrain = DataFrameFourthOutput[0:7000]

dataFrameInputTest = DataFrameFourthInput[7000:]
dataFrameOutputTest = DataFrameFourthOutput[7000:]

w = policzW(dataFrameInputTrain, dataFrameOutputTrain)
dataFrameOutputHat = policzPredykcje(w,dataFrameInputTest)

r2 = policzR2(dataFrameOutputTest, dataFrameOutputHat)
print "4. Moje r_squared pogoda + pogoda_hist + warunki + warunki_hist:", r2
print "4. Moje blWzgl pogoda + pogoda_hist + warunki+ warunki_hist",  policzBladWzgledny(dataFrameOutputHat, dataFrameOutputTest)

##2. ICH
regr = linear_model.LinearRegression()
regr.fit(dataFrameInputTest, dataFrameOutputTest)
predictedOutput = regr.predict(dataFrameInputTest)

print "4.rsquared implementacja ich",regr.score(dataFrameInputTest, dataFrameOutputTest)
print "4.blWzgl pogoda + pogoda_hist + warunki+ warunki_hist ich",policzBladWzgledny(predictedOutput, dataFrameOutputTest)

###REGUL:

regr = linear_model.Ridge()
regr.fit(dataFrameInputTest, dataFrameOutputTest)
predictedOutput = regr.predict(dataFrameInputTest)
print "Lasso",regr.score(dataFrameInputTest, dataFrameOutputTest)
print "Lasso",policzBladWzgledny(predictedOutput, dataFrameOutputTest)

####################################################PODODA + POGODA_HIST, WARUNKI+WIATR########################

##WYWALAMY WAR.HIST BO POGARSZALY WYNIK

DataFrameFifth= mainDataFrame[['temperatura','predkosc wiatru','wilgotnosc', 'warunki pogodowe','PM10', 'kierunek wiatru', 'date', 'cisnienie']]
onesColumn = np.ones((len(DataFrameFifth),1))
DataFrameFifth['rain'] = np.where((DataFrameFifth['warunki pogodowe'].str.contains("Rain")) | (DataFrameFifth['warunki pogodowe'].str.contains("Drizzle")) | (DataFrameFifth['warunki pogodowe'].str.contains("Thunderstorm")) | (DataFrameFifth['warunki pogodowe'].str.contains("Hail")),1,0)
DataFrameFifth['fog'] = np.where( DataFrameFifth['warunki pogodowe'].str.contains("Fog"),1, 0)
DataFrameFifth['mist'] = np.where(DataFrameFifth['warunki pogodowe'].str.contains("Mist"),1, 0)
DataFrameFifth['snow'] = np.where(DataFrameFifth['warunki pogodowe'].str.contains("Snow"),1, 0)
DataFrameFifth['partly cloudy'] = np.where(DataFrameFifth['warunki pogodowe'].str.contains("Partly Cloudy"),1, 0)
DataFrameFifth['overcast'] = np.where(DataFrameFifth['warunki pogodowe'].str.contains("Overcast"),1, 0)
DataFrameFifth['clear'] = np.where(DataFrameFifth['warunki pogodowe'].str.contains("Clear"),1, 0)
DataFrameFifth['scattered clouds'] = np.where(DataFrameFifth['warunki pogodowe'].str.contains("Scattered Clouds"),1, 0)
DataFrameFifth['mostly cloudy'] = np.where(DataFrameFifth['warunki pogodowe'].str.contains("Mostly Cloudy"),1, 0)
DataFrameFifth['unknown'] = np.where(DataFrameFifth['warunki pogodowe'].str.contains("Unknown"),1,0)
DataFrameFifth['ones'] = onesColumn


tempPoprzednia = DataFrameFifth[0:-1]['temperatura']
wilgPoprzednia = DataFrameFifth[0:-1]['wilgotnosc']
predkoscWiatruPoprzednia = DataFrameFifth[0:-1]['predkosc wiatru']
cisnPoprzednie = DataFrameFifth[0:-1]['cisnienie']

DataFrameFifth['west'] =  np.where( DataFrameFifth['kierunek wiatru'] == ("West"),1, 0)
DataFrameFifth['wsw'] =  np.where( DataFrameFifth['kierunek wiatru'] == ("WSW"),1, 0)
DataFrameFifth['wnw'] =  np.where( DataFrameFifth['kierunek wiatru'] == ("WNW"),1, 0)
DataFrameFifth['variable'] =  np.where( DataFrameFifth['kierunek wiatru'] == ("Variable"),1, 0)
DataFrameFifth['south'] =  np.where( DataFrameFifth['kierunek wiatru'] == ("South"),1, 0)
DataFrameFifth['sw'] =  np.where( DataFrameFifth['kierunek wiatru'] == ("SW"),1, 0)
DataFrameFifth['ssw'] =  np.where( DataFrameFifth['kierunek wiatru'] == ("SSW"),1, 0)
DataFrameFifth['sse'] =  np.where( DataFrameFifth['kierunek wiatru'] == ("SSE"),1, 0)
DataFrameFifth['se'] =  np.where( DataFrameFifth['kierunek wiatru'] == ("SE"),1, 0)
DataFrameFifth['north'] =  np.where( DataFrameFifth['kierunek wiatru'] == ("North"),1, 0)
DataFrameFifth['nw'] =  np.where( DataFrameFifth['kierunek wiatru'] == ("NW"),1, 0)
DataFrameFifth['nnw'] =  np.where( DataFrameFifth['kierunek wiatru'] == ("NNW"),1, 0)
DataFrameFifth['nne'] =  np.where( DataFrameFifth['kierunek wiatru'] == ("NNE"),1, 0)
DataFrameFifth['ne'] =  np.where( DataFrameFifth['kierunek wiatru'] == ("NE"),1, 0)
DataFrameFifth['east'] =  np.where( DataFrameFifth['kierunek wiatru'] == ("East"),1, 0)
DataFrameFifth['ese'] =  np.where( DataFrameFifth['kierunek wiatru'] == ("ESE"),1, 0)
DataFrameFifth['ene'] =  np.where( DataFrameFifth['kierunek wiatru'] == ("ENE"),1, 0)

DataFrameFifth = DataFrameFifth[1:]
DataFrameFifth = DataFrameFifth.reset_index(drop=True)

DataFrameFifth['tempPoprzednia'] = tempPoprzednia
DataFrameFifth['wilgPoprzednia'] = wilgPoprzednia
DataFrameFifth['predkPoprzednia'] = predkoscWiatruPoprzednia
DataFrameFifth['cisnPoprzednie'] = cisnPoprzednie

DataFrameFifthBeforeSfuffled = DataFrameFifth

DataFrameFifth = shuffle(DataFrameFifth)

DataFrameFifthInput = DataFrameFifth[['temperatura', 'wilgotnosc', 'predkosc wiatru','rain','fog','mist','ones',
                                      'tempPoprzednia','wilgPoprzednia','predkPoprzednia','west', 'wsw', 'wnw', 'variable',
                                      'south', 'sw', 'ssw',
                                      'sse', 'se', 'north', 'nw', 'nnw', 'nne', 'ne', 'east', 'ese', 'ene'
                                     ]]

DataFrameFifthOutput = DataFrameFifth['PM10']


DataFrameFifthInput = np.array(DataFrameFifthInput)
DataFrameFifthOutput = np.array(DataFrameFifthOutput)

dataFrameInputTrain = DataFrameFifthInput[0:7000]
dataFrameOutputTrain = DataFrameFifthOutput[0:7000]

dataFrameInputTest = DataFrameFifthInput[7000:]
dataFrameOutputTest = DataFrameFifthOutput[7000:]

w = policzW(dataFrameInputTrain, dataFrameOutputTrain)
dataFrameOutputHat = policzPredykcje(w,dataFrameInputTest)

r2 = policzR2(dataFrameOutputTest, dataFrameOutputHat)
print "5. Moje r_squared pogoda + pogoda_hist + warunki + wiatr:", r2
print "5. Moje blWzgl pogoda + pogoda_hist + warunki+ wiatr",  policzBladWzgledny(dataFrameOutputHat, dataFrameOutputTest)

##2. ICH
regr = linear_model.LinearRegression()
regr.fit(dataFrameInputTest, dataFrameOutputTest)
predictedOutput = regr.predict(dataFrameInputTest)

print "5.rsquared implementacja ich",regr.score(dataFrameInputTest, dataFrameOutputTest)
print "5. blWzgl pogoda + pogoda_hist + warunki+ wiatr ich",policzBladWzgledny(predictedOutput, dataFrameOutputTest)

###REGUL:

regr = linear_model.Ridge()
regr.fit(dataFrameInputTest, dataFrameOutputTest)
predictedOutput = regr.predict(dataFrameInputTest)
print "Lasso",regr.score(dataFrameInputTest, dataFrameOutputTest)
print "Lasso",policzBladWzgledny(predictedOutput, dataFrameOutputTest)

# ############################################Pogoda + warunki + wiatr + wiatr_hist#####################################

DataFrameSixth = DataFrameFifthBeforeSfuffled

westHist = DataFrameSixth[0:-1]['west']
wswHist = DataFrameSixth[0:-1]['wsw']
wnwHist= DataFrameSixth[0:-1]['wnw']
variableHist = DataFrameSixth[0:-1]['variable']
southHist = DataFrameSixth[0:-1]['south']
swHist = DataFrameSixth[0:-1]['sw']
sswHist = DataFrameSixth[0:-1]['ssw']
sseHist = DataFrameSixth[0:-1]['sse']
seHist = DataFrameSixth[0:-1]['se']
northHist = DataFrameSixth[0:-1]['north']
nwHist = DataFrameSixth[0:-1]['nw']
nnwHist = DataFrameSixth[0:-1]['nnw']
nneHist = DataFrameSixth[0:-1]['nne']
neHist = DataFrameSixth[0:-1]['ne']
eastHist = DataFrameSixth[0:-1]['east']
eseHist = DataFrameSixth[0:-1]['ese']
eneHist = DataFrameSixth[0:-1]['ene']

DataFrameSixth = DataFrameSixth[1:]
DataFrameSixth = DataFrameSixth.reset_index(drop=True)

DataFrameSixth['westHist'] = westHist
DataFrameSixth['wswHist'] = wswHist
DataFrameSixth['wnwHsit'] = wnwHist
DataFrameSixth['variableHist'] = variableHist
DataFrameSixth['southHist'] = southHist
DataFrameSixth['swHist'] = swHist
DataFrameSixth['sswHist'] = sswHist
DataFrameSixth['sseHist'] = sseHist
DataFrameSixth['seHist'] = seHist
DataFrameSixth['northHist'] = northHist
DataFrameSixth['nwHist'] = nwHist
DataFrameSixth['nnwHist'] = nnwHist
DataFrameSixth['nneHist'] = nneHist
DataFrameSixth['neHist'] = neHist
DataFrameSixth['eastHist'] = eastHist
DataFrameSixth['eseHist'] = eseHist
DataFrameSixth['eneHist'] = eneHist


DataFrameSixthBeforeShuffled = DataFrameSixth
DataFrameSixth = shuffle(DataFrameSixth)

DataFrameSixthInput = DataFrameSixth[['temperatura', 'wilgotnosc', 'predkosc wiatru','rain','fog','mist','ones',
                                      'tempPoprzednia','wilgPoprzednia','predkPoprzednia','west', 'wsw', 'wnw', 'variable',
                                      'south', 'sw', 'ssw',
                                      'sse', 'se', 'north', 'nw', 'nnw', 'nne', 'ne', 'east', 'ese', 'ene',
                                      'westHist', 'wswHist', 'wnwHsit', 'variableHist', 'southHist', 'swHist',
                                      'sswHist', 'sseHist', 'seHist', 'northHist', 'nwHist', 'nnwHist', 'nneHist',
                                      'neHist', 'eastHist', 'eseHist', 'eneHist'
                                     ]]

DataFrameSixthOutput = DataFrameSixth['PM10']

DataFrameSixthInput = np.array(DataFrameSixthInput)
DataFrameSixthOutput = np.array(DataFrameSixthOutput)

dataFrameInputTrain = DataFrameSixthInput[0:7000]
dataFrameOutputTrain = DataFrameSixthOutput[0:7000]

dataFrameInputTest = DataFrameSixthInput[7000:]
dataFrameOutputTest = DataFrameSixthOutput[7000:]

w = policzW(dataFrameInputTrain, dataFrameOutputTrain)
dataFrameOutputHat = policzPredykcje(w,dataFrameInputTest)

r2 = policzR2(dataFrameOutputTest, dataFrameOutputHat)
print "6. Moje r_squared pogoda + pogoda_hist + warunki + wiatr+ wiatrHist:", r2
print "6. Moje blWzgl pogoda + pogoda_hist + warunki+ wiatr + wiatrHist",  policzBladWzgledny(dataFrameOutputHat, dataFrameOutputTest)


##2. ICH
regr = linear_model.LinearRegression()
regr.fit(dataFrameInputTest, dataFrameOutputTest)
predictedOutput = regr.predict(dataFrameInputTest)

print "6.rsquared implementacja ich",regr.score(dataFrameInputTest, dataFrameOutputTest)
print "6.blWzgl blWzgl pogoda + pogoda_hist + warunki+ wiatr + wiatrHist ich",policzBladWzgledny(predictedOutput, dataFrameOutputTest)

###REGUL:

regr = linear_model.Ridge()
regr.fit(dataFrameInputTest, dataFrameOutputTest)
predictedOutput = regr.predict(dataFrameInputTest)
print "Lasso",regr.score(dataFrameInputTest, dataFrameOutputTest)
print "Lasso",policzBladWzgledny(predictedOutput, dataFrameOutputTest)

##########################################################Pogoda + warunki + wiatr + wiatr_hist + godzina############3

DataFrameSeventh = DataFrameSixthBeforeShuffled

DataFrameSeventh['godzina 0'] = np.where(DataFrameSeventh['date'].dt.hour == 0, 1, 0)
DataFrameSeventh['godzina 1'] = np.where(DataFrameSeventh['date'].dt.hour == 1, 1, 0)
DataFrameSeventh['godzina 2'] = np.where(DataFrameSeventh['date'].dt.hour == 2, 1, 0)
DataFrameSeventh['godzina 3'] = np.where(DataFrameSeventh['date'].dt.hour == 3, 1, 0)
DataFrameSeventh['godzina 4'] = np.where(DataFrameSeventh['date'].dt.hour == 4, 1, 0)
DataFrameSeventh['godzina 5'] = np.where(DataFrameSeventh['date'].dt.hour == 5, 1, 0)
DataFrameSeventh['godzina 6'] = np.where(DataFrameSeventh['date'].dt.hour == 6, 1, 0)
DataFrameSeventh['godzina 7'] = np.where(DataFrameSeventh['date'].dt.hour == 7, 1, 0)
DataFrameSeventh['godzina 8'] = np.where(DataFrameSeventh['date'].dt.hour == 8, 1, 0)
DataFrameSeventh['godzina 9'] = np.where(DataFrameSeventh['date'].dt.hour == 9, 1, 0)
DataFrameSeventh['godzina 10'] = np.where(DataFrameSeventh['date'].dt.hour == 10, 1, 0)
DataFrameSeventh['godzina 11'] = np.where(DataFrameSeventh['date'].dt.hour == 11, 1, 0)
DataFrameSeventh['godzina 12'] = np.where(DataFrameSeventh['date'].dt.hour == 12, 1, 0)
DataFrameSeventh['godzina 13'] = np.where(DataFrameSeventh['date'].dt.hour == 13, 1, 0)
DataFrameSeventh['godzina 14'] = np.where(DataFrameSeventh['date'].dt.hour == 14, 1, 0)
DataFrameSeventh['godzina 15'] = np.where(DataFrameSeventh['date'].dt.hour == 15, 1, 0)
DataFrameSeventh['godzina 16'] = np.where(DataFrameSeventh['date'].dt.hour == 16, 1, 0)
DataFrameSeventh['godzina 17'] = np.where(DataFrameSeventh['date'].dt.hour == 17, 1, 0)
DataFrameSeventh['godzina 18'] = np.where(DataFrameSeventh['date'].dt.hour == 18, 1, 0)
DataFrameSeventh['godzina 19'] = np.where(DataFrameSeventh['date'].dt.hour == 19, 1, 0)
DataFrameSeventh['godzina 20'] = np.where(DataFrameSeventh['date'].dt.hour == 20, 1, 0)
DataFrameSeventh['godzina 21'] = np.where(DataFrameSeventh['date'].dt.hour == 21, 1, 0)
DataFrameSeventh['godzina 22'] = np.where(DataFrameSeventh['date'].dt.hour == 22, 1, 0)
DataFrameSeventh['godzina 23'] = np.where(DataFrameSeventh['date'].dt.hour == 23, 1, 0)

DataFrameSeventhBeforeShuffled = DataFrameSeventh
DataFrameSeventh = shuffle(DataFrameSeventh)

DataFrameSeventhInput = DataFrameSeventh[['temperatura', 'wilgotnosc', 'predkosc wiatru','rain','fog','mist','ones',
                                      'tempPoprzednia','wilgPoprzednia','predkPoprzednia','west', 'wsw', 'wnw', 'variable',
                                      'south', 'sw', 'ssw',
                                      'sse', 'se', 'north', 'nw', 'nnw', 'nne', 'ne', 'east', 'ese', 'ene',

                                        'godzina 0', 'godzina 1','godzina 2','godzina 3','godzina 4',
'godzina 5','godzina 6','godzina 7','godzina 8','godzina 9','godzina 10','godzina 11','godzina 12','godzina 13',
'godzina 14','godzina 15','godzina 16','godzina 17','godzina 18','godzina 19','godzina 20','godzina 21','godzina 22',
'godzina 23'
 ]]

DataFrameSeventhOutput = DataFrameSeventh['PM10']


DataFrameSeventhInput = np.array(DataFrameSeventhInput)
DataFrameSeventhOutput = np.array(DataFrameSeventhOutput)

dataFrameInputTrain = DataFrameSeventhInput[0:7000]
dataFrameOutputTrain = DataFrameSeventhOutput[0:7000]

dataFrameInputTest = DataFrameSeventhInput[7000:]
dataFrameOutputTest = DataFrameSeventhOutput[7000:]

w = policzW(dataFrameInputTrain, dataFrameOutputTrain)
dataFrameOutputHat = policzPredykcje(w,dataFrameInputTest)

r2 = policzR2(dataFrameOutputTest, dataFrameOutputHat)
print "7. Moje r_squared pogoda + pogoda_hist + warunki + wiatr + wiatr_hist + godzina:", r2
print "7. Moje blWzgl pogoda + pogoda_hist + warunki + wiatr + wiatr_hist + godzina:",  policzBladWzgledny(dataFrameOutputHat, dataFrameOutputTest)

##2. ICH
regr = linear_model.LinearRegression()
regr.fit(dataFrameInputTest, dataFrameOutputTest)
predictedOutput = regr.predict(dataFrameInputTest)

print "7.rsquared implementacja ich",regr.score(dataFrameInputTest, dataFrameOutputTest)
print "7. blWzgl pogoda + pogoda_hist + warunki + wiatr + wiatr_hist + godzina: ich",policzBladWzgledny(predictedOutput, dataFrameOutputTest)


###REGUL:

regr = linear_model.Ridge()
regr.fit(dataFrameInputTest, dataFrameOutputTest)
predictedOutput = regr.predict(dataFrameInputTest)
print "Lasso",regr.score(dataFrameInputTest, dataFrameOutputTest)
print "Lasso",policzBladWzgledny(predictedOutput, dataFrameOutputTest)


##############################################Poprzedni + miesiac #####################################

DataFrameEight = DataFrameSeventhBeforeShuffled


DataFrameEight['styczen'] =  np.where(DataFrameEight['date'].dt.month == 1, 1, 0)
DataFrameEight['luty'] =np.where(DataFrameEight['date'].dt.month == 2, 1, 0)
DataFrameEight['marzec'] = np.where(DataFrameEight['date'].dt.month == 3, 1, 0)
DataFrameEight['kwiecien'] = np.where(DataFrameEight['date'].dt.month == 4, 1, 0)
DataFrameEight['maj'] = np.where(DataFrameEight['date'].dt.month == 5, 1, 0)
DataFrameEight['czerwiec'] = np.where(DataFrameEight['date'].dt.month == 6, 1, 0)
DataFrameEight['lipiec'] = np.where(DataFrameEight['date'].dt.month == 7, 1, 0)
DataFrameEight['sierpien'] = np.where(DataFrameEight['date'].dt.month == 8, 1, 0)
DataFrameEight['wrzesien'] = np.where(DataFrameEight['date'].dt.month == 9, 1, 0)
DataFrameEight['pazdziernik'] = np.where(DataFrameEight['date'].dt.month == 10, 1, 0)
DataFrameEight['listopad'] = np.where(DataFrameEight['date'].dt.month == 11, 1, 0)
DataFrameEight['grudzien'] = np.where(DataFrameEight['date'].dt.month == 12, 1, 0)


DataFrameEightBeforeShuffled = DataFrameEight
DataFrameEight = shuffle(DataFrameEight)

DataFrameEightInput = DataFrameEight[['temperatura', 'wilgotnosc', 'predkosc wiatru','rain','fog','mist','ones',
                                      'tempPoprzednia','wilgPoprzednia','predkPoprzednia','west', 'wsw', 'wnw', 'variable',
                                      'south', 'sw', 'ssw',
                                      'sse', 'se', 'north', 'nw', 'nnw', 'nne', 'ne', 'east', 'ese', 'ene',

                                        'godzina 0', 'godzina 1','godzina 2','godzina 3','godzina 4',
'godzina 5','godzina 6','godzina 7','godzina 8','godzina 9','godzina 10','godzina 11','godzina 12','godzina 13',
'godzina 14','godzina 15','godzina 16','godzina 17','godzina 18','godzina 19','godzina 20','godzina 21','godzina 22',
'godzina 23','styczen','luty','marzec','kwiecien','maj','czerwiec','lipiec','sierpien','wrzesien','pazdziernik',
'listopad', 'grudzien'
 ]]

DataFrameEightOutput = DataFrameEight['PM10']


DataFrameEightInput = np.array(DataFrameEightInput)
DataFrameEightOutput = np.array(DataFrameEightOutput)

dataFrameInputTrain = DataFrameEightInput[0:7000]
dataFrameOutputTrain = DataFrameEightOutput[0:7000]

dataFrameInputTest = DataFrameEightInput[7000:]
dataFrameOutputTest = DataFrameEightOutput[7000:]

w = policzW(dataFrameInputTrain, dataFrameOutputTrain)
dataFrameOutputHat = policzPredykcje(w,dataFrameInputTest)
r2 = policzR2(dataFrameOutputTest, dataFrameOutputHat)
print "8. Moje r_squared pogoda + pogoda_hist + warunki + wiatr + wiatr_hist + godzina + miesiac:", r2
print "8. Moje blWzgl pogoda + pogoda_hist + warunki + wiatr + wiatr_hist + godzina + miesiac:",  policzBladWzgledny(dataFrameOutputHat, dataFrameOutputTest)

##2. ICH
regr = linear_model.LinearRegression()
regr.fit(dataFrameInputTest, dataFrameOutputTest)
predictedOutput = regr.predict(dataFrameInputTest)
print "8.rsquared implementacja ich",regr.score(dataFrameInputTest, dataFrameOutputTest)
print "8. blWzgl pogoda + pogoda_hist + warunki + wiatr + wiatr_hist + godzina + miesiac: ich",policzBladWzgledny(predictedOutput, dataFrameOutputTest)


###REGUL:

regr = linear_model.Ridge()
regr.fit(dataFrameInputTest, dataFrameOutputTest)
predictedOutput = regr.predict(dataFrameInputTest)
print "Lasso",regr.score(dataFrameInputTest, dataFrameOutputTest)
print "Lasso",policzBladWzgledny(predictedOutput, dataFrameOutputTest)

############################################################MODEL FINALNY BEZ prevPM10 ALE Z CISN. I ZACHMURZENIEM############

DataFrameNinth = DataFrameEight

DataFrameNinth = DataFrameNinth.reset_index(drop=True)

DataFrameNinthInput = DataFrameNinth[['temperatura', 'wilgotnosc', 'predkosc wiatru','rain','fog','mist','ones',
                                      'tempPoprzednia','wilgPoprzednia','predkPoprzednia','west', 'wsw', 'wnw', 'variable',
                                      'south', 'sw', 'ssw',
                                      'sse', 'se', 'north', 'nw', 'nnw', 'nne', 'ne', 'east', 'ese', 'ene',

                                        'godzina 0', 'godzina 1','godzina 2','godzina 3','godzina 4',
'godzina 5','godzina 6','godzina 7','godzina 8','godzina 9','godzina 10','godzina 11','godzina 12','godzina 13',
'godzina 14','godzina 15','godzina 16','godzina 17','godzina 18','godzina 19','godzina 20','godzina 21','godzina 22',
'godzina 23','styczen','luty','marzec','kwiecien','maj','czerwiec','lipiec','sierpien','wrzesien','pazdziernik',
'listopad', 'grudzien', 'cisnienie']]


DataFrameNinthOutput = DataFrameNinth['PM10']

DataFrameNinthInput = np.array(DataFrameNinthInput)
DataFrameNinthOutput = np.array(DataFrameNinthOutput)

dataFrameInputTrain = DataFrameNinthInput[0:7000]
dataFrameOutputTrain = DataFrameNinthOutput[0:7000]

dataFrameInputTest = DataFrameNinthInput[7000:]
dataFrameOutputTest = DataFrameNinthOutput[7000:]

w = policzW(dataFrameInputTrain, dataFrameOutputTrain)
dataFrameOutputHat = policzPredykcje(w,dataFrameInputTest)
r2 = policzR2(dataFrameOutputTest, dataFrameOutputHat)


print "Model numer 9. Wartość R^2  dla regresji typu 1: ", r2
print "Model numer 9. Wartość błędu względnego dla regresji typu 1: ", policzBladWzgledny(dataFrameOutputHat, dataFrameOutputTest)

##2. ICH
regr = linear_model.LinearRegression()
regr.fit(dataFrameInputTest, dataFrameOutputTest)
predictedOutput = regr.predict(dataFrameInputTest)
print "Model numer 9. Wartość R^2  dla regresji typu 2: ",regr.score(dataFrameInputTest, dataFrameOutputTest)
print "Model numer 9. Wartość błędu względnego dla regresji typu 2: ",policzBladWzgledny(predictedOutput, dataFrameOutputTest)


###REGUL:

regr = linear_model.Ridge()
regr.fit(dataFrameInputTest, dataFrameOutputTest)
predictedOutput = regr.predict(dataFrameInputTest)
print "Model numer 9. Wartość R^2 dla regresji typu 2 przy wykorzystaniu regularyzacji L2: ",regr.score(dataFrameInputTest, dataFrameOutputTest)
print "Model numer 9. Wartość błędu względnego dla regresju typu 2 przy wykorzystaniu regularyzacji L2: ",policzBladWzgledny(predictedOutput, dataFrameOutputTest)

###################################################FINALNE DODANIE WAR.POG########################################

DataFrameTenth = DataFrameEightBeforeShuffled

DataFrameTenth= DataFrameTenth.reset_index(drop=True)
prevPM10 = DataFrameTenth[0:-1]['PM10']



DataFrameTenthInput = DataFrameTenth[['temperatura', 'wilgotnosc', 'predkosc wiatru','rain','fog','mist','ones',
                                      'tempPoprzednia','wilgPoprzednia','predkPoprzednia','west', 'wsw', 'wnw', 'variable',
                                      'south', 'sw', 'ssw',
                                      'sse', 'se', 'north', 'nw', 'nnw', 'nne', 'ne', 'east', 'ese', 'ene',

                                        'godzina 0', 'godzina 1','godzina 2','godzina 3','godzina 4',
'godzina 5','godzina 6','godzina 7','godzina 8','godzina 9','godzina 10','godzina 11','godzina 12','godzina 13',
'godzina 14','godzina 15','godzina 16','godzina 17','godzina 18','godzina 19','godzina 20','godzina 21','godzina 22',
'godzina 23','styczen','luty','marzec','kwiecien','maj','czerwiec','lipiec','sierpien','wrzesien','pazdziernik',
'listopad', 'grudzien', 'cisnienie','partly cloudy', 'overcast', 'clear', 'scattered clouds', 'mostly cloudy',
                                      'unknown','ones','cisnPoprzednie']]


DataFrameTenthInput = DataFrameTenthInput[1:]
DataFrameTenthInput = DataFrameTenthInput.reset_index(drop=True)
DataFrameTenthInput['prevPM10'] = prevPM10
DataFrameTenthInputBef = DataFrameTenthInput


DataFrameTenthInput = np.array(DataFrameTenthInput)
DataFrameTenthOutput = DataFrameTenth[['PM10']][1:]
DataFrameTenethOutpBef = DataFrameTenthOutput

DataFrameTenthOutput = np.array(DataFrameTenthOutput.reset_index(drop=True))

df = np.concatenate((DataFrameTenthInput, DataFrameTenthOutput),axis = 1)
df = shuffle(df)
DataFrameTenthInput = df[:,:-1]
DataFrameTenthOutput = df[:,-1]


DataFrameTenthInput = np.array(DataFrameTenthInput)
DataFrameTenthOutput = np.array(DataFrameTenthOutput)

dataFrameInputTrain = DataFrameTenthInput[0:7000]
dataFrameOutputTrain = DataFrameTenthOutput[0:7000]

dataFrameInputTest = DataFrameTenthInput[7000:]
dataFrameOutputTest = DataFrameTenthOutput[7000:]

w = policzW(dataFrameInputTrain, dataFrameOutputTrain)
dataFrameOutputHat = policzPredykcje(w,dataFrameInputTest)
r2 = policzR2(dataFrameOutputTest, dataFrameOutputHat)


print "10. Moje r_squared pogoda + pogoda_hist + warunki + wiatr + wiatr_hist + godzina + miesiac + cisnienie:", r2
print "10. Moje blWzgl pogoda + pogoda_hist + warunki + wiatr + wiatr_hist + godzina + miesiac+ cisnienie:", policzBladWzgledny(dataFrameOutputHat, dataFrameOutputTest)

##2. ICH
regr = linear_model.LinearRegression()
regr.fit(dataFrameInputTest, dataFrameOutputTest)
predictedOutput = regr.predict(dataFrameInputTest)

print "10.rsquared implementacja ich",regr.score(dataFrameInputTest, dataFrameOutputTest)
print "10. blWzgl pogoda + pogoda_hist + warunki + wiatr + wiatr_hist + godzina + miesiac+cisn: ich",policzBladWzgledny(predictedOutput, dataFrameOutputTest)

##############################SPR. % PRZEWID TENDENCJI:

DataFrameTenthInputBef = pd.DataFrame(DataFrameTenthInputBef)
DataFrameTenethOutpBef = pd.DataFrame(DataFrameTenethOutpBef)


concatDF = np.concatenate((DataFrameTenthInputBef, DataFrameTenethOutpBef), 1)
concatDF = pd.DataFrame(concatDF)
concatDF.to_sql(con=conn, name="testt", if_exists="replace")



tend = TendencyCreator()
arrWholeData = tend.getClassifierForWholeDataFrame(concatDF)
dataFrameTrain, dataFrameTest, testIndexes, trainIndexes, testCatValues = tend.divideOnTestAndTrainData(concatDF)

print "testCatValues"
print testCatValues
dataFrameYTrain = pd.DataFrame(dataFrameTrain.iloc[:,-1])

XtrainNumpy = np.array(dataFrameTrain.iloc[:,:-1])
YtrainNumpy = np.array(dataFrameTrain.iloc[:,-1])
XtestNumpy = np.array(dataFrameTest.iloc[:,:-1])

regr = linear_model.LinearRegression()
regr.fit(XtrainNumpy,YtrainNumpy)
predictedOutput = regr.predict(XtestNumpy)
dataFrameYTrain.columns = ['PM10']

dataFrameOutputPredicted = pd.DataFrame(data=predictedOutput, index=testIndexes)
dataFrameOutputPredicted.columns = ['PM10']

dataFrameConcatenatedWithPredictedValues = pd.concat([dataFrameYTrain, dataFrameOutputPredicted], axis = 0)
dataFrameConcatenatedWithPredictedValues = dataFrameConcatenatedWithPredictedValues.sort_index()

dataFrameConcatenatedWithPredictedValues.to_sql(con=conn, name="przewidzianaInormalnaConcat", if_exists="replace")

tendencyArrForPredictedDataFrame = tend.createCatValArray(dataFrameConcatenatedWithPredictedValues)



tendencyArrForRealDataFrame = tend.createCatValArray(concatDF) #dla normalnego dataframe

print "Indeksy testowe - określa numery indeksów dla których dokonywana była klasyfikacja : "
print testIndexes

print "Tablica rzeczywistych tendencji : "
print testCatValues

tendencyForTest = [k for k in map(lambda x : tendencyArrForPredictedDataFrame[x], testIndexes)]

print "Tablica prognozowanych tendencji : "
print tendencyForTest


accuracy = accuracy_score(testCatValues, tendencyForTest)
print "Skuteczność klasyfikacji : "
print accuracy * 100, "%"

