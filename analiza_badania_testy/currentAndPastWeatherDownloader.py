import datetime as dtme
from datetime import timedelta
import requests
import pandas as pd


class CurrentAndPastWeatherDownloader(object):
    def __init__(self, hoursInPast):
        self.hoursInPast = hoursInPast

    def downloadData(self):

        NumberOfHoursInPast = self.hoursInPast

        now = dtme.datetime.now()

        datesNeedForRequest = []
        neededDates = []
        numberOfRequestsForToday = 0
        numberOfRequestsForYesterday = 0

        cisnienie = []
        kierunekWiatru = []
        predkoscWiatru = []
        temperatura = []
        warunkiPogodowe = []
        deszcz = []
        wilgotnosc = []
        snieg = []
        mgla = []
        date = []

        columns = ['date', 'cisnienie', 'kierunek_wiatru', 'predkosc_wiatru', 'temperatura', 'warunki_pogodowe',
                   'wilgotnosc','deszcz', 'snieg']


        dataFrameForWeather = pd.DataFrame(columns=columns)

        for x in range(0,NumberOfHoursInPast,1):
             pastDate = (now-timedelta(hours=x))
             if pastDate.date() == now.date():
                 numberOfRequestsForToday = numberOfRequestsForToday+1
             elif pastDate.date() < now.date():
                 numberOfRequestsForYesterday = numberOfRequestsForYesterday+1
             pastDate = str (pastDate)
             pastDate = pastDate [0:14]
             pastDate = pastDate + "00"
             neededDates.append(str(pastDate))

        for item in neededDates:
            item = item [0:10]
            item = item.replace("-","")
            datesNeedForRequest.append(item)
            datesNeedForRequestSet = set(datesNeedForRequest)
            datesNeedForRequest = list(datesNeedForRequestSet)


        for requestDate in datesNeedForRequest:
            response = requests.get("http://api.wunderground.com/api/de8dda073f18e891/history_"+requestDate+"/q/CA/Warszawa.json")
            data = response.json()
            NumberOfData = len(data["history"]["observations"])
            stringData = ""

            for x in range(0, NumberOfData):
             stringData = (
             data["history"]["observations"][x]["date"]["year"] + "-" + data["history"]["observations"][x]["date"]["mon"] + "-" +
             data["history"]["observations"][x]["date"]["mday"] + " " + data["history"]["observations"][x]["date"]["hour"][0:5] +
             ":" + data["history"]["observations"][x]["date"][ "min"])
             date.append(stringData)

             cisnienie.append(data["history"]["observations"][x]["pressurem"])
             kierunekWiatru.append(data["history"]["observations"][x]["wdire"])
             predkoscWiatru.append(data["history"]["observations"][x]["wspdm"])
             temperatura.append(data["history"]["observations"][x]["tempm"])
             warunkiPogodowe.append(data["history"]["observations"][x]["conds"])
             deszcz.append(data["history"]["observations"][x]["rain"])
             wilgotnosc.append(data["history"]["observations"][x]["hum"])
             snieg.append(data["history"]["observations"][x]["snow"])
             mgla.append(data["history"]["observations"][x]["fog"])

        dataFrameForWeather["date"] = date
        dataFrameForWeather["cisnienie"] = cisnienie
        dataFrameForWeather["kierunek_wiatru"] = kierunekWiatru
        dataFrameForWeather["predkosc_wiatru"] = predkoscWiatru
        dataFrameForWeather["warunki_pogodowe"] = warunkiPogodowe
        dataFrameForWeather["wilgotnosc"] = wilgotnosc
        dataFrameForWeather["temperatura"] = temperatura
        dataFrameForWeather["deszcz"] = deszcz
        dataFrameForWeather["snieg"] = snieg
        dataFrameForWeather["mgla"] = mgla

        dataFrameForWeather.drop_duplicates(['date'], keep='last', inplace=True)
        downloadedWeatherDataFrame = (dataFrameForWeather[dataFrameForWeather['date'].isin(neededDates)])
        return downloadedWeatherDataFrame