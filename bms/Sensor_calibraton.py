import numpy as np
import matplotlib.pyplot as plt

def csvToList(filename):
    
    Xarray=list()
    Yarray=list()
    dataFile=open(filename,'r')
    unformattedData=dataFile.readlines()
    formattedData=list()
    del unformattedData[0]
    for line in unformattedData:
        lineReading=line.split(',')
        Xarray.append(float(lineReading[0]))
        Yarray.append(float(lineReading[1]))
    #print(Xarray[0]+1)
    formattedData.append(Xarray)
    formattedData.append(Yarray)
    return formattedData

def getPolynomialVal(Xvals,Yvals,order):
    
    newYvals=list()
    coefficients=np.polyfit(Xvals,Yvals,order)
    for X in Xvals:
        Y=0
        i = 0
        while order - i >= 0:
            Y += coefficients[i] * X ** (order - i)
            i += 1
        newYvals.append(Y)
    return newYvals

    
        

formattedDt=csvToList('voltmeter_calibration.csv')
new=getPolynomialVal(formattedDt[0],formattedDt[1],2)
plt.scatter(formattedDt[0],formattedDt[1],color='r',label='without calibrating')
plt.plot(formattedDt[0],new,color='g',label='after calibrating')
plt.xlabel("Arduino readings")
plt.ylabel("Voltmeter readings")
plt.title("Calibration")
plt.legend()
plt.show()
coefficients=np.polyfit(formattedDt[0],new,2)
print(coefficients)
#print(new)
    