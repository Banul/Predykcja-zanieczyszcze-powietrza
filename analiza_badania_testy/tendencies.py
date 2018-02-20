from sklearn.utils import shuffle

# klasa badajaca tendencje (wzrost/spadek) dla regresji liniowej


class TendencyCreator(object):

    def divideOnTestAndTrainData(self, dataFrame):
        allCatValues = self.getClassifierForWholeDataFrame(dataFrame)
        dataFrame = dataFrame[0:-3]
        dataFrame = dataFrame.reset_index(drop=True)
        dataFrame = shuffle(dataFrame)
        dataFrameTrain = dataFrame[0:7000]
        dataFrameTest = dataFrame[7000:]
        testIndexes = [i for i in list(dataFrameTest.index.values)]
        print "maxTest", max(testIndexes)
        trainIndexes = [i for i in list (dataFrameTrain.index.values)]
        print "max", max(trainIndexes)
        testCatValues = [k for k in map(lambda x: allCatValues[x], testIndexes )]

        return dataFrameTrain, dataFrameTest, testIndexes, trainIndexes, testCatValues



    def getClassifierForWholeDataFrame(self, dataFrame):
        allCatValArr = self.createCatValArray(dataFrame)

        return allCatValArr

    def getPM10Differance(self, index, dataFrame):
        if index > 0:
            diff = float(dataFrame.iloc[index,-1]) - float (dataFrame.iloc[index-1,-1])
            if diff > 0:
                return 1
            else:
                return 0

    def createCatValArray(self, dataFrame):
        catValArr = []
        for index, row in dataFrame.iterrows():
            if index<len(dataFrame)-1:
                catVal = self.getPM10Differance(index, dataFrame)
                catValArr.append(catVal)
        return catValArr
