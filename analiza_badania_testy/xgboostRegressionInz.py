# -*- coding: utf-8 -*-

# skrypt badajacy jak dobrze dokonuje predykcji xgboost

from __future__ import unicode_literals

import os
from datetime import datetime
mingw_path = 'C:\\Program Files\mingw-w64\\x86_64-7.2.0-posix-seh-rt_v5-rev1\\mingw64\\bin'
os.environ['PATH'] = mingw_path + ';' + os.environ['PATH']

from xgboost import XGBRegressor
import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from matplotlib import pyplot
from xgboost import plot_importance
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from numpy import array
import numpy as np
from sklearn.metrics import accuracy_score

from sklearn.utils import shuffle


mainArray = ["temperature1", "windStrength1", "humidity1","pressure1",
              "temperature2", "windStrength2", "humidity2","pressure2",

               "windDir1-1",
                "windDir1-2", "windDir1-3","windDir1-4","windDir1-5","windDir1-6","windDir1-7",
                "windDir1-8","windDir1-9","windDir1-10","windDir1-11","windDir1-12","windDir1-13",
                "windDir1-14","windDir1-15","windDir1-16","windDir1-17","windDir1-18",

               "windDir2-1", "windDir2-2", "windDir2-3", "windDir2-4", "windDir2-5",
               "windDir2-6", "windDir2-7", "windDir2-8","windDir2-9", "windDir2-10",
               "windDir2-11", "windDir2-12", "windDir2-13", "windDir2-14",
               "windDir2-15","windDir2-16", "windDir2-17", "windDir2-18",

                "deszcz1","rzadka mgla1", "gesta mgla1","snieg1","czesciowo pochmurnie1",
                "calkowicie pochmurnie1","czyste niebo1", "rozproszone chmury1","wiekszosc pochmurna1",
                "nieznane1","lekki deszcz1",  "burza1", "duzy deszcz1",

                "deszcz2", "rzadka mgla2", "gesta mgla2", "snieg2",
                "czesciowo pochmurnie2", "calkowicie pochmurnie2", "czyste niebo2",
                "rozproszone chmury2", "wiekszosc pochmurna2", "nieznane2",
                 "lekki deszcz2", "burza2", "duzy deszcz2", "currentPM10",

 "hour0", "hour1",
                "hour2", "hour3","hour4", "hour5", "hour6", "hour7", "hour8","hour9",
"hour10","hour11","hour12","hour13","hour14","hour15","hour16","hour17","hour18","hour19",
"hour20","hour21", "hour22", "hour23",
"month1","month2","month3","month4","month5","month6","month7","month8","month9","month10","month11","month12"


             ]


inputArray = [

    "temperature1", "windStrength1", "humidity1","pressure1",
              # "temperature2", "windStrength2", "humidity2","pressure2",
#
               "windDir1-1",
                "windDir1-2", "windDir1-3","windDir1-4","windDir1-5","windDir1-6","windDir1-7",
                "windDir1-8","windDir1-9","windDir1-10","windDir1-11","windDir1-12","windDir1-13",
                "windDir1-14","windDir1-15","windDir1-16","windDir1-17","windDir1-18",

               # "windDir2-1", "windDir2-2", "windDir2-3", "windDir2-4", "windDir2-5",
               # "windDir2-6", "windDir2-7", "windDir2-8","windDir2-9", "windDir2-10",
               # "windDir2-11", "windDir2-12", "windDir2-13", "windDir2-14",
               # "windDir2-15","windDir2-16", "windDir2-17", "windDir2-18",

                "deszcz1","rzadka mgla1", "gesta mgla1","snieg1","czesciowo pochmurnie1",
                "calkowicie pochmurnie1","czyste niebo1", "rozproszone chmury1","wiekszosc pochmurna1",
                "nieznane1","lekki deszcz1",  "burza1", "duzy deszcz1",

                "deszcz2", "rzadka mgla2", "gesta mgla2", "snieg2",
                "czesciowo pochmurnie2", "calkowicie pochmurnie2", "czyste niebo2",
                "rozproszone chmury2", "wiekszosc pochmurna2", "nieznane2",
                 "lekki deszcz2", "burza2", "duzy deszcz2",
#               "hour0", "hour1",
#                 "hour2", "hour3","hour4", "hour5", "hour6", "hour7", "hour8","hour9",
# "hour10","hour11","hour12","hour13","hour14","hour15","hour16","hour17","hour18","hour19",
# "hour20","hour21", "hour22", "hour23"
#
"month1","month2","month3","month4","month5","month6","month7","month8","month9","month10","month11","month12"              ]

outputArray = ["currentPM10"]

conn = sqlite3.connect('dane.db')
dataFrame = pd.read_sql_query("SELECT * FROM resultcsv", conn)
dataFrame = dataFrame.sort_values(by='date')
dataFrame = dataFrame.dropna(axis=0, how='any')
dataFrame = dataFrame.reset_index(drop=True)


dataFrameForRegressionX = pd.DataFrame(columns=inputArray)
dataFrameForRegressionY = pd.DataFrame(columns=outputArray)


def getPM10(index):
    PM10 = dataFrame.iloc[index]['PM10']
    return PM10

def getMonth(index):
    monthList = range(1,13)
    values = array(monthList)
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(values)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoder = OneHotEncoder(sparse=False)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
    date = datetime.strptime(dataFrame.iloc[index]['date'], '%Y-%m-%d %H:%M')
    month = date.month
    indexMonth = monthList.index(month)

    return onehot_encoded[indexMonth]

def getHour (index):
    hourList = range(0,24)
    values = array(hourList)

    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(values)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoder = OneHotEncoder(sparse=False)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
    date = datetime.strptime(dataFrame.iloc[index]['date'], '%Y-%m-%d %H:%M')
    hour = date.hour
    indexHour = hourList.index(hour)

    return onehot_encoded[indexHour]




def getCategories(category, index):
    if category == "kierunek wiatru":
        catList = ['west','wsw','wnw','variable','south','sw','ssw','sse','se','north','nw','nnw','nne','ne','east','ese','ene','']
        values = array(catList)

        label_encoder = LabelEncoder()
        integer_encoded = label_encoder.fit_transform(values)
        integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)

        onehot_encoder = OneHotEncoder(sparse=False)
        onehot_encoded = onehot_encoder.fit_transform(integer_encoded)

        category1 = str(dataFrame.iloc[index-1][category])
        category2 = str(dataFrame.iloc[index][category])

        indexCat1 = catList.index(category1.lower())
        indexCat2 = catList.index(category2.lower())

        return onehot_encoded[indexCat1], onehot_encoded[indexCat2]

    elif category == "warunki pogodowe":
        catList = ['rain', 'fog', 'mist', 'snow', 'partly cloudy', 'overcast', 'clear', 'scattered clouds',
                   'mostly cloudy', 'unknown', 'drizzle', 'thunderstorm', 'hail']

        values = array(catList)

        label_encoder = LabelEncoder()
        integer_encoded = label_encoder.fit_transform(values)
        onehot_encoder = OneHotEncoder(sparse=False)
        integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
        onehot_encoded = onehot_encoder.fit_transform(integer_encoded)

        category1 = str(dataFrame.iloc[index-1][category])
        category2 = str(dataFrame.iloc[index][category])

        if ("snow" in category1.lower()):
            category1 = "snow"
        if ("snow" in category2.lower()):
            category2 = "snow"

        if ("fog" in category1.lower()):
            category1 = "fog"
        if ("fog" in category2.lower()):
            category2 = "fog"

        if ("rain" in category1.lower()):
            category1 = "rain"
        if "rain" in category2.lower():
            category2 = "rain"

        if "drizzle" in category1.lower():
            category1 = "drizzle"
        if "drizzle" in category2.lower():
            category2 = "drizzle"

        if "showers" in category1.lower():
            category1 = "rain"
        if "showers" in category2.lower():
            category2 = "rain"

        if category1 == '':
            category1 = "unknown"
        if category2 == '':
            category2 = "unknown"

        if "hail" in category1.lower():
            category1 = "hail"
        if "hail" in category2.lower():
            category2 = "hail"

        indexCat1 = catList.index(category1.lower())
        indexCat2 = catList.index(category2.lower())

        return onehot_encoded[indexCat1], onehot_encoded[indexCat2]


dataFrameForRegression = pd.DataFrame(columns=mainArray)
for index, row in dataFrame.iterrows():
    if (index>=1) & (index<=8100):

        prevPM10 = float(getPM10(index-1))
        currentPM10 = float(getPM10(index))

        currTemperature = float(dataFrame.iloc[[index]]['temperatura'])
        currWindStrength = float(dataFrame.iloc[[index]]['predkosc wiatru'])
        currHumidity = float(dataFrame.iloc[index]['wilgotnosc'])
        currPressure = float(dataFrame.iloc[index]['cisnienie'])

        prevTemperature = float(dataFrame.iloc[[index-1]]['temperatura'])
        prevWindStrength = float(dataFrame.iloc[[index-1]]['predkosc wiatru'])
        prevHumidity = float(dataFrame.iloc[index-1]['wilgotnosc'])
        prevPressure = float(dataFrame.iloc[index-1]['cisnienie'])
        hour = getHour(index)
        month = getMonth(index)


        windDir1,windDir2 = getCategories("kierunek wiatru", index)
        weatherCond1, weatherCond2 = getCategories('warunki pogodowe', index)

        listOfData = [currTemperature, currWindStrength, currHumidity,currPressure,
                       prevTemperature, prevWindStrength, prevHumidity,prevPressure,
                       windDir1[0], windDir1[1], windDir1[2],
                       windDir1[3], windDir1[4], windDir1[5],
                       windDir1[6], windDir1[7], windDir1[8],
                       windDir1[9], windDir1[10], windDir1[11],
                       windDir1[12], windDir1[13], windDir1[14],
                       windDir1[15], windDir1[16],  windDir1[17],

                       windDir2[0], windDir2[1], windDir2[2], windDir2[3],
                       windDir2[4], windDir2[5], windDir2[6],windDir2[7],
                       windDir2[8], windDir2[9], windDir2[10], windDir2[11],
                       windDir2[12], windDir2[13], windDir2[14],
                       windDir2[15], windDir2[16], windDir2[17],

                       weatherCond1[8], weatherCond1[2], weatherCond1[4], weatherCond1[10],
                       weatherCond1[7], weatherCond1[6], weatherCond1[0], weatherCond1[9], weatherCond1[5],
                       weatherCond1[12],  weatherCond1[1], weatherCond1[11], weatherCond1[3],

                       weatherCond2[8], weatherCond2[2], weatherCond2[4], weatherCond2[10],
                       weatherCond2[7], weatherCond2[6], weatherCond2[0], weatherCond2[9], weatherCond2[5],
                       weatherCond2[12],
                       weatherCond2[1], weatherCond2[11], weatherCond2[3], currentPM10,
                      hour[0], hour[1], hour[2], hour[3], hour[4], hour[5], hour[6], hour[7],
                      hour[8], hour[9], hour[10], hour[11], hour[12], hour[13], hour[14], hour[15],
                      hour[16], hour[17], hour[18], hour[19], hour[20], hour[21], hour[22], hour[23],
                      month[0], month[1], month[2], month[3], month[4], month[5], month[6], month[7],
                      month[8], month[9], month[10], month[11]
                      ]


        dataFrameTemp = pd.DataFrame([listOfData], columns=mainArray)
        dataFrameForRegression = dataFrameForRegression.append(dataFrameTemp)

dataFrameForRegression = shuffle(dataFrameForRegression)
dataFrameForRegressionX = dataFrameForRegression[inputArray]
dataFrameForRegressionY = dataFrameForRegression[outputArray]

X_train, X_test, y_train, y_test = train_test_split(dataFrameForRegressionX, dataFrameForRegressionY, test_size=0.138, random_state=20)

avgTrain = sum(y_train['currentPM10'])/len(y_train['currentPM10'])
avgTest = sum(y_test['currentPM10'])/len(y_test['currentPM10'])



model = XGBRegressor(
    reg_lambda=0
)

eval_set = [(X_train, y_train), (X_test, y_test)]

model.fit(X_train, y_train ,  early_stopping_rounds=20, eval_metric="mae", eval_set=eval_set, verbose=True)

y_pred = model.predict(X_test)

#accuracy = accuracy_score(testDataY, predictions)


avgTrain = sum(y_train['currentPM10'])/len(y_train['currentPM10'])
avgTest = sum(y_test['currentPM10'])/len(y_test['currentPM10'])

y_test = list(y_test['currentPM10'])

results = model.evals_result()
print results
epochs = len(results['validation_0']['mae'])
x_axis = range(1, epochs+1)
# plot classification error
fig, ax = pyplot.subplots()

resultsToPlotTrain = [i for i in results['validation_0']['mae']]
resultsToPlotTest = [i for i in results['validation_1']['mae']]


ax.plot(x_axis, resultsToPlotTest)
pyplot.ylabel('Średni błąd absolutny', fontsize = 20)
pyplot.xlabel('Numer iteracji', fontsize = 20)
pyplot.xticks(np.arange(min(x_axis), max(x_axis)+1, 10.0), fontsize = 14)
pyplot.xticks(fontsize=14)
pyplot.yticks(fontsize=14)
pyplot.grid(1)
pyplot.title('Badanie średniego błędu absolutnego predykcji stężenia pyłu $PM_{10}$ przy użyciu algorytmu XGBoost dla modelu numer 8 ', fontsize = 15)
pyplot.show()

y_pred = [round (x,2) for x in y_pred ]
y_test = [round (x,2) for x in y_test]


error_array = []

for i in range (0, len(y_pred)-1):
    error = abs (y_pred[i] - y_test[i])
    relativeError = error / y_test[i]
    error_array.append(relativeError)

avgError = sum(error_array)/len(error_array)

print np.array(y_pred).shape
print avgError