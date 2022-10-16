import numpy as np
import serial
import time

def readSerialLine(ser):
    line = ser.readline()
    line = line.decode("utf-8")
    dataLine = line
    lineOutput = dataLine.strip()
    return lineOutput

def getSoCFromOCV(OCV):
    coefficients = [-286.9048927614211, 5446.351538527408, -42701.39690121678, 177102.651630974, -410021.8330743389,
                    502646.275158812, -255008.70081787533]
    OCV_used = OCV
    
    if OCV_used < 2.5:
        OCV_used = 2.5093
    if OCV_used > 4.057:
        OCV_used = 4.057
    # calculates the state of charge from the OCV
    SoC = 0
    i = 0
    while 6 - i >= 0:
        SoC += coefficients[i] * OCV_used ** (6 - i)
        i += 1
    # returns the state of charge as a function of measured open circuit voltage (OCV)
    return SoC

def initStateVariable(SoC, I):
    return np.array([SoC], [I])

def updateTransformationMatrix(deltaT):
    totalCoulombs = 10800
    return np.array([[1, -1 * (deltaT / totalCoulombs) * 100], [0, 1]])

def main():
    serialPort = 'COM6'
    baudRate = 9600
    arduino = serial.Serial(serialPort, baudRate)
    time.sleep(2)
    
    write_to_file_path = "Kalman_Filter.csv"
    output_file = open(write_to_file_path, "w+")
    estimate1Name = "Coulomb Counting"
    estimate2Name = "Voltage method"
    estimate3Name = "Kakman Filter"
    output_file.write("Time" + "," + estimate1Name + "," + estimate2Name + "," + estimate3Name  + "\n")
    
    CURRENT_CODE = '2'
    OCV_CODE = '1'
    
    arduino.write(str.encode(OCV_CODE))
    while arduino.inWaiting() < 0:
        time.sleep(0.1)
    arduinoData = readSerialLine(arduino)
    initialVoltage = float(arduinoData) / 3 #batterry cells
    
    initialSoC = getSoCFromOCV(initialVoltage)
    #print(arduinoData)
    
    arduino.write(str.encode(CURRENT_CODE))
    while arduino.inWaiting() < 0:
        time.sleep(0.1)
    arduinoData = readSerialLine(arduino)
    if float(arduinoData)<0:
        arduinoData=0
    initialCurrent = float(arduinoData)/1#current
    
    displaySoC = round(initialSoC, 2)
    
    print("Battery Charge (" + estimate1Name + "): " + str(round(displaySoC, 2)) + "%")

    print("Battery Charge (" + estimate2Name + "): " + str(round(displaySoC, 2)) + "%")

    print("Battery Charge (" + estimate3Name + "): " + str(round(displaySoC, 2)) + "%")
    
    print("------------------------------------------")
    
    csvLine = "0.0" + "," + str(round(displaySoC, 2)) + "," + str(round(displaySoC, 2)) + "," + \
              str(round(displaySoC, 2)) +"\n"

    output_file.write(csvLine)
    
    lastState1 = np.array([[initialSoC], [initialCurrent]])
    lastState2 = np.array([[initialSoC], [initialCurrent]])
    lastState3 = np.array([[initialSoC], [initialCurrent]])
    
    lastVariance1 = np.array([[.5, 0], [0, .5]])
    lastVariance2 = np.array([[.5, 0], [0, .5]])
    lastVariance3 = np.array([[.5, 0], [0, .5]])
    
    observationMatrix = np.array([[1, 0], [0, 1]])
    
    observationNoise1 = np.array([[.25, 0], [0, .25]])
    observationNoise2 = np.array([[.25, 0], [0, .25]])
    observationNoise3 = np.array([[.25, 0], [0, .25]])
    
    totalCoulombs = 10800
    # Updated by Arduino
    deltaT = 0
    transformationMatrix = np.array([[1, -1 * (deltaT / totalCoulombs)*100], [0, 1]])
    
    operate = True
    dataStartTime = time.time()
    ocvStartTime = time.time()
    longCurrentStartTime = time.time()
    doLongCurrentUpdate = False
    extraTimeReference = 0
    extraTime = 0
    operationStartTime=time.time()
    
    while operate:
        
        startTime = time.time()
        
        time.sleep(10)
        
        transformationMatrix = updateTransformationMatrix(time.time() - startTime + extraTime)
        
        stateEstimate1 = np.matmul(transformationMatrix, lastState1)
        stateEstimate2 = lastState2
        stateEstimate3 = np.matmul(transformationMatrix, lastState3)
        
        varianceEstimate1 = np.matmul(np.matmul(transformationMatrix, lastVariance1), np.linalg.inv(transformationMatrix))
        varianceEstimate3 = np.matmul(np.matmul(transformationMatrix, lastVariance3), np.linalg.inv(transformationMatrix))
        
        extraTime = 0
        extraTimeReference = time.time()
        
        arduino.write(str.encode(CURRENT_CODE))
        while arduino.inWaiting() < 0:
            time.sleep(0.1)
        arduinoData = readSerialLine(arduino)#current
        if float(arduinoData)<0:
            stateCurrent=0
        stateCurrent = float(arduinoData)/1
        
        stateEstimate1[1] = stateCurrent
        stateEstimate3[1] = stateCurrent
        
        lastState1 = stateEstimate1
        lastState3 = stateEstimate3
        
        lastVariance1 = varianceEstimate1
        lastVariance3 = varianceEstimate3
        
        if time.time() - ocvStartTime > 6:
            
            arduino.write(str.encode(OCV_CODE))
            while arduino.inWaiting() < 0:
                time.sleep(0.1)
            arduinoData = readSerialLine(arduino)
            measuredVoltage = float(arduinoData) / 3 #batteries
            
            measuredSoC = getSoCFromOCV(measuredVoltage)
            measuredCurrent = stateCurrent
            
            stateMeasurement = np.array([[measuredSoC], [measuredCurrent]])
            
            measurementResidual3 = stateMeasurement - stateEstimate3
            
            residualVariance3 = varianceEstimate3 + observationNoise3
            
            kalmanGain3 = np.matmul(varianceEstimate3, np.linalg.inv(residualVariance3))
            
            lastState2 = stateMeasurement
            lastState3 = stateEstimate3 + np.matmul(kalmanGain3, measurementResidual3)
            
            lastVariance3 = np.matmul((np.identity(2) - kalmanGain3), varianceEstimate3)
            
            ocvStartTime = time.time()
            
        displaySoC1 = float(lastState1[0])
        print("Battery Charge (" + estimate1Name + "): " + str(round(displaySoC1, 2)) + "%")

        displaySoC2 = float(lastState2[0])
        print("Battery Charge (" + estimate2Name + "): " + str(round(displaySoC2, 2)) + "%")

        displaySoC3 = float(lastState3[0])
        print("Battery Charge (" + estimate3Name + "): " + str(round(displaySoC3, 2)) + "%")
        
        print("------------------------------------------")
        
        csvLine = str(round((time.time() - dataStartTime), 2)) + "," + str(round(displaySoC1, 2))+","+str(round(displaySoC2,2))+","+str(round(displaySoC3,2)) + "\n"
        output_file.write(csvLine)
        print(time.time()-operationStartTime)
        if time.time()-operationStartTime>200: #data collecting time
            break
            output_file.close()
        
       # extraTime = time.time() - extraTimeReference
        
main()
            
            
            
    