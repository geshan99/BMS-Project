import numpy as np
import matplotlib.pyplot as plt

def csvToList(file_path):
    data_file=open(file_path,'r')
    unformatted_data=data_file.readlines()
    formatted_data=list()
    
    titleNames=unformatted_data[0].split(',')
    relevantData=unformatted_data[1:]
    
    for line in relevantData:
        currentLine=line.split(',')
        time=float(currentLine[0])
        estimate1=float(currentLine[1]) #culombcounting
        estimate2=float(currentLine[2]) #OCV
        estimate3=float(currentLine[3]) #KF
        formatted_data.append([time,estimate1,estimate2,estimate3])
    data_file.close()
    return([titleNames,formatted_data])

def fixOCVData(OCVlist,timelist):
    lastOCV=-100.0
    fixedOCVlist=list()
    for i in range(len(OCVlist)):
        if lastOCV!=OCVlist[i]:
            fixedOCVlist.append([timelist[i],OCVlist[i]])
            lastOCV=OCVlist[i]
    return(fixedOCVlist)
            
def main():
    data_set=csvToList('kalman_400ms.csv')
    rel_data=data_set[1]
    
    timeMeasurements=list()
    OCVEstMeasurements=list()
    culombCountMeasurements=list()
    kalmanMeasurements=list()
    
    for line in rel_data:
        timeMeasurements.append(line[0])
        culombCountMeasurements.append(line[1])
        OCVEstMeasurements.append(line[2])
        kalmanMeasurements.append(line[3])
    
    newOCVdata=fixOCVData(OCVEstMeasurements,timeMeasurements)
    newTimelist=list()
    newOCVlist=list()
    
    for data in newOCVdata:
        newTimelist.append(data[0])
        newOCVlist.append(data[1])
        
    plt.title('SoC Estimation Analysis')    
    plt.plot(timeMeasurements,culombCountMeasurements,label='Culomb Counting')
    plt.plot(timeMeasurements,kalmanMeasurements,label='Kalman Filtering')
    plt.plot(newTimelist,newOCVlist,'r',label='Voltage method')
    plt.legend(loc='best')
    plt.xlabel('Time(ms)')
    plt.ylabel('SoC(%)')
    plt.show()
    
    
main()
    