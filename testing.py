import serial
import time

def readSerialLine(ser):
    line = ser.readline()
    line = line.decode("utf-8")
    dataLine = line
    lineOutput = dataLine.strip()
    return lineOutput

def main():
    serial_port='COM6'
    baud_rate=9600
    
    arduino=serial.Serial(serial_port,baud_rate,timeout=1)
    while True:
    
    #get voltage measurements
        time.sleep(4)
        arduino.write(str.encode('1'))
        while arduino.inWaiting()<0:
            time.sleep(0.1)
        arduinoData=readSerialLine(arduino)
        initialVoltage=float(arduinoData)
    
    #get current measurement
        time.sleep(2)
        arduino.write(str.encode('2'))
        while arduino.inWaiting()<0:
            time.sleep(0.1)
        arduinoData=readSerialLine(arduino)
        initialCurrent=float(arduinoData)
        print('------------updated----------')
        print(f'voltage:{initialVoltage}V')
        print(f'current:{initialCurrent}A')
      
    
    
    
  
       
        
main()