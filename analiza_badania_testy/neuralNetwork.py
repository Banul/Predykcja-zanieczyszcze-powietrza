import numpy as np

# implementacja sieci wzieta z :
# https://github.com/stephencwelch/Neural-Networks-Demystified



class Neural_Network(object):
    def __init__(self, Lambda=0 ):
        # Define Hyperparameters
        self.inputLayerSize = 100
        self.outputLayerSize = 1
        self.hiddenLayerSize = 50
        self.Lambda = Lambda

        # Weights (parameters)
        self.W1 = np.random.randn(self.inputLayerSize, self.hiddenLayerSize)
        self.W2 = np.random.randn(self.hiddenLayerSize, self.outputLayerSize)

    def returnFirstError(self, X, T, diff):
        errAvg = []
        Yhat = self.forward(X)
        for i in range(0, len(T)):
            if T[i]!=0:
                relErr = abs(T[i] * diff - Yhat[i] * diff) / T[i] * diff
                errAvg.append(relErr)
        return sum(errAvg)/len(errAvg)



    def forward(self, X):
        # Propagate inputs though network
        self.z2 = np.dot(X, self.W1)
        self.a2 = self.sigmoid(self.z2)
        self.z3 = np.dot(self.a2, self.W2)
        yHat = self.sigmoid(self.z3)
        return yHat

    def sigmoid(self,z):
        return 1 / (1 + np.exp(-z))

    def sigmoidPrime(self,z):
        # Derivative of sigmoid function
        return np.exp(-z) / ((1 + np.exp(-z)) ** 2)

    def costFunction(self, X, y):
        # Compute cost for given X,y, use weights already stored in class.
        self.yHat = self.forward(X)
        J = 0.5*sum((y-self.yHat)**2) + (self.Lambda/2)*(np.sum(self.W1**2)+np.sum(self.W2**2))
        return J

    def costFunctionWithoutParam(self, X, y):
        yHat = self.forward(X)
        J = 0.5*sum((y-yHat)**2) + (self.Lambda/2)*(np.sum(self.W1**2)+np.sum(self.W2**2))
        J = sum(J)
        return J

    def returnerYAndYhat (self, X, y):
        yHat = self.forward(X)

        return yHat, y


    def costFunctionPrime(self, X, y):
        # Compute derivative with respect to W and W2 for a given X and y:
        self.yHat = self.forward(X)
        delta3 = np.multiply(-(y - self.yHat), self.sigmoidPrime(self.z3))
        dJdW2 = np.dot(self.a2.T, delta3) + self.Lambda*self.W2
        delta2 = np.dot(delta3, self.W2.T) * self.sigmoidPrime(self.z2)
        dJdW1 = np.dot(X.T, delta2) + self.Lambda*self.W1

        return dJdW1, dJdW2

    def getParams(self):
        params = np.concatenate((self.W1.ravel(), self.W2.ravel()))
        return params

    def setParams(self, params):
        W1_start = 0
        W1_end = self.hiddenLayerSize * self.inputLayerSize
        self.W1 = np.reshape(params[W1_start:W1_end], (self.inputLayerSize, self.hiddenLayerSize))
        W2_end = W1_end + self.hiddenLayerSize * self.outputLayerSize
        self.W2 = np.reshape(params[W1_end:W2_end], (self.hiddenLayerSize, self.outputLayerSize))

    def setWeightsAsArrays(self, w1, w2):
        self.W1 = w1
        self.W2 = w2

    def computeGradients(self, X, y):
        dJdW1, dJdW2 = self.costFunctionPrime(X, y)
        return np.concatenate((dJdW1.ravel(), dJdW2.ravel()))
