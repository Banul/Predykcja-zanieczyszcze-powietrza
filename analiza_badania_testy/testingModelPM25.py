import numpy as np
from sklearn.utils import shuffle
from sklearn import datasets, linear_model, preprocessing
import os
import dataReturner

# test dla modelu PM25, umieszczanie danych w plikach .txt


dataReturner = dataReturner.dataReturner()
mainDataFrame = dataReturner.returnData()
print mainDataFrame

mainArr = []
tempArr = []
for index, row in mainDataFrame.iterrows():
    if (index%10 == 0) & (index!=0):
        mainArr.append(tempArr)
        tempArr = []
    tempArr.append(np.array(row))

#mainArr = shuffle(mainArr)
trainData = mainArr[100:]
testData = mainArr[0:100]

mainTrainOutpArr = []
mainTrainInpArr = []

mainTestOutpArr = []
mainTestInpArr = []

for item in trainData:
    for element in item:
        mainTrainOutpArr.append(round(element[0],1))
        mainTrainInpArr.append(element[2:])
mainTrainOutpArr = np.array(mainTrainOutpArr)
mainTrainInpArr = np.array(mainTrainInpArr)


regr = linear_model.LinearRegression()
regr.fit(mainTrainInpArr, mainTrainOutpArr)

# element 0 -> output PM25
# element -1 -> prevPM10

if os.path.exists("err1hPM25.txt"):
    append_write = 'a' 
else:
    append_write = 'w' 

text_file1 = open("err1hPM25.txt", append_write)
text_file2 = open("err2hPM25.txt", append_write)
text_file3 = open("err3hPM25.txt", append_write)
text_file4 = open("err4hPM25.txt", append_write)
text_file5 = open("err5hPM25.txt", append_write)
text_file6 = open("err6hPM25.txt", append_write)
text_file7 = open("err7hPM25.txt", append_write)
text_file8 = open("err8hPM25.txt", append_write)
text_file9 = open("err9hPM25.txt", append_write)
text_file10 = open("err10hPM25.txt", append_write)

for item in testData:
    predicted = -2
    for counter, arr in enumerate(item):
        if predicted != -2:
            arr[-1] = predicted
        predicted = regr.predict(arr[2:])
        relativeErr = abs(predicted*0.81 - arr[0])*100/arr[0]
        relativeErr = round(relativeErr,2)

        if counter == 0:
            text_file1.write(str(relativeErr))
            text_file1.write('\n')
        if counter == 1:
            text_file2.write(str(relativeErr))
            text_file2.write('\n')
        if counter == 2:
            text_file3.write(str(relativeErr))
            text_file3.write('\n')
        if counter == 3:
            text_file4.write(str(relativeErr))
            text_file4.write('\n')
        if counter == 4:
            text_file5.write(str(relativeErr))
            text_file5.write('\n')
        if counter == 5:
            text_file6.write(str(relativeErr))
            text_file6.write('\n')
        if counter == 6:
            text_file7.write(str(relativeErr))
            text_file7.write('\n')
        if counter == 7:
            text_file8.write(str(relativeErr))
            text_file8.write('\n')
        if counter == 8:
            text_file9.write(str(relativeErr))
            text_file9.write('\n')
        if counter == 9:
            text_file10.write(str(relativeErr))
            text_file10.write('\n')
