# -*- coding: utf-8 -*-

# implementacja sieci neuronowej zaczerpnieta z
# https://github.com/stephencwelch/Neural-Networks-Demystified


from __future__ import unicode_literals

from scipy import optimize
import numpy as np
from neuralNetwork import Neural_Network
import matplotlib.pyplot as plt
import sqlite3
from sklearn import preprocessing
import pandas as pd
from sklearn.utils import shuffle


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

mainDataFrame = dataFrame[['temperatura','wilgotnosc','predkosc wiatru','cisnienie','PM10','date','warunki pogodowe','kierunek wiatru']]

###############################################DODANIE POPRZEDNICH WARTOSCI######################################################

mainDataFrame = mainDataFrame.reset_index(drop=True)


#########################################KONIEC DODANIA POPRZEDNICH WARTOSCI#######################################################


mainDataFrame = mainDataFrame.dropna(axis = 0, how ='any')
mainDataFrameInput = mainDataFrame [['date','temperatura','cisnienie','wilgotnosc','predkosc wiatru','warunki pogodowe','kierunek wiatru','PM10' ]]
mainDataFrameInput = mainDataFrameInput.reset_index(drop=True)

#########################################DODANIE ONE HOT ENCODING - GODZINA########################################################


mainDataFrameInput['godzina 0'] = np.where(mainDataFrameInput['date'].dt.hour == 0, 1, 0)
mainDataFrameInput['godzina 1'] = np.where(mainDataFrameInput['date'].dt.hour == 1, 1, 0)
mainDataFrameInput['godzina 2'] = np.where(mainDataFrameInput['date'].dt.hour == 2, 1, 0)
mainDataFrameInput['godzina 3'] = np.where(mainDataFrameInput['date'].dt.hour == 3, 1, 0)
mainDataFrameInput['godzina 4'] = np.where(mainDataFrameInput['date'].dt.hour == 4, 1, 0)
mainDataFrameInput['godzina 5'] = np.where(mainDataFrameInput['date'].dt.hour == 5, 1, 0)
mainDataFrameInput['godzina 6'] = np.where(mainDataFrameInput['date'].dt.hour == 6, 1, 0)
mainDataFrameInput['godzina 7'] = np.where(mainDataFrameInput['date'].dt.hour == 7, 1, 0)
mainDataFrameInput['godzina 8'] = np.where(mainDataFrameInput['date'].dt.hour == 8, 1, 0)
mainDataFrameInput['godzina 9'] = np.where(mainDataFrameInput['date'].dt.hour == 9, 1, 0)
mainDataFrameInput['godzina 10'] = np.where(mainDataFrameInput['date'].dt.hour == 10, 1, 0)
mainDataFrameInput['godzina 11'] = np.where(mainDataFrameInput['date'].dt.hour == 11, 1, 0)
mainDataFrameInput['godzina 12'] = np.where(mainDataFrameInput['date'].dt.hour == 12, 1, 0)
mainDataFrameInput['godzina 13'] = np.where(mainDataFrameInput['date'].dt.hour == 13, 1, 0)
mainDataFrameInput['godzina 14'] = np.where(mainDataFrameInput['date'].dt.hour == 14, 1, 0)
mainDataFrameInput['godzina 15'] = np.where(mainDataFrameInput['date'].dt.hour == 15, 1, 0)
mainDataFrameInput['godzina 16'] = np.where(mainDataFrameInput['date'].dt.hour == 16, 1, 0)
mainDataFrameInput['godzina 17'] = np.where(mainDataFrameInput['date'].dt.hour == 17, 1, 0)
mainDataFrameInput['godzina 18'] = np.where(mainDataFrameInput['date'].dt.hour == 18, 1, 0)
mainDataFrameInput['godzina 19'] = np.where(mainDataFrameInput['date'].dt.hour == 19, 1, 0)
mainDataFrameInput['godzina 20'] = np.where(mainDataFrameInput['date'].dt.hour == 20, 1, 0)
mainDataFrameInput['godzina 21'] = np.where(mainDataFrameInput['date'].dt.hour == 21, 1, 0)
mainDataFrameInput['godzina 22'] = np.where(mainDataFrameInput['date'].dt.hour == 22, 1, 0)
mainDataFrameInput['godzina 23'] = np.where(mainDataFrameInput['date'].dt.hour == 23, 1, 0)
#
mainDataFrameInput['styczen'] =  np.where(mainDataFrameInput['date'].dt.month == 1, 1, 0)
mainDataFrameInput['luty'] =np.where(mainDataFrameInput['date'].dt.month == 2, 1, 0)
mainDataFrameInput['marzec'] = np.where(mainDataFrameInput['date'].dt.month == 3, 1, 0)
mainDataFrameInput['kwiecien'] = np.where(mainDataFrameInput['date'].dt.month == 4, 1, 0)
mainDataFrameInput['maj'] = np.where(mainDataFrameInput['date'].dt.month == 5, 1, 0)
mainDataFrameInput['czerwiec'] = np.where(mainDataFrameInput['date'].dt.month == 6, 1, 0)
mainDataFrameInput['lipiec'] = np.where(mainDataFrameInput['date'].dt.month == 7, 1, 0)
mainDataFrameInput['sierpien'] = np.where(mainDataFrameInput['date'].dt.month == 8, 1, 0)
mainDataFrameInput['wrzesien'] = np.where(mainDataFrameInput['date'].dt.month == 9, 1, 0)
mainDataFrameInput['pazdziernik'] = np.where(mainDataFrameInput['date'].dt.month == 10, 1, 0)
mainDataFrameInput['listopad'] = np.where(mainDataFrameInput['date'].dt.month == 11, 1, 0)
mainDataFrameInput['grudzien'] = np.where(mainDataFrameInput['date'].dt.month == 12, 1, 0)
#
mainDataFrameInput = mainDataFrameInput.drop('date',1)

# #######################################################ONE HOT ENCODING DATA KONIEC####################################################
#
# ######################################################ONE HOT ENCODING WARUNKI POGODOWE POCZATEK#######################################
mainDataFrameInput['rain'] = np.where((mainDataFrameInput['warunki pogodowe'].str.contains("Rain")) | (mainDataFrameInput['warunki pogodowe'].str.contains("Drizzle")) | (mainDataFrameInput['warunki pogodowe'].str.contains("Thunderstorm")) | (mainDataFrameInput['warunki pogodowe'].str.contains("Hail")),1,0)
mainDataFrameInput['fog'] = np.where( mainDataFrameInput['warunki pogodowe'].str.contains("Fog"),1, 0)
mainDataFrameInput['mist'] = np.where(mainDataFrameInput['warunki pogodowe'].str.contains("Mist"),1, 0)
mainDataFrameInput['snow'] = np.where(mainDataFrameInput['warunki pogodowe'].str.contains("Snow"),1, 0)
mainDataFrameInput['partly cloudy'] = np.where(mainDataFrameInput['warunki pogodowe'].str.contains("Partly Cloudy"),1, 0)
mainDataFrameInput['overcast'] = np.where(mainDataFrameInput['warunki pogodowe'].str.contains("Overcast"),1, 0)
mainDataFrameInput['clear'] = np.where(mainDataFrameInput['warunki pogodowe'].str.contains("Clear"),1, 0)
mainDataFrameInput['scattered clouds'] = np.where(mainDataFrameInput['warunki pogodowe'].str.contains("Scattered Clouds"),1, 0)
mainDataFrameInput['mostly cloudy'] = np.where(mainDataFrameInput['warunki pogodowe'].str.contains("Mostly Cloudy"),1, 0)
mainDataFrameInput['unknown'] = np.where(mainDataFrameInput['warunki pogodowe'].str.contains("Unknown"),1,0)

mainDataFrameInput = mainDataFrameInput.reset_index(drop=True)

poprzPM10 = mainDataFrameInput['PM10'][0:-1]
poprzCisn = mainDataFrameInput['cisnienie'][0:-1]
poprzWilg = mainDataFrameInput ['wilgotnosc'][0:-1]
poprzSilaWiatru = mainDataFrameInput ['predkosc wiatru'][0:-1]
poprzTemp = mainDataFrameInput ['temperatura'][0:-1]

poprzRain = mainDataFrameInput['rain'][0:-1]
poprzFog = mainDataFrameInput['fog'][0:-1]
poprzMist = mainDataFrameInput['mist'][0:-1]
poprzSnow = mainDataFrameInput['snow'][0:-1]
poprzPartlyCloudy = mainDataFrameInput['partly cloudy'][0:-1]
poprzOvercast = mainDataFrameInput ['overcast'][0:-1]
poprzClear = mainDataFrameInput ['clear'][0:-1]
poprzScatteredClouds = mainDataFrameInput['scattered clouds'][0:-1]
poprzMostlyCloudy = mainDataFrameInput ['mostly cloudy'][0:-1]
poprzUnknown = mainDataFrameInput['unknown'][0:-1]

mainDataFrameInput = mainDataFrameInput[1:]
mainDataFrameInput = mainDataFrameInput.reset_index(drop=True)

mainDataFrameInput = mainDataFrameInput.drop('PM10',1)
mainDataFrameInput ['poprzPM10'] = poprzPM10

mainDataFrameInput ['poprzRain'] = poprzRain
mainDataFrameInput ['poprzFog'] = poprzFog
mainDataFrameInput ['poprzMist'] = poprzMist
mainDataFrameInput ['poprzSnow'] = poprzSnow
mainDataFrameInput ['poprzPartlyCloudy'] = poprzPartlyCloudy
mainDataFrameInput ['poprzOvercast'] = poprzOvercast
mainDataFrameInput ['poprzClear'] = poprzClear
mainDataFrameInput ['poprzScatteredClouds'] = poprzScatteredClouds
mainDataFrameInput ['poprzMostlyCloudy'] = poprzMostlyCloudy
mainDataFrameInput ['poprzUnknown'] = poprzUnknown
mainDataFrameInput ['poprzCisn'] = poprzCisn
mainDataFrameInput ['poprzWilg'] = poprzWilg
mainDataFrameInput ['poprzSilaWiatru'] = poprzSilaWiatru
mainDataFrameInput ['poprzTemp'] = poprzTemp
mainDataFrameInput = mainDataFrameInput.drop('warunki pogodowe',1)

# ####################################################ONE HOT ENCODING WARUNKI POGODOWE KONIEC##########################################
#
#
# #################################################ONE HOT ENCODING KIERUNEK WIATRU POCZATEK########################################
mainDataFrameInput['west'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("West"), 1, 0)
mainDataFrameInput['wsw'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("WSW"), 1, 0)
mainDataFrameInput['wnw'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("WNW"), 1, 0)
mainDataFrameInput['variable'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("Variable"), 1, 0)
mainDataFrameInput['south'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("South"), 1, 0)
mainDataFrameInput['sw'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("SW"), 1, 0)
mainDataFrameInput['ssw'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("SSW"), 1, 0)
mainDataFrameInput['sse'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("SSE"), 1, 0)
mainDataFrameInput['se'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("SE"), 1, 0)
mainDataFrameInput['north'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("North"), 1, 0)
mainDataFrameInput['nw'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("NW"), 1, 0)
mainDataFrameInput['nnw'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("NNW"), 1, 0)
mainDataFrameInput['nne'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("NNE"), 1, 0)
mainDataFrameInput['ne'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("NE"), 1, 0)
mainDataFrameInput['east'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("East"), 1, 0)
mainDataFrameInput['ese'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("ESE"), 1, 0)
mainDataFrameInput['ene'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("ENE"), 1, 0)

mainDataFrameInput = mainDataFrameInput.drop('kierunek wiatru',1)


westHist = mainDataFrameInput[0:-1]['west']
wswHist = mainDataFrameInput[0:-1]['wsw']
wnwHist= mainDataFrameInput[0:-1]['wnw']
variableHist = mainDataFrameInput[0:-1]['variable']
southHist = mainDataFrameInput[0:-1]['south']
swHist = mainDataFrameInput[0:-1]['sw']
sswHist = mainDataFrameInput[0:-1]['ssw']
sseHist = mainDataFrameInput[0:-1]['sse']
seHist = mainDataFrameInput[0:-1]['se']
northHist = mainDataFrameInput[0:-1]['north']
nwHist = mainDataFrameInput[0:-1]['nw']
nnwHist = mainDataFrameInput[0:-1]['nnw']
nneHist = mainDataFrameInput[0:-1]['nne']
neHist = mainDataFrameInput[0:-1]['ne']
eastHist = mainDataFrameInput[0:-1]['east']
eseHist = mainDataFrameInput[0:-1]['ese']
eneHist = mainDataFrameInput[0:-1]['ene']

mainDataFrameInput = mainDataFrameInput [1:]
mainDataFrameInput = mainDataFrameInput.reset_index(drop=True)

mainDataFrameInput['westHist'] = westHist
mainDataFrameInput['wswHist'] = wswHist
mainDataFrameInput['wnwHsit'] = wnwHist
mainDataFrameInput['variableHist'] = variableHist
mainDataFrameInput['southHist'] = southHist
mainDataFrameInput['swHist'] = swHist
mainDataFrameInput['sswHist'] = sswHist
mainDataFrameInput['sseHist'] = sseHist
mainDataFrameInput['seHist'] = seHist
mainDataFrameInput['northHist'] = northHist
mainDataFrameInput['nwHist'] = nwHist
mainDataFrameInput['nnwHist'] = nnwHist
mainDataFrameInput['nneHist'] = nneHist
mainDataFrameInput['neHist'] = neHist
mainDataFrameInput['eastHist'] = eastHist
mainDataFrameInput['eseHist'] = eseHist
mainDataFrameInput['eneHist'] = eneHist


#############################################ONE HOT ENCODING KIERUNEK WIATRU KONIEC##############################################

mainDataFrameInput = mainDataFrameInput.reset_index(drop=True)

mainDataFrameOutput = mainDataFrame [2:][['PM10']]
mainDataFrameOutput = mainDataFrameOutput.reset_index(drop=True)

df = np.concatenate((mainDataFrameInput, mainDataFrameOutput), axis = 1)

df = shuffle(df)
mainDataFrameInput = df[:,0:-1]
mainDataFrameOutput = df [:,-1]


min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0,1))
mainDataFrameInput = min_max_scaler.fit_transform(mainDataFrameInput)
training_inputs = [np.reshape(x, (99, 1)) for x in mainDataFrameInput]

# mainDataFrameOutput = mainDataFrameOutput.values
minOutp = min(mainDataFrameOutput)
maxOutp = max(mainDataFrameOutput)

mainDataFrameOutput = min_max_scaler.fit_transform(mainDataFrameOutput)
training_outputs = [np.reshape(x, (1, 1)) for x in mainDataFrameOutput]

training_inputs = np.array(training_inputs)
training_outputs = np.array(training_outputs)


nowaTablicaInput = np.zeros([training_inputs.shape[0],training_inputs.shape[1]])
for index,row in enumerate (training_inputs,start=0):
    temporaryRowList = []
    for element in row:
        temporaryRowList.append(float(element))
    nowaTablicaInput[index,:] = temporaryRowList


nowaTablicaOutput = np.zeros([training_outputs.shape[0],training_outputs.shape[1]])
for index,row in enumerate (training_outputs,start=0):
    temporaryRowList = []
    for element in row:
        temporaryRowList.append(float(element))
    nowaTablicaOutput[index,:] = temporaryRowList




nowaTablicaInputTrain = nowaTablicaInput[0:7000]

nowaTablicaInputTrain = np.array(nowaTablicaInputTrain)
ones = np.ones((nowaTablicaInputTrain.shape[0], 1))
nowaTablicaInputTrain = np.concatenate((nowaTablicaInputTrain, ones), 1)


nowaTablicaInputTest = nowaTablicaInput[7000:]
nowaTablicaInputTest = np.array(nowaTablicaInputTest)
ones = np.ones((nowaTablicaInputTest.shape[0], 1))
nowaTablicaInputTest = np.concatenate((nowaTablicaInputTest, ones), 1)

nowaTablicaOutputTrain = nowaTablicaOutput[0:7000]
nowaTablicaOutputTest = nowaTablicaOutput[7000:]



treningowaInp = nowaTablicaInputTrain
treningowaOutp = nowaTablicaOutputTrain
testowaInp = nowaTablicaInputTest
testowaOutp = nowaTablicaOutputTest

class trainer(object):
    def __init__(self, N):
        self.N = N

    def callbackF(self, params):
        self.N.setParams(params)

        yHat, y = self.N.returnerYAndYhat(self.testX, self.testY)
        tempRelativeErr = []
        for i in range(0, len(y)):
            if y[i]!=0:
                diff = maxOutp - minOutp
                absoluteErr = abs(yHat[i]*diff - y[i]*diff)
                relativeError = absoluteErr/(y[i]*diff)
                tempRelativeErr.append(relativeError)

        relativeAvg = sum(tempRelativeErr)/len(tempRelativeErr)
        self.errorTest.append(relativeAvg)

    def costFunctionWrapper(self, params, X, y):

        self.N.setParams(params)
        cost = self.N.costFunction(X, y)
        grad = self.N.computeGradients(X, y)

        return cost, grad

    def train(self, trainX, trainY, testX, testY):
        self.trainX = trainX
        self.trainY = trainY
        self.testX = testX
        self.testY = testY
        self.J = []
        self.JTest = []
        self.errorTrain = []
        self.errorTest = []

        params0 = self.N.getParams()

        options = {'maxiter': 2, 'disp': True}
        _res = optimize.minimize(self.costFunctionWrapper, params0, jac=True, method='BFGS', \
                                 args=(trainX, trainY), options=options, callback=self.callbackF)

        self.N.setParams(_res.x)

inputLayerSize = 100
outputLayerSize = 1
hiddenLayerSize = 50
w1 = np.random.randn(inputLayerSize, hiddenLayerSize)
w2 = np.random.randn(hiddenLayerSize, outputLayerSize)



NN = Neural_Network(Lambda=0.0)
NN.setWeightsAsArrays(w1=w1, w2=w2)
diff = maxOutp - minOutp
firstErr = NN.returnFirstError(testowaInp, testowaOutp,diff) * 100
T = trainer(NN)
T.train(treningowaInp,treningowaOutp,testowaInp,testowaOutp)

errorWithoutRegularization = [i * 100 for i in T.errorTest]
print T.errorTest
print T.errorTest[-1]


x = range(1,3,1)
plt.plot(x, errorWithoutRegularization,color = 'g')
plt.xticks(np.arange(min(x), max(x)+1, 5.0), fontsize = 14)
plt.yticks(fontsize = 14)
plt.legend( prop={'size': 16})
plt.grid(1)
plt.xlabel('Numer iteracji', fontsize = 20)
plt.ylabel('Średni błąd względny [%]', fontsize = 20)
plt.title('Badanie błędu względnego predykcji stężenia pyłu $PM_{10}$ przy użyciu sieci neuronowej dla modelu numer 8', fontsize = 14)
plt.show()

centile_5th = np.percentile(T.errorTest, 5)
centile_25th = np.percentile(T.errorTest, 25)
centile_50th = np.percentile(T.errorTest, 50)
centile_75th = np.percentile(T.errorTest, 75)
centile_95th = np.percentile(T.errorTest, 95)


