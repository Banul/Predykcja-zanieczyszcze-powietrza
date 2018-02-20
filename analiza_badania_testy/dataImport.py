import sqlite3
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.utils import shuffle

# klasa sluzaca do pobierania danych
#


class DataGetter(object):
    def getData(self):
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
        mainDataFrame = dataFrame[['temperatura','wilgotnosc','predkosc wiatru','cisnienie','PM25','PM10','date','warunki pogodowe','kierunek wiatru']]
        mainDataFrame = mainDataFrame.dropna(axis = 0, how ='any')
        mainDataFrame = mainDataFrame.reset_index(drop=True)

        mainDataFrameInput = mainDataFrame [['temperatura','wilgotnosc','predkosc wiatru','cisnienie','date','warunki pogodowe','kierunek wiatru']]
        onesColumn = np.ones((len(mainDataFrameInput), 1))
        mainDataFrameInput['ones'] = onesColumn

        # ###########################ONE HOT ENCODING BEGIN - DATA###########################################
        tempPoprzednia = mainDataFrameInput[0:-1]['temperatura']
        wilgPoprzednia = mainDataFrame[0:-1]['wilgotnosc']
        predkoscWiatruPoprzednia = mainDataFrame[0:-1]['predkosc wiatru']
        cisnPoprzednie = mainDataFrame[0:-1]['cisnienie']

        mainDataFrameInput = mainDataFrameInput[1:]
        mainDataFrameInput = mainDataFrameInput.reset_index(drop=True)

        mainDataFrameInput['temperaturaPoprzednia'] = tempPoprzednia
        mainDataFrameInput['wilgotnoscPoprzednia'] = wilgPoprzednia
        mainDataFrameInput['predkoscWiatruPoprzednia'] = predkoscWiatruPoprzednia
        mainDataFrameInput['cisnPoprzednie'] = cisnPoprzednie

        # mainDataFrameInput['godzina 0'] = np.where(mainDataFrameInput['date'].dt.hour == 0, 1, 0)
        # mainDataFrameInput['godzina 1'] = np.where(mainDataFrameInput['date'].dt.hour == 1, 1, 0)
        # mainDataFrameInput['godzina 2'] = np.where(mainDataFrameInput['date'].dt.hour == 2, 1, 0)
        # mainDataFrameInput['godzina 3'] = np.where(mainDataFrameInput['date'].dt.hour == 3, 1, 0)
        # mainDataFrameInput['godzina 4'] = np.where(mainDataFrameInput['date'].dt.hour == 4, 1, 0)
        # mainDataFrameInput['godzina 5'] = np.where(mainDataFrameInput['date'].dt.hour == 5, 1, 0)
        # mainDataFrameInput['godzina 6'] = np.where(mainDataFrameInput['date'].dt.hour == 6, 1, 0)
        # mainDataFrameInput['godzina 7'] = np.where(mainDataFrameInput['date'].dt.hour == 7, 1, 0)
        # mainDataFrameInput['godzina 8'] = np.where(mainDataFrameInput['date'].dt.hour == 8, 1, 0)
        # mainDataFrameInput['godzina 9'] = np.where(mainDataFrameInput['date'].dt.hour == 9, 1, 0)
        # mainDataFrameInput['godzina 10'] = np.where(mainDataFrameInput['date'].dt.hour == 10, 1, 0)
        # mainDataFrameInput['godzina 11'] = np.where(mainDataFrameInput['date'].dt.hour == 11, 1, 0)
        # mainDataFrameInput['godzina 12'] = np.where(mainDataFrameInput['date'].dt.hour == 12, 1, 0)
        # mainDataFrameInput['godzina 13'] = np.where(mainDataFrameInput['date'].dt.hour == 13, 1, 0)
        # mainDataFrameInput['godzina 14'] = np.where(mainDataFrameInput['date'].dt.hour == 14, 1, 0)
        # mainDataFrameInput['godzina 15'] = np.where(mainDataFrameInput['date'].dt.hour == 15, 1, 0)
        # mainDataFrameInput['godzina 16'] = np.where(mainDataFrameInput['date'].dt.hour == 16, 1, 0)
        # mainDataFrameInput['godzina 17'] = np.where(mainDataFrameInput['date'].dt.hour == 17, 1, 0)
        # mainDataFrameInput['godzina 18'] = np.where(mainDataFrameInput['date'].dt.hour == 18, 1, 0)
        # mainDataFrameInput['godzina 19'] = np.where(mainDataFrameInput['date'].dt.hour == 19, 1, 0)
        # mainDataFrameInput['godzina 20'] = np.where(mainDataFrameInput['date'].dt.hour == 20, 1, 0)
        # mainDataFrameInput['godzina 21'] = np.where(mainDataFrameInput['date'].dt.hour == 21, 1, 0)
        # mainDataFrameInput['godzina 22'] = np.where(mainDataFrameInput['date'].dt.hour == 22, 1, 0)
        # mainDataFrameInput['godzina 23'] = np.where(mainDataFrameInput['date'].dt.hour == 23, 1, 0)
        #
        # mainDataFrameInput['styczen'] = np.where(mainDataFrameInput['date'].dt.month == 1, 1, 0)
        # mainDataFrameInput['luty'] = np.where(mainDataFrameInput['date'].dt.month == 2, 1, 0)
        # mainDataFrameInput['marzec'] = np.where(mainDataFrameInput['date'].dt.month == 3, 1, 0)
        # mainDataFrameInput['kwiecien'] = np.where(mainDataFrameInput['date'].dt.month == 4, 1, 0)
        # mainDataFrameInput['maj'] = np.where(mainDataFrameInput['date'].dt.month == 5, 1, 0)
        # mainDataFrameInput['czerwiec'] = np.where(mainDataFrameInput['date'].dt.month == 6, 1, 0)
        # mainDataFrameInput['lipiec'] = np.where(mainDataFrameInput['date'].dt.month == 7, 1, 0)
        # mainDataFrameInput['sierpien'] = np.where(mainDataFrameInput['date'].dt.month == 8, 1, 0)
        # mainDataFrameInput['wrzesien'] = np.where(mainDataFrameInput['date'].dt.month == 9, 1, 0)
        # mainDataFrameInput['pazdziernik'] = np.where(mainDataFrameInput['date'].dt.month == 10, 1, 0)
        # mainDataFrameInput['listopad'] = np.where(mainDataFrameInput['date'].dt.month == 11, 1, 0)
        # mainDataFrameInput['grudzien'] = np.where(mainDataFrameInput['date'].dt.month == 12, 1, 0)
        #
        mainDataFrameInput = mainDataFrameInput.drop('date', 1)
        #
        #
        # #########################################ONE HOT ENCODING DATA- END#######################################
        #
        #
        # ##########################################ONE HOT ENCODING - WEATHER COND ###############################
        #
        # mainDataFrameInput['rain'] = np.where((mainDataFrameInput['warunki pogodowe'].str.contains("Rain")) | (
        #     mainDataFrameInput['warunki pogodowe'].str.contains("Drizzle")) | (
        #     mainDataFrameInput['warunki pogodowe'].str.contains("Thunderstorm")) | (
        #     mainDataFrameInput['warunki pogodowe'].str.contains("Hail")), 1, 0)
        # mainDataFrameInput['fog'] = np.where(mainDataFrameInput['warunki pogodowe'].str.contains("Fog"), 1, 0)
        # mainDataFrameInput['mist'] = np.where(mainDataFrameInput['warunki pogodowe'].str.contains("Mist"), 1, 0)
        # mainDataFrameInput['snow'] = np.where(mainDataFrameInput['warunki pogodowe'].str.contains("Snow"), 1, 0)
        # mainDataFrameInput['partly cloudy'] = np.where(mainDataFrameInput['warunki pogodowe'].str.contains("Partly Cloudy"), 1, 0)
        # mainDataFrameInput['overcast'] = np.where(mainDataFrameInput['warunki pogodowe'].str.contains("Overcast"), 1, 0)
        # mainDataFrameInput['clear'] = np.where(mainDataFrameInput['warunki pogodowe'].str.contains("Clear"), 1, 0)
        # mainDataFrameInput['scattered clouds'] = np.where(
        #     mainDataFrameInput['warunki pogodowe'].str.contains("Scattered Clouds"), 1, 0)
        # mainDataFrameInput['mostly cloudy'] = np.where(mainDataFrameInput['warunki pogodowe'].str.contains("Mostly Cloudy"), 1, 0)
        # mainDataFrameInput['unknown'] = np.where(mainDataFrameInput['warunki pogodowe'].str.contains("Unknown"), 1, 0)

        mainDataFrameInput = mainDataFrameInput.drop('warunki pogodowe',1)

        #
        # rainPoprz = mainDataFrameInput[0:-1]['rain']
        # fogPoprz = mainDataFrameInput[0:-1]['fog']
        # mistPoprz = mainDataFrameInput[0:-1]['mist']
        # snowPoprz = mainDataFrameInput[0:-1]['snow']
        # partlyCloudyPoprz = mainDataFrameInput[0:-1]['partly cloudy']
        # overcastPoprz = mainDataFrameInput[0:-1]['overcast']
        # clearPoprz = mainDataFrameInput[0:-1]['clear']
        # mostlyCloudyPoprz = mainDataFrameInput[0:-1]['mostly cloudy']
        # scatteredCloudsPoprz = mainDataFrameInput[0:-1]['scattered clouds']
        # unknownPoprz = mainDataFrameInput[0:-1]['unknown']
        #
        # mainDataFrameInput = mainDataFrameInput[1:]
        # mainDataFrameInput = mainDataFrameInput.reset_index(drop=True)
        #
        #
        #
        # mainDataFrameInput['rainPoprz'] = rainPoprz
        # mainDataFrameInput['fogPoprz'] =  fogPoprz
        # mainDataFrameInput['mistPoprz'] = mistPoprz
        # mainDataFrameInput['snowPoprz'] =  snowPoprz
        # mainDataFrameInput['partlyCloudyPoprz'] = partlyCloudyPoprz
        # mainDataFrameInput['overcastPoprz'] = overcastPoprz
        # mainDataFrameInput['clearPoprz'] = clearPoprz
        # mainDataFrameInput['mostlyCloudyPoprz'] = mostlyCloudyPoprz
        # mainDataFrameInput['scatteredCloudsPoprz'] = scatteredCloudsPoprz
        # mainDataFrameInput['unknownPoprz'] = unknownPoprz
        #
        #
        # #################################################ONE HOT ENCODING WEATHER COND - END ##################################
        #
        #
        # ################################################ONE HOT ENCODING WIND DIR #############################################
        #
        # mainDataFrameInput['west'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("West"), 1, 0)
        # mainDataFrameInput['wsw'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("WSW"), 1, 0)
        # mainDataFrameInput['wnw'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("WNW"), 1, 0)
        # mainDataFrameInput['variable'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("Variable"), 1, 0)
        # mainDataFrameInput['south'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("South"), 1, 0)
        # mainDataFrameInput['sw'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("SW"), 1, 0)
        # mainDataFrameInput['ssw'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("SSW"), 1, 0)
        # mainDataFrameInput['sse'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("SSE"), 1, 0)
        # mainDataFrameInput['se'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("SE"), 1, 0)
        # mainDataFrameInput['north'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("North"), 1, 0)
        # mainDataFrameInput['nw'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("NW"), 1, 0)
        # mainDataFrameInput['nnw'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("NNW"), 1, 0)
        # mainDataFrameInput['nne'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("NNE"), 1, 0)
        # mainDataFrameInput['ne'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("NE"), 1, 0)
        # mainDataFrameInput['east'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("East"), 1, 0)
        # mainDataFrameInput['ese'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("ESE"), 1, 0)
        # mainDataFrameInput['ene'] = np.where(mainDataFrameInput['kierunek wiatru'] == ("ENE"), 1, 0)
        #
        # westHist = mainDataFrameInput[0:-1]['west']
        # wswHist = mainDataFrameInput[0:-1]['wsw']
        # wnwHist = mainDataFrameInput[0:-1]['wnw']
        # variableHist = mainDataFrameInput[0:-1]['variable']
        # southHist = mainDataFrameInput[0:-1]['south']
        # swHist = mainDataFrameInput[0:-1]['sw']
        # sswHist = mainDataFrameInput[0:-1]['ssw']
        # sseHist = mainDataFrameInput[0:-1]['sse']
        # seHist = mainDataFrameInput[0:-1]['se']
        # northHist = mainDataFrameInput[0:-1]['north']
        # nwHist = mainDataFrameInput[0:-1]['nw']
        # nnwHist = mainDataFrameInput[0:-1]['nnw']
        # nneHist = mainDataFrameInput[0:-1]['nne']
        # neHist = mainDataFrameInput[0:-1]['ne']
        # eastHist = mainDataFrameInput[0:-1]['east']
        # eseHist = mainDataFrameInput[0:-1]['ese']
        # eneHist = mainDataFrameInput[0:-1]['ene']
        #
        # mainDataFrameInput = mainDataFrameInput[1:]
        # mainDataFrameInput = mainDataFrameInput.reset_index(drop=True)
        #
        # mainDataFrameInput['westHist'] = westHist
        # mainDataFrameInput['wswHist'] = wswHist
        # mainDataFrameInput['wnwHsit'] = wnwHist
        # mainDataFrameInput['variableHist'] = variableHist
        # mainDataFrameInput['southHist'] = southHist
        # mainDataFrameInput['swHist'] = swHist
        # mainDataFrameInput['sswHist'] = sswHist
        # mainDataFrameInput['sseHist'] = sseHist
        # mainDataFrameInput['seHist'] = seHist
        # mainDataFrameInput['northHist'] = northHist
        # mainDataFrameInput['nwHist'] = nwHist
        # mainDataFrameInput['nnwHist'] = nnwHist
        # mainDataFrameInput['nneHist'] = nneHist
        # mainDataFrameInput['neHist'] = neHist
        # mainDataFrameInput['eastHist'] = eastHist
        # mainDataFrameInput['eseHist'] = eseHist
        # mainDataFrameInput['eneHist'] = eneHist
        #
        #
        mainDataFrameInput = mainDataFrameInput.drop('kierunek wiatru', 1)
        mainDataFrameInput = mainDataFrameInput.reset_index(drop=True)

        mainDataFrameOutput = mainDataFrame [['PM10']][1:]
        mainDataFrameOutput = mainDataFrameOutput.reset_index(drop=True)


        data = np.concatenate((mainDataFrameInput, mainDataFrameOutput), axis=1)
        data = shuffle(data)

        mainDataFrameInput = data[:,0:-1]
        mainDataFrameOutput = data[:,-1]


        min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0,1))
        mainDataFrameInput = min_max_scaler.fit_transform(mainDataFrameInput)
        training_inputs = [np.reshape(x, (9, 1)) for x in mainDataFrameInput]
        maxValue = max(mainDataFrameOutput)
        minValue = min(mainDataFrameOutput)
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

        nowaTablicaInputTest = nowaTablicaInput[7000:]
        nowaTablicaInputTest = np.array(nowaTablicaInputTest)

        nowaTablicaOutputTrain = nowaTablicaOutput[0:7000]
        nowaTablicaOutputTest = nowaTablicaOutput[7000:]


        treningowaInp = nowaTablicaInputTrain
        treningowaOutp = nowaTablicaOutputTrain
        testowaInp = nowaTablicaInputTest
        testowaOutp = nowaTablicaOutputTest

        return treningowaInp,treningowaOutp,testowaInp,testowaOutp,minValue,maxValue

data = DataGetter()
data.getData()