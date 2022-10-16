   
import serial


def main():

    # declare port, baud, and file path
    serial_port = 'COM5'
    baud_rate = 9600
    write_to_file_path = "Samsung_18650_set3_run_3.csv"

    # open file for writing and  get serial feed
    output_file = open(write_to_file_path, "w")
    ser = serial.Serial(serial_port, baud_rate)

    # write serial output to a csv file
    #output_file.write("Data Point" + "," + "Voltage" + "\n")
    output_file.write("Voltage" + "\n")
    while True:
    #i=0
    #while i<=10:
        line = ser.readline()
        line = line.decode("utf-8")
        data_line = str(line)
        print(line, end="")
        #output_file.write(data_line)
        #if line==0:
            #print('empty')
        #output_file.write("hhghghgh"+ "\n")
        output_file.write(str(data_line))
        #voltage = float(data_line.split(",")[1])
        voltage = float(data_line)
        line=0
        # when batteries have been depleted
        if voltage < 3.50:
            break
        #i+=1
    output_file.close()

main()

