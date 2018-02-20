import currentAndPastWeatherDownloader
import pollutionDownloader
import pandas as pd
import futureWeatherDownloader
import psycopg2
from sqlalchemy import create_engine
import datetime
from dataHelperForJob import PredictorContainer

#Uruchomienie skryptu powoduje uaktualnienie danych w bazie

linksTable = ["http://powietrze.gios.gov.pl/pjp/current/station_details/table/550/3/0","http://powietrze.gios.gov.pl/pjp/current/station_details/table/544/3/0"
              ,"http://powietrze.gios.gov.pl/pjp/current/station_details/table/530/3/0","http://powietrze.gios.gov.pl/pjp/current/station_details/table/10434/3/0"
              ,"http://powietrze.gios.gov.pl/pjp/current/station_details/table/485/3/0"]

hoursToPredict = 5

class WeatherReturner(object):
    def downloadWeatherAndFutureWeather(self):
        dataWeather = currentAndPastWeatherDownloader.CurrentAndPastWeatherDownloader(72)
        currentWeatherDataFrame = dataWeather.downloadData()
        dataWeatherFuture = futureWeatherDownloader.FutureWeatherDownloader(hoursToPredict)
        futureWeatherDataFrame = dataWeatherFuture.downloadData()
        return currentWeatherDataFrame, futureWeatherDataFrame

class PollutionDownloaderHelper (object):

    def __init__(self, link,dataFrameWeather,dataFrameWeatherFuture,ID):

        self.link = link
        dataPollution = pollutionDownloader.PollutionDownloader(self.link)
        self.dataFramePollution = dataPollution.downloadData()
        self.dataFrameWeather = dataFrameWeather
        self.dataFrameWeatherFuture = dataFrameWeatherFuture
        self.ID = ID



class Helper(object):
    def __init__(self, stationId):
        self.id = stationId

    def countDifferance(self, lastDate):
        currDate = datetime.datetime.now()
        print "currDate"
        print currDate
        print "lastDate"
        print lastDate
        dateDifferance = (currDate - lastDate).total_seconds()/3600
        return dateDifferance

    def returnFinalDataFrame(self, weatherDataFrame, pollutionDataFrame, futureWeather, hoursToPredict):
        mergedDataFrame = pd.merge(weatherDataFrame, pollutionDataFrame, how='inner', on='date')
        mergedDataFrame = mergedDataFrame.sort_values(by="date")
        mergedDataFrame = pd.DataFrame.append(mergedDataFrame, futureWeather, ignore_index=True)

        mergedDataFrame = mergedDataFrame[
            ['temperatura', 'cisnienie', 'predkosc_wiatru', 'wilgotnosc', 'kierunek_wiatru', 'warunki_pogodowe', 'date',
             'pm10', 'pm25']]

        mergedDataFrame['date'] = pd.to_datetime(mergedDataFrame['date'])
        mergedDataFrame['temperatura'] = mergedDataFrame['temperatura'].astype(float)
        mergedDataFrame['cisnienie'] = mergedDataFrame['cisnienie'].astype(float)
        mergedDataFrame['predkosc_wiatru'] = mergedDataFrame['predkosc_wiatru'].astype(float)
        mergedDataFrame['wilgotnosc'] = mergedDataFrame['wilgotnosc'].astype(float)
        mergedDataFrame['id_stacji'] = self.id
        helperData = PredictorContainer()

        indexes = mergedDataFrame.index.values
        predictionsArrPM10 = helperData.transformAndPredict(mergedDataFrame, hoursToPredict)
        numbersOfIndexesForPM10Array = range(0, len(predictionsArrPM10))

        predictionsArrPM25 = [k for k in map(lambda x : predictionsArrPM10[x]*0.83, numbersOfIndexesForPM10Array)]

        for i in range(-hoursToPredict, 0):
            mergedDataFrame.set_value(indexes[i], 'pm10', round(predictionsArrPM10[i],1))
            mergedDataFrame.set_value(indexes[i], 'pm25', round(predictionsArrPM25[i],1))
            mergedDataFrame = mergedDataFrame[['temperatura', 'cisnienie', 'predkosc_wiatru', 'wilgotnosc',
            'kierunek_wiatru', 'warunki_pogodowe','date','pm10','pm25', 'id_stacji']]

        mergedDataFrame = mergedDataFrame.sort_values(by='date')
        finalDataFrame = mergedDataFrame
        return finalDataFrame



weatherReturner = WeatherReturner()
dataFrameWeather,dataFrameWeatherFuture = weatherReturner.downloadWeatherAndFutureWeather()
hoursToPredict = len(dataFrameWeatherFuture)
arrayOfDataFrames = []
idsToOmit = []
finalDataFrame = []
idsToDelete = []

for counter, link in enumerate(linksTable):
    id = counter+1
    downloaderPredictor = PollutionDownloaderHelper(link,dataFrameWeather,dataFrameWeatherFuture,id)
    pollutionDataFrame = pd.DataFrame(downloaderPredictor.dataFramePollution)
    if (pollutionDataFrame.empty):
        idsToOmit.append(id)
    if (not pollutionDataFrame.empty):
        dateHelper = Helper(id)
        table =  dateHelper.returnFinalDataFrame(dataFrameWeather, pollutionDataFrame, dataFrameWeatherFuture, hoursToPredict)
        diff = dateHelper.countDifferance(table.iloc[-hoursToPredict-1]['date'])

        if diff >= 6:
            idsToOmit.append(id)
        else:
            table = table.sort_values(by='date')
            arrayOfDataFrames.append(table)
            finalDataFrame = pd.concat(arrayOfDataFrames)
            finalDataFrame = pd.DataFrame(finalDataFrame)
            finalDataFrame = finalDataFrame.reset_index(drop=True)
            idsToDelete.append(id)


arrTablesToOmit = []
conn = psycopg2.connect("dbname='helloworld' user='helloworld' host='helloworld.cggjgttkvbq5.eu-central-1.rds.amazonaws.com' password='helloworld'")
cur = conn.cursor()

if len(idsToDelete) > 0:
    for id in idsToDelete:
        cur.execute('DELETE FROM "final_table" where id_stacji = ' + str(id) + ' ; ')

indexTable = pd.read_sql_query('select index from "final_table";', con=conn)
maxIndex  = pd.read_sql_query('select max(index) from "final_table";', con=conn)
maxIndex = maxIndex.values[0][0]
dataFrameToPushToDatabase = finalDataFrame

if (not indexTable.empty ):
    dataFrameToPushToDatabase.index += maxIndex+1

print dataFrameToPushToDatabase
dataFrameToPushToDatabase = pd.DataFrame(dataFrameToPushToDatabase)
print dataFrameToPushToDatabase
engine = create_engine(
'postgresql://helloworld:helloworld@helloworld.cggjgttkvbq5.eu-central-1.rds.amazonaws.com:5432/helloworld')
dataFrameToPushToDatabase.to_sql('final_table', engine, if_exists='append', index=True)
conn.commit()
conn.close()









