# -*- coding: utf-8 -*-

# Skrypt badajacy jak dobrze klasyfikuje algorytm xgboost

from __future__ import unicode_literals

import os
mingw_path = 'C:\\Program Files\mingw-w64\\x86_64-7.2.0-posix-seh-rt_v5-rev1\\mingw64\\bin'
os.environ['PATH'] = mingw_path + ';' + os.environ['PATH']
from datetime import datetime

from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.utils import shuffle
from xgboost import plot_importance
from sklearn.preprocessing import LabelEncoder
import sqlite3
import pandas as pd
from matplotlib import pyplot
from sklearn.preprocessing import OneHotEncoder
from numpy import array
import numpy as np
conn = sqlite3.connect('dane.db')
dataFrame = pd.read_sql_query("SELECT * FROM resultcsv", conn)
dataFrame = dataFrame.sort_values(by='date')
dataFrame = dataFrame.dropna(axis=0, how='any')
dataFrame = dataFrame.reset_index(drop=True)


inputArray = [

         "pressureDiff",
        "windSpeedDiff", "temperatureDiff","humidityDiff","pressure","temperature","humidity","windSpeed",
 "hour0", "hour1",
                "hour2", "hour3","hour4", "hour5", "hour6", "hour7", "hour8","hour9",
"hour10","hour11","hour12","hour13","hour14","hour15","hour16","hour17","hour18","hour19",
"hour20","hour21", "hour22", "hour23",
"month1","month2","month3","month4","month5","month6","month7","month8","month9","month10","month11","month12",
     "PM10","windDir1-1",
"windDir1-2", "windDir1-3","windDir1-4","windDir1-5","windDir1-6","windDir1-7",
"windDir1-8","windDir1-9","windDir1-10","windDir1-11","windDir1-12","windDir1-13",
 "windDir1-14","windDir1-15","windDir1-16","windDir1-17","windDir1-18"



]


mainDataColumns = [
              "hour0", "hour1",
                "hour2", "hour3","hour4", "hour5", "hour6", "hour7", "hour8","hour9",
"hour10","hour11","hour12","hour13","hour14","hour15","hour16","hour17","hour18","hour19",
"hour20","hour21", "hour22", "hour23",

"month1","month2","month3","month4","month5","month6","month7","month8","month9","month10","month11","month12", "pressureDiff","windDir1-1",
                                                            "windDir1-2", "windDir1-3","windDir1-4","windDir1-5","windDir1-6","windDir1-7",
                                                            "windDir1-8","windDir1-9","windDir1-10","windDir1-11","windDir1-12","windDir1-13",
                                                            "windDir1-14","windDir1-15","windDir1-16","windDir1-17","windDir1-18", "windDir2-1",
                                                            "windDir2-2","windDir2-3","windDir2-4","windDir2-5","windDir2-6", "windDir2-7","windDir2-8",
                                                            "windDir2-9","windDir2-10","windDir2-11","windDir2-12","windDir2-13","windDir2-14","windDir2-15"
                                                            ,"windDir2-16","windDir2-17","windDir2-18","deszcz1","rzadka mgla1", "gesta mgla1","snieg1","czesciowo pochmurnie1",
                                                            "calkowicie pochmurnie1","czyste niebo1", "rozproszone chmury1","wiekszosc pochmurna1","nieznane1","lekki deszcz1",
                                                            "burza1", "duzy deszcz1",

                                                            "deszcz2", "rzadka mgla2", "gesta mgla2", "snieg2",
                                                            "czesciowo pochmurnie2",
                                                            "calkowicie pochmurnie2", "czyste niebo2",
                                                            "rozproszone chmury2", "wiekszosc pochmurna2", "nieznane2",
                                                            "lekki deszcz2",
                                                            "burza2", "duzy deszcz2",
                                                            "windSpeedDiff", "temperatureDiff","humidityDiff","windSpeed","temperature","humidity",
                                                            "PM10", "prevPM10", "pressure", "category"]


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



def getDateHourAndMonth (date):
    date = date.values[0]
    date = datetime.strptime(date, '%Y-%m-%d %H:%M')
    return float(date.hour), float(date.month)

def getDifferance(cat, index):

    value1 = float (dataFrame.iloc[index][cat])
    value2 = float(dataFrame.iloc[index+1][cat])
    value1 = round(value1, 2)
    value2 = round(value2, 2)
    differance = value2 - value1
    return differance


def getCategories(category, index):
    if category == "kierunek wiatru":
        catList = ['west','wsw','wnw','variable','south','sw','ssw','sse','se','north','nw','nnw','nne','ne','east','ese','ene','']
        values = array(catList)

        label_encoder = LabelEncoder()
        integer_encoded = label_encoder.fit_transform(values)
        integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)

        onehot_encoder = OneHotEncoder(sparse=False)
        onehot_encoded = onehot_encoder.fit_transform(integer_encoded)

        category1 = str(dataFrame.iloc[index][category])
        category2 = str(dataFrame.iloc[index+1][category])

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


        category1 = str(dataFrame.iloc[index][category])
        category2 = str(dataFrame.iloc[index+1][category])

        if ("snow" in category1.lower()):
            category1 = "snow"
        if ("snow" in category2.lower()):
            category2 = "snow"

        if ("fog" in category1.lower()):
            category1 = "fog"
        if  ("fog" in category2.lower()):
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

def getCategoryValue(index):
    PM10Diff = getDifferance('PM10', index)
    if PM10Diff <= 0:
        value = 0
    else:
        value = 1
    return value

newdataFrame = pd.DataFrame(columns= mainDataColumns)
for index, row in dataFrame.iterrows():
    if (index >= 1) & (index < 8100):
        diffsList = []

        hour = getHour(index)
        month = getMonth(index)
        temperature = float(dataFrame.iloc[[index]]['temperatura'])
        windSpeed = float(dataFrame.iloc[[index]]['predkosc wiatru'])
        humidity = float(dataFrame.iloc[[index]]['wilgotnosc'])
        pressure = float(dataFrame.iloc[[index]]['cisnienie'])
        pressureDiff = getDifferance('cisnienie',index)
        windSpeedDiff = getDifferance('predkosc wiatru', index)
        humidityDiff = getDifferance('wilgotnosc', index)
        tempDiff = getDifferance('temperatura', index )
        windDir1, windDir2 = getCategories('kierunek wiatru', index)
        weatherCond1, weatherCond2 = getCategories('warunki pogodowe', index)
        valueOfCategory = float(getCategoryValue(index))
        lastValueOfCategory = float(getCategoryValue(index-1))
        PM10 = float(dataFrame.iloc[[index]]['PM10'])
        prevPM10 = float(dataFrame.iloc[[index-1]]['PM10'])


        itemsList = [ hour[0], hour[1], hour[2], hour[3], hour[4], hour[5], hour[6], hour[7],
                      hour[8], hour[9], hour[10], hour[11], hour[12], hour[13], hour[14], hour[15],
                      hour[16], hour[17], hour[18], hour[19], hour[20], hour[21], hour[22], hour[23],
                      month[0], month[1], month[2], month[3], month[4], month[5], month[6], month[7],
                      month[8], month[9], month[10], month[11], pressureDiff,windDir1[0],windDir1[1], windDir1[2],
                     windDir1[3], windDir1[4], windDir1[5], windDir1[6], windDir1[7], windDir1[8], windDir1[9],
                     windDir1[10], windDir1[11], windDir1[12], windDir1[13], windDir1[14], windDir1[15],windDir1[16],
                     windDir1[17], windDir2[0], windDir2[1], windDir2[2], windDir2[3], windDir2[4], windDir2[5], windDir2[6],
                     windDir2[7],windDir2[8], windDir2[9],windDir2[10], windDir2[11], windDir2[12], windDir2[13], windDir2[14],
                     windDir2[15], windDir2[16],windDir2[17],weatherCond1[8], weatherCond1[2], weatherCond1[4], weatherCond1[10],
                     weatherCond1[7],weatherCond1[6], weatherCond1[0], weatherCond1[9], weatherCond1[5], weatherCond1[12],
                     weatherCond1[1], weatherCond1[11], weatherCond1[3],

                     weatherCond2[8], weatherCond2[2], weatherCond2[4], weatherCond2[10],
                     weatherCond2[7], weatherCond2[6], weatherCond2[0], weatherCond2[9], weatherCond2[5],
                     weatherCond2[12],
                     weatherCond2[1], weatherCond2[11], weatherCond2[3],

                     windSpeedDiff, tempDiff, humidityDiff,windSpeed,temperature,humidity, PM10, prevPM10, pressure,
                     valueOfCategory]

        dataFrameTemp = pd.DataFrame([itemsList], columns= mainDataColumns)
        newdataFrame = newdataFrame.append(dataFrameTemp)

#newdataFrame = shuffle(newdataFrame)
newdataFrame = newdataFrame.reset_index(drop=True)
newdataFrame.to_sql(con=conn, name="testtXGBoost", if_exists="replace")


trainDataX = newdataFrame[0:7000][inputArray]

trainDataY = newdataFrame[0:7000]["category"]

testDataX = newdataFrame[7000:][inputArray]


testDataY = newdataFrame[7000:]["category"]


model = XGBClassifier(
    learning_rate=0.7,
    max_depth=6,
    reg_alpha=0.2,
    reg_lambda=800


)
eval_set = [(trainDataX, trainDataY), (testDataX, testDataY)]

model.fit(trainDataX, trainDataY ,  early_stopping_rounds=20, eval_metric="error", eval_set=eval_set, verbose=True)

plot_importance(model)
pyplot.show()
y_pred = model.predict(testDataX)
predictions = [round(value) for value in y_pred]
testDataY = list(testDataY)
accuracy = accuracy_score(testDataY, predictions)


results = model.evals_result()
epochs = len(results['validation_0']['error'])
x_axis = range(1, epochs+1, 1)
# plot classification error
fig, ax = pyplot.subplots()
# ax.plot(x_axis, results['validation_0']['error'], label='Train')


yToPlot = results['validation_1']['error']

yToPlot = [100 - k*100 for k in yToPlot ]

ax.plot(x_axis,yToPlot, label='Test')
# ax.legend()
pyplot.xticks(np.arange(min(x_axis), max(x_axis)+1, 1.0), fontsize = 14)

pyplot.xlabel("Numer iteracji", fontsize = 20)
pyplot.ylabel('Poprawnych klasyfikacji [%]',fontsize=20)
pyplot.title('Badanie poprawności predykcji zmian stężenia pyłu $PM_{10}$ dla algorytmu XGBoost', fontsize=20)
pyplot.xticks(fontsize = 14)
pyplot.yticks(fontsize = 14)
pyplot.grid(1)
pyplot.show()


print("Accuracy: %.2f%%" % (accuracy * 100.0))

