import matplotlib.pyplot as plt

dataFile=open("Samsung_18650_set3_run_2.csv",'r')
writeFile = open("voltage_readings.csv",'w')
writeFile.write("Data point"+','+"Voltage(V)\n")
dataList=dataFile.readlines()
list1=list()

del dataList[0]
i=1
for data in dataList:
    
    if data!='\n':
        temp_list=[]
        temp_list.append(i)
        temp_list.append(float(data))
        #list1.append(temp_list)
        writeFile.write(str(i)+','+data)
        list1.append(float(data))
        i+=1
       
dataFile.close()
writeFile.close()
xList=[x for x in range(0,len(dataList))]
plt.scatter(xList,dataList,color='r',label='Battery Data')
plt.show()
print(list1)

