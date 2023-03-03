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

readings, second, sends = [], datetime.now().second, 0
while True:
    command_send = bytes.fromhex("A0 06 FF 8B 01 00 01 CE")
    ser.write(command_send)
    sends += 1
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
            readings.append(chip_code)
            
            thread = threading.Thread(target=save_data, args=(chip_code, get_timestamp_format(header_capture_time)))
            thread.start()
    
    old_second = second
    second = datetime.now().second
    if second != old_second:
        print("Second: %d" % second, "Sends: %d" % sends, "Readings: %d" % len(readings))
        readings = []
        sends = 0
        
ser.close()
