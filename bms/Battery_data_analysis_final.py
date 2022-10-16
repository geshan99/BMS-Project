import numpy as np
import matplotlib.pyplot as plt

def csvToList(fileName):
    dataFile = open(fileName, 'r')
    unformattedData = dataFile.readlines()
    formattedData = list()
    # get rid of column titles
    del unformattedData[0]
    # split the data by column, put in a formatted data list
    for line in unformattedData:
        currentLine = line.split(',')
        measurementNumber = int(currentLine[0])
        voltage = float(currentLine[1])
        formattedData.append([measurementNumber, voltage])
    dataFile.close()
    return formattedData

def findAnomalyIndex(dataList):
    anomalyIndexList = list()
    for i in range(len(dataList)):
        if i != 0:
            if dataList[i][1] - dataList[i-1][1] > .01:
                anomalyIndexList.append(i)
    return anomalyIndexList

def fixSingleAnomaly(anomalyIndex, dataSet):
    surroundingAverage = abs((dataSet[anomalyIndex + 1][1] + dataSet[anomalyIndex - 1][1])/2)
    dataSet[anomalyIndex][1] = surroundingAverage
    
def flipList(inputList):
    flippedList = list()
    for i in range(len(inputList)):
        flippedList.append(inputList[len(inputList) - i - 1])
    return flippedList

def createArray(listX, listY):
    newList = list()
    for i in range(len(listX)):
        newList.append([listX[i], listY[i]])
    return np.array(newList)

def createSpacedList(min, max, spacing):
    currentVal = min
    spacedList = list()
    i = 0
    while currentVal < max:
        currentVal = min + (i * spacing)
        spacedList.append(currentVal)
        i += 1
    return spacedList

def getPolyFitValues(order, xList, yList):
    coefficients = np.polyfit(xList, yList, order)
    #print(coefficients)
    modeledValues = list()
    for x in xList:
        yVal = 0
        i = 0
        while order - i >= 0:
            yVal += coefficients[i] * x ** (order - i)
            i += 1
        modeledValues.append(yVal)
        #if x==3.8:
            #print(yVal)
        #print(x,yVal)
    return modeledValues

def getChiSquaredValue(experimentalValues, modeledValues):
    totalChiSquared = 0
    for i in range(len(experimentalValues)):
        expectedValue = modeledValues[i]
        observedValue = experimentalValues[i]
        if expectedValue != 0:
            totalChiSquared += abs(((observedValue - expectedValue)**2) / expectedValue)
        elif abs(observedValue - expectedValue) <= 0.000001:
            totalChiSquared += 0
        else:
            totalChiSquared += (observedValue + expectedValue)**2
    return totalChiSquared

def findOptimalOrderFit(xValues, yValues):
    n = 1
    chiSquaredResults = list()
    while n <= 8:
        currentChiSquared = getChiSquaredValue(yValues, getPolyFitValues(n, xValues, yValues))
        chiSquaredResults.append([n, currentChiSquared])
        n += 1
    minIndex = 0
    minChiSquared = 1000000000.0
    for i in range(len(chiSquaredResults)):
        if chiSquaredResults[i][1] < minChiSquared:
            minChiSquared = chiSquaredResults[i][1]
            minIndex = i
    return chiSquaredResults[minIndex]

def printFittingResults(chiSquaredResults, xValues, yValues):
    #print("Optimal Order Fit:", chiSquaredResults[0])
    #print("Chi-Squared Value:", chiSquaredResults[1])
    print("Coefficients:")
    coefficientList = np.polyfit(xValues, yValues, chiSquaredResults[0])
    order = chiSquaredResults[0]
    for i in range(len(coefficientList)):
        print("\tx^" + str(order - i) +":", coefficientList[i])
        
def main():
    
    batteryData1 = csvToList("voltage_readings.csv")
    measurementNumbers1 = list()
    voltageReading1 = list()
    for data in batteryData1:
        measurementNumbers1.append(data[0])
        voltageReading1.append(data[1])

    anomalies = findAnomalyIndex(batteryData1)
    
    for anomaly in anomalies:
        fixSingleAnomaly(anomaly - 1, batteryData1)

    measurementNumbers1 = list()
    voltageReading1 = list()
    for data in batteryData1:
        measurementNumbers1.append(data[0])
        voltageReading1.append(data[1])

    measurementsAdjusted = flipList(measurementNumbers1)
    voltageReadingFinal = flipList(voltageReading1)

    # Normalize the data measurement numbers on a 0 to 100% scale
    numMeasurements = len(measurementsAdjusted)
    increment = 100.0/numMeasurements
    normalizedSoC = list()
    tempI = 0
    while tempI < numMeasurements:
        normalizedSoC.append(tempI*increment)
        tempI += 1

    optimalFitValues = findOptimalOrderFit(voltageReadingFinal, normalizedSoC)
    optimalOrder = optimalFitValues[0]
    modeledValues = getPolyFitValues(optimalOrder, voltageReadingFinal, normalizedSoC)
    #print(modeledValues)
  
    printFittingResults(optimalFitValues, voltageReadingFinal, normalizedSoC)
    
    #plot
    plt.plot(voltageReadingFinal, normalizedSoC, label='Experimental Data')
    plt.plot(voltageReadingFinal, modeledValues, label='Polynomial Fit')
    plt.legend(loc='best')
    plt.ylabel('State of Charge (%)')
    plt.xlabel('Cell Voltage (V)')
    plt.title('SoC vs Cell Voltage',fontweight='700')
    plt.grid(True)
    plt.subplots_adjust(wspace=0.35)

    plt.show()


main()

