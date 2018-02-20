
import requests
import numpy as np
import pandas as pd
import sqlite3

# Skrypt pobiera dane pogodowe, trzeba zmieniac url zawarte w zmiennej response
#

conn = sqlite3.connect("dane.db")

for iterator in range(30,32):

    response = requests.get("http://api.wunderground.com/api/de8dda073f18e891/history_201612"+str(iterator)+"/q/CA/Warszawa.json")

    data = response.json()

    k = len(data["history"]["observations"])

    stringData = ""
    date = []

    for x in range (0,k):
        stringData = (data["history"]["observations"][x]["date"]["year"]+"-"+data["history"]["observations"][x]["date"]["mon"]+"-"+data["history"]["observations"][x]["date"]["mday"]+" "+data["history"]["observations"][x]["date"]["hour"][0:5]+":"+data["history"]["observations"][x]["date"]["min"])
        date.append(stringData)


    columns = ['date','cisnienie','kierunek wiatru','predkosc wiatru','temperatura','warunki pogodowe','wilgotnosc','deszcz','snieg','mgla']
    dataFrame = pd.DataFrame(columns=columns )

    cisnienie = []
    kierunekWiatru = []
    predkoscWiatru = []
    temperatura = []
    warunkiPogodowe = []
    deszcz = []
    widzialnosc = []
    wilgotnosc = []
    snieg = []
    mgla = []


    for x in range(0,k):
        cisnienie.append(data["history"]["observations"][x]["pressurem"])
        kierunekWiatru.append(data["history"]["observations"][x]["wdire"])
        predkoscWiatru.append(data["history"]["observations"][x]["wspdm"])
        temperatura.append(data["history"]["observations"][x]["tempm"])
        warunkiPogodowe.append(data["history"]["observations"][x]["conds"])
        deszcz.append(data["history"]["observations"][x]["rain"])
        wilgotnosc.append(data["history"]["observations"][x]["hum"])
        snieg.append(data["history"]["observations"][x]["snow"])
        mgla.append(data["history"]["observations"][x]["fog"])

    dataFrame["date"] = date
    dataFrame["cisnienie"] = cisnienie
    dataFrame["kierunek wiatru"] = kierunekWiatru
    dataFrame["predkosc wiatru"] = predkoscWiatru
    dataFrame["warunki pogodowe"] = warunkiPogodowe
    dataFrame["wilgotnosc"] = wilgotnosc
    dataFrame["temperatura"] = temperatura
    dataFrame["deszcz"] = deszcz
    dataFrame ["snieg"] = snieg
    dataFrame ["mgla"] = mgla

    dataFrame.drop_duplicates(['date'], keep = 'last', inplace=True)


    dataFrame.to_sql('pogoda',conn,if_exists='append')


