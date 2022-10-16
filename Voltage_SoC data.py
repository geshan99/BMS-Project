import serial


def main():

    # declare port, baud, and file path
    serial_port = 'COM6'
    baud_rate = 9600
    write_to_file_path = "Battery_voltage.csv"

    # open file for writing and  get serial feed
    output_file = open(write_to_file_path, "w+")
    ser = serial.Serial(serial_port, baud_rate)

    # write serial output to a csv file
    output_file.write("Data Point" + "," + "Voltage" + "\n")
    while True:
        line = ser.readline()
        line = line.decode("utf-8")
        data_line = line
        print(line, end="")
        #output_file.write(line)
        voltage = float(data_line.split(",")[1])
        dataPoint=str(data_line.split(',')[0])
        write_line=dataPoint+','+str(voltage)+'\n'
        output_file.write(write_line)
        # when batteries have been depleted
        if voltage < 2.4:
            break
    output_file.close()

main()


