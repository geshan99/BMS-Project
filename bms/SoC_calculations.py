import serial

coeffcients=[42456.74875114,-655660.6260594883,3047061.1509360303,977768.3352114791,-38488640.35216225,1037157.7714138603,586426305.9848473,-1626532633.9780855,1387926680.0836513]
ser = serial.Serial('COM5', 9600)

def getCapacity(voltage):
    i=8
    val=0
    for coe in coeffcients:
        val+=coe*float(voltage)**i
        i-=1
    return val
        
while True:
    line = ser.readline()
    line = line.decode("utf-8")
    lineData=line.split(',')
    cap1=getCapacity(lineData[0])
    cap2=getCapacity(lineData[1])
    print('Bat1_Cap = '+str(cap1)+' %')
    print('Bat2_Cap = '+str(cap2)+' %')
    #print('Voltage1 = '+str(float(line))+' V')
    #print(getCapacity(lineData[0]))
   
    