import time
import socket
from datetime import datetime

def receive_data(sock):
    buffer = sock.recv(1024 * 4)
    buffer = buffer.hex()
    messages = []
    while len(buffer) > 0:
        index = buffer.find("a0")
        if index == -1:
            break
        message = buffer[index:index+42]
        messages.append(message)
        buffer = buffer[index+42:]
    return messages

def process_message(message):
    chip_code = message[34:38].upper()
    battery_level = message[8:10].upper()
    now = datetime.fromtimestamp(time.time())
    now_str = now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    file_name = chip_code + " " + now_str + ".txt"
    with open("passings/" + file_name, "a") as file:
        file.write(chip_code + 
                    "_|_" + 
                    now_str +
                    "_|_" + 
                    battery_level +
                    "\n"
                )
    file.close()

def client(host='192.168.0.178', port=4001):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    print("Connecting to %s port %s" % server_address)
    sock.connect(server_address)
    try:
        readings, second, sends = [], datetime.now().second, 0
        while True:
            message = "A006FF8B010001CE"
            sock.sendall(bytes.fromhex(message))
            sends += 1
            messages = receive_data(sock)
            for msg in messages:
                if not msg:
                    continue
                size = int(msg[2:4], 16)
                if(size == 19):
                    readings.append(msg)
                    process_message(msg)
            old_second = second
            second = datetime.now().second
            if second != old_second:
                print("Second: %d" % second, "Sends: %d" % sends, "Readings: %d" % len(readings))
                readings = []
                sends = 0
            #time.sleep(1)
            
    except socket.error as e:
        print("Socket error: %s" % str(e))
    except Exception as e:
        print("Other exception: %s" % str(e))
    finally:
        print("Closing connection to the server")
        sock.close()

client()