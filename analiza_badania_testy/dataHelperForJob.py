import numpy as np
import PredykcjaRegresja


class PredictorContainer(object):
    def transformAndPredict(self, dataFrame, hoursToPredict):
        previousPM10 = dataFrame['pm10'][0:-1]
        prevHumidity = dataFrame['wilgotnosc'][0:-1]
        prevPressure = dataFrame['cisnienie'][0:-1]
        prevWindSpeed = dataFrame['predkosc_wiatru'][0:-1]
        prevTemperature = dataFrame ['temperatura'][0:-1]


        dataFrame['godzina 0'] = np.where(dataFrame['date'].dt.hour == 0, 1, 0)
        dataFrame['godzina 1'] = np.where(dataFrame['date'].dt.hour == 1, 1, 0)
        dataFrame['godzina 2'] = np.where(dataFrame['date'].dt.hour == 2, 1, 0)
        dataFrame['godzina 3'] = np.where(dataFrame['date'].dt.hour == 3, 1, 0)
        dataFrame['godzina 4'] = np.where(dataFrame['date'].dt.hour == 4, 1, 0)
        dataFrame['godzina 5'] = np.where(dataFrame['date'].dt.hour == 5, 1, 0)
        dataFrame['godzina 6'] = np.where(dataFrame['date'].dt.hour == 6, 1, 0)
        dataFrame['godzina 7'] = np.where(dataFrame['date'].dt.hour == 7, 1, 0)
        dataFrame['godzina 8'] = np.where(dataFrame['date'].dt.hour == 8, 1, 0)
        dataFrame['godzina 9'] = np.where(dataFrame['date'].dt.hour == 9, 1, 0)
        dataFrame['godzina 10'] = np.where(dataFrame['date'].dt.hour == 10, 1, 0)
        dataFrame['godzina 11'] = np.where(dataFrame['date'].dt.hour == 11, 1, 0)
        dataFrame['godzina 12'] = np.where(dataFrame['date'].dt.hour == 12, 1, 0)
        dataFrame['godzina 13'] = np.where(dataFrame['date'].dt.hour == 13, 1, 0)
        dataFrame['godzina 14'] = np.where(dataFrame['date'].dt.hour == 14, 1, 0)
        dataFrame['godzina 15'] = np.where(dataFrame['date'].dt.hour == 15, 1, 0)
        dataFrame['godzina 16'] = np.where(dataFrame['date'].dt.hour == 16, 1, 0)
        dataFrame['godzina 17'] = np.where(dataFrame['date'].dt.hour == 17, 1, 0)
        dataFrame['godzina 18'] = np.where(dataFrame['date'].dt.hour == 18, 1, 0)
        dataFrame['godzina 19'] = np.where(dataFrame['date'].dt.hour == 19, 1, 0)
        dataFrame['godzina 20'] = np.where(dataFrame['date'].dt.hour == 20, 1, 0)
        dataFrame['godzina 21'] = np.where(dataFrame['date'].dt.hour == 21, 1, 0)
        dataFrame['godzina 22'] = np.where(dataFrame['date'].dt.hour == 22, 1, 0)
        dataFrame['godzina 23'] = np.where(dataFrame['date'].dt.hour == 23, 1, 0)

        dataFrame['styczen'] = np.where(dataFrame['date'].dt.month == 1, 1, 0)
        dataFrame['luty'] = np.where(dataFrame['date'].dt.month == 2, 1, 0)
        dataFrame['marzec'] = np.where(dataFrame['date'].dt.month == 3, 1, 0)
        dataFrame['kwiecien'] = np.where(dataFrame['date'].dt.month == 4, 1, 0)
        dataFrame['maj'] = np.where(dataFrame['date'].dt.month == 5, 1, 0)
        dataFrame['czerwiec'] = np.where(dataFrame['date'].dt.month == 6, 1, 0)
        dataFrame['lipiec'] = np.where(dataFrame['date'].dt.month == 7, 1, 0)
        dataFrame['sierpien'] = np.where(dataFrame['date'].dt.month == 8, 1, 0)
        dataFrame['wrzesien'] = np.where(dataFrame['date'].dt.month == 9, 1, 0)
        dataFrame['pazdziernik'] = np.where(dataFrame['date'].dt.month == 10, 1, 0)
        dataFrame['listopad'] = np.where(dataFrame['date'].dt.month == 11, 1, 0)
        dataFrame['grudzien'] = np.where(dataFrame['date'].dt.month == 12, 1, 0)

        dataFrame['rain'] = np.where((dataFrame['warunki_pogodowe'].str.contains("Rain")) | (
        dataFrame['warunki_pogodowe'].str.contains("Drizzle")) | (
                                          dataFrame['warunki_pogodowe'].str.contains("Thunderstorm")) | (
                                          dataFrame['warunki_pogodowe'].str.contains("Hail")), 1, 0)
        dataFrame['fog'] = np.where(dataFrame['warunki_pogodowe'].str.contains("Fog"), 1, 0)
        dataFrame['mist'] = np.where(dataFrame['warunki_pogodowe'].str.contains("Mist"), 1, 0)
        dataFrame['snow'] = np.where(dataFrame['warunki_pogodowe'].str.contains("Snow"), 1, 0)
        dataFrame['partly cloudy'] = np.where(dataFrame['warunki_pogodowe'].str.contains("Partly Cloudy"), 1,
                                                   0)
        dataFrame['overcast'] = np.where(dataFrame['warunki_pogodowe'].str.contains("Overcast"), 1, 0)
        dataFrame['clear'] = np.where(dataFrame['warunki_pogodowe'].str.contains("Clear"), 1, 0)
        dataFrame['scattered clouds'] = np.where(
            dataFrame['warunki_pogodowe'].str.contains("Scattered Clouds"), 1, 0)
        dataFrame['mostly cloudy'] = np.where(dataFrame['warunki_pogodowe'].str.contains("Mostly Cloudy"), 1,
                                                   0)
        dataFrame['unknown'] = np.where(dataFrame['warunki_pogodowe'].str.contains("Unknown"), 1, 0)

        dataFrame['west'] = np.where(dataFrame['kierunek_wiatru'] == ("West"), 1, 0)
        dataFrame['wsw'] = np.where(dataFrame['kierunek_wiatru'] == ("WSW"), 1, 0)
        dataFrame['wnw'] = np.where(dataFrame['kierunek_wiatru'] == ("WNW"), 1, 0)
        dataFrame['variable'] = np.where(dataFrame['kierunek_wiatru'] == ("Variable"), 1, 0)
        dataFrame['south'] = np.where(dataFrame['kierunek_wiatru'] == ("South"), 1, 0)
        dataFrame['sw'] = np.where(dataFrame['kierunek_wiatru'] == ("SW"), 1, 0)
        dataFrame['ssw'] = np.where(dataFrame['kierunek_wiatru'] == ("SSW"), 1, 0)
        dataFrame['sse'] = np.where(dataFrame['kierunek_wiatru'] == ("SSE"), 1, 0)
        dataFrame['se'] = np.where(dataFrame['kierunek_wiatru'] == ("SE"), 1, 0)
        dataFrame['north'] = np.where(dataFrame['kierunek_wiatru'] == ("North"), 1, 0)
        dataFrame['nw'] = np.where(dataFrame['kierunek_wiatru'] == ("NW"), 1, 0)
        dataFrame['nnw'] = np.where(dataFrame['kierunek_wiatru'] == ("NNW"), 1, 0)
        dataFrame['nne'] = np.where(dataFrame['kierunek_wiatru'] == ("NNE"), 1, 0)
        dataFrame['ne'] = np.where(dataFrame['kierunek_wiatru'] == ("NE"), 1, 0)
        dataFrame['east'] = np.where(dataFrame['kierunek_wiatru'] == ("East"), 1, 0)
        dataFrame['ese'] = np.where(dataFrame['kierunek_wiatru'] == ("ESE"), 1, 0)
        dataFrame['ene'] = np.where(dataFrame['kierunek_wiatru'] == ("ENE"), 1, 0)

        dataFrame = dataFrame[1:]
        dataFrame = dataFrame.reset_index(drop=True)
        dataFrame['previousPM10'] = previousPM10
        dataFrame['prevHumidity'] = prevHumidity
        dataFrame['prevPressure'] = prevPressure
        dataFrame['prevWindSpeed'] = prevWindSpeed
        dataFrame['prevTemperature'] = prevTemperature

        onesColumn = np.ones((dataFrame.shape[0], 1))
        onesColumn = onesColumn.astype(np.float)
        dataFrame['ones'] = onesColumn

        dataFrameInput = dataFrame[['temperatura', 'wilgotnosc', 'predkosc_wiatru','rain','fog','mist','ones',
                                      'prevTemperature','prevHumidity','prevWindSpeed','west', 'wsw', 'wnw', 'variable',
                                      'south', 'sw', 'ssw',
                                      'sse', 'se', 'north', 'nw', 'nnw', 'nne', 'ne', 'east', 'ese', 'ene',

                                        'godzina 0', 'godzina 1','godzina 2','godzina 3','godzina 4',
'godzina 5','godzina 6','godzina 7','godzina 8','godzina 9','godzina 10','godzina 11','godzina 12','godzina 13',
'godzina 14','godzina 15','godzina 16','godzina 17','godzina 18','godzina 19','godzina 20','godzina 21','godzina 22',
'godzina 23','styczen','luty','marzec','kwiecien','maj','czerwiec','lipiec','sierpien','wrzesien','pazdziernik',
'listopad', 'grudzien', 'cisnienie','partly cloudy', 'overcast', 'clear', 'scattered clouds', 'mostly cloudy',
                                      'unknown','ones','prevPressure','previousPM10']]

        dataFrameInput = np.array(dataFrameInput)
        predictionArray = []
        for i in range(-hoursToPredict, 0 ):
          predictor = PredykcjaRegresja.Predictor(dataFrameInput[i])
          prediction = predictor.predict()
          predictionArray.append(prediction)
          if (i != -1):
              dataFrameInput[i+1][-1] = prediction


        return predictionArray