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
    now = datetime.now()
    message_with_time = f"{message} | {now}"
    print("Received message: " + message_with_time)

def client(host='192.168.0.178', port=4001):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    print("Connecting to %s port %s" % server_address)
    sock.connect(server_address)
    try:
        num = 0
        while True:
            message = "A006FF8B010001CE"
            print("Sending %s" % message)
            sock.sendall(bytes.fromhex(message))
            start_time = time.time()
            while (time.time() - start_time) < 1:
                messages = receive_data(sock)
                for msg in messages:
                    process_message(msg)
            num += 1
            print("num: %d" % num)
            time.sleep(1)

    except socket.error as e:
        print("Socket error: %s" % str(e))
    except Exception as e:
        print("Other exception: %s" % str(e))
    finally:
        print("Closing connection to the server")
        sock.close()

client()
