import requests
import pandas as pd

class FutureWeatherDownloader(object):

    def __init__(self, predDuration):
        self.predictionDuration = predDuration

    def downloadData(self):

        predictionDuration = self.predictionDuration

        columns = ['date', 'cisnienie', 'kierunek_wiatru', 'predkosc_wiatru', 'temperatura', 'warunki_pogodowe',
                   'wilgotnosc',
                   'deszcz', 'snieg']

        dataFrame = pd.DataFrame(columns=columns)


        response = requests.get("http://api.wunderground.com/api/de8dda073f18e891/hourly/q/CA/Warszawa.json")

        data = response.json()

        print "daaata"
        print data

        date = []

        for k in range(0,predictionDuration,1):
            stringData = data["hourly_forecast"][k]["FCTTIME"]["year"]+"-"+data["hourly_forecast"][k]["FCTTIME"]["mon_padded"]+"-"+data["hourly_forecast"][k]["FCTTIME"]["mday_padded"]+" "+data["hourly_forecast"][k]["FCTTIME"]["hour_padded"]+":"+data["hourly_forecast"][k]["FCTTIME"]["min"]
            date.append(stringData)


        cisnienie = []
        kierunekWiatru = []
        predkoscWiatru = []
        temperatura = []
        warunkiPogodowe = []
        deszcz = []
        wilgotnosc = []
        snieg = []

        for k in range(0,predictionDuration,1):
            cisnienie.append(data["hourly_forecast"][k]["mslp"]["metric"])
            kierunekWiatru.append(data["hourly_forecast"][k]["wdir"]["dir"])
            predkoscWiatru.append(data["hourly_forecast"][k]["wspd"]["metric"])
            temperatura.append(data["hourly_forecast"][k]["temp"]["metric"])
            warunkiPogodowe.append(data["hourly_forecast"][k]["wx"])
            deszcz.append(data["hourly_forecast"][k]["qpf"]["metric"])
            wilgotnosc.append(data["hourly_forecast"][k]["humidity"])
            snieg.append(data["hourly_forecast"][k]["snow"]["metric"])

        dataFrame["date"] = date
        dataFrame["cisnienie"] = cisnienie
        dataFrame["kierunek_wiatru"] = kierunekWiatru
        dataFrame["predkosc_wiatru"] = predkoscWiatru
        dataFrame["warunki_pogodowe"] = warunkiPogodowe
        dataFrame["wilgotnosc"] = wilgotnosc
        dataFrame["temperatura"] = temperatura
        dataFrame["deszcz"] = deszcz
        dataFrame["snieg"] = snieg

        return dataFrame
