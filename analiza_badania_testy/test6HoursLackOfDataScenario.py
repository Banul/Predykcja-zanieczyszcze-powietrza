import numpy as np
from sklearn.utils import shuffle
from sklearn import datasets, linear_model, preprocessing
import os
import dataReturner

# Skrypt testuje działanie systemu w przypadku braku danych przez 6 godzin


dataReturner = dataReturner.dataReturner()
mainDataFrame = dataReturner.returnData()
mainDataFrame = mainDataFrame

mainArr = []
tempArr = []

for index, row in mainDataFrame.iterrows():
    if (index%17 == 0) & (index!=0):
        mainArr.append(tempArr)
        tempArr = []
    tempArr.append(np.array(row))

#mainArr = shuffle(mainArr)
trainData = mainArr[100:]
testData = mainArr[0:100]


listOfElements = [k for k in range(7,17)]
listOfElements.append(0)
listOfElements.sort()

for counter,item in enumerate(testData):
    newItem = [item [n] for n in listOfElements]
    testData[counter] = newItem


mainTrainOutpArr = []
mainTrainInpArr = []
mainTestOutpArr = []
mainTestInpArr = []

for item in trainData:
    for element in item:
        mainTrainOutpArr.append(round(element[0],1))
        mainTrainInpArr.append(element[1:])
mainTrainOutpArr = np.array(mainTrainOutpArr)
mainTrainInpArr = np.array(mainTrainInpArr)

regr = linear_model.LinearRegression()
regr.fit(mainTrainInpArr, mainTrainOutpArr)


if os.path.exists("err6hLack1hPrediction.txt"):
    append_write = 'a' # append if already exists
else:
    append_write = 'w' # make a new file if not

text_file1 = open("err6hLack1hPrediction.txt", append_write)
text_file2 = open("err6hLack2hPrediction.txt", append_write)
text_file3 = open("err6hLack3hPrediction.txt", append_write)
text_file4 = open("err6hLack4hPrediction.txt", append_write)
text_file5 = open("err6hLack5hPrediction.txt", append_write)
text_file6 = open("err6hLack6hPrediction.txt", append_write)
text_file7 = open("err6hLack7hPrediction.txt", append_write)
text_file8 = open("err6hLack8hPrediction.txt", append_write)
text_file9 = open("err6hLack9hPrediction.txt", append_write)
text_file10 = open("err6hLack10hPrediction.txt", append_write)



for cnter, item in enumerate(testData):
    historicData = item[0][1:-37]
    output = item[0][0]
    for counter, arr in enumerate(item):
        if counter!=0:
            arr[-1] = output
            arr[1:-37] = historicData
        predicted = regr.predict(arr[1:])
        relativeErr = abs(predicted - arr[0])*100/arr[0]
        relativeErr = round(relativeErr,2)
        if counter == 1:
            text_file1.write(str(relativeErr))
            text_file1.write('\n')
        if counter == 2:
            text_file2.write(str(relativeErr))
            text_file2.write('\n')
        if counter == 3:
            text_file3.write(str(relativeErr))
            text_file3.write('\n')
        if counter == 4:
            text_file4.write(str(relativeErr))
            text_file4.write('\n')
        if counter == 5:
            text_file5.write(str(relativeErr))
            text_file5.write('\n')
        if counter == 6:
            text_file6.write(str(relativeErr))
            text_file6.write('\n')
        if counter == 7:
            text_file7.write(str(relativeErr))
            text_file7.write('\n')
        if counter == 8:
            text_file8.write(str(relativeErr))
            text_file8.write('\n')
        if counter == 9:
            text_file9.write(str(relativeErr))
            text_file9.write('\n')
        if counter == 10:
            text_file10.write(str(relativeErr))
            text_file10.write('\n')

