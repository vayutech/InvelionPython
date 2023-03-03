import serial
import time
from datetime import datetime
import threading

port = 'COM6'
baud_rate = 115200
byte_size = serial.EIGHTBITS
parity = serial.PARITY_NONE
stop_bits = serial.STOPBITS_ONE

def get_timestamp_format(time):
    return datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

def save_data(chip_code, time):
    file_name = chip_code + " " + time + ".txt"
    with open("passings/" + file_name, "a") as file:
        file.write(chip_code + " | " + time + "\n")
    file.close()

try:
    ser = serial.Serial(port, baud_rate, byte_size, parity, stop_bits)
    if ser.is_open:
        print(f"Conexão com a porta {port} estabelecida.")
    ser.timeout = 0.050
except serial.SerialException as e:
    print(f"Erro ao abrir a porta {port}: {e}")
    exit()

while True:
    command_send = bytes.fromhex("A0 06 FF 8B 01 00 01 CE")
    ser.write(command_send)
    command_send_time = time.time()
    print("Loop Start - (0.000seg)")
    packages = 0
    while True:
        byte = ser.read()

        byte_int = int.from_bytes(byte, byteorder='big')

        if byte_int == 0xA0:
            header_capture_time = time.time()
            size = ser.read()
            size_int = int.from_bytes(size, byteorder='big')
            msg = ser.read(size_int)
            
            if(size_int == 10):
                break
            
            msg_full = bytearray()
            msg_full.append(byte_int)
            msg_full.append(size_int)
            msg_full.extend(msg)
            msg_full_str = ''.join(hex(x)[2:].zfill(2) for x in msg_full)
            chip_code = msg_full_str[34:38].upper()
            
            #thread = threading.Thread(target=save_data, args=(chip_code, get_timestamp_format(header_capture_time)))
            #thread.start()

            print(
                  get_timestamp_format(header_capture_time), " | ",
                  "\t", chip_code, " | ",
                  "\t (", "{:.3f}".format(header_capture_time - command_send_time), "seg)"
            )
            
            packages += 1

        if time.time() - command_send_time > 1:
            break

    end_time = time.time()
    sleep_time = 0.1 - (end_time - command_send_time)
    if(packages):
        print(
            "Tempo leituras: ", 
            "{:.3f}".format(end_time - command_send_time),
            "\t | ",
            "\t #", packages, "  | ",
            "\t (", "{:.3f}".format(end_time - command_send_time), "seg)",
            " - Sleep: ", "{:.3f}".format(sleep_time), "seg",
            "\n")
    else:
        print("Nenhum pacote recebido\n")

    #if sleep_time > 0:
        #time.sleep(sleep_time)
        
        
ser.close()
