from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
from numpy import nan

class PollutionDownloader(object):
    def __init__(self, url):
        self.url = url

    def downloadData(self):

        k=0
        frames=[]
        while True:
            link = self.url +str(k)

            k=k+1
            r = requests.get(link)
            data = r.text
            soup = BeautifulSoup(data,"lxml")

            table = soup.find_all('table')[0]
            rows = table.find_all('tr')[2:-3]

            data = {
                    'date' :[],
                    'pm10' : [],
                    'pm25' : [],
                    'o3' : [],
                    'no2' : [],
                    'so2' : [],
                    'co' : []
                   }

            for row in rows:
                value = row.find_all('td')
                try:
                    data['pm10'].append(float((value[0].get_text()).replace(",",".")))
                except ValueError:
                    data['pm10'].append(float ('NaN'))
                try:
                    data['pm25'].append(float((value[1].get_text()).replace(",",".")))
                except ValueError:
                    data['pm25'].append(float ('NaN'))
                try:
                    data['o3'].append(float((value[2].get_text()).replace(",",".")))
                except ValueError:
                    data['o3'].append(float ('NaN'))
                try:
                    data['no2'].append(float((value[3].get_text()).replace(",",".")))
                except ValueError:
                    data['no2'].append (float('NaN'))
                try:
                    data['so2'].append(float((value[4].get_text()).replace(",", ".")))
                except ValueError:
                    data['so2'].append(float('NaN'))
                try:
                  data['co'].append(float((value[6].get_text()).replace(",",".")))
                except ValueError:
                    data['co'].append(float('NaN'))

            tbody = soup.find_all('tbody')[0]
            szukane = (tbody.find_all('th'))[0:-3]

            for element in szukane:
                dodamToData = str(element.get_text()[0:10])
                dodamToGodzina = str(element.get_text()[12:17])
                sformatowanaData= str(dodamToData+' '+dodamToGodzina)
                sformatowanaDataTa = str(datetime.strptime(sformatowanaData,'%d.%m.%Y %H:%M'))
                data['date'].append(sformatowanaDataTa)

            df = pd.DataFrame.from_dict(data)
            if df.empty:
                break
            else:
                frames.append(df)
        df=pd.concat(frames).reset_index(drop = False)
        df= pd.DataFrame(df)
        df.fillna(value=nan, inplace=True)

        df = df[['pm10','pm25','index','date']]
        df = df.dropna(thresh=2)

        for x in range(0, df.__len__()):
            df['date'][x] = df['date'][x][0:16]

        df=df.dropna(axis=1,how='all')
        del df['index']

        df=df.dropna(thresh=2)
        pollutionDataFrame = df
        return pollutionDataFrame
