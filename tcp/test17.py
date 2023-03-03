import time
from time import sleep
import socket
from datetime import datetime

def receive_data(sock):
    message = ""
    messages = []
    while True:
        byte = sock.recv(1)
        if not byte:
            # a conexão foi encerrada
            break
        
        byte_hex = byte.hex()
        if byte_hex == "a0":
            # encontrou o cabeçalho 0xA0, aciona o evento
            if message:
                messages.append(message)
                message = ""
        message += byte_hex
        
    # adiciona a última mensagem recebida
    if message:
        messages.append(message)
    
    return messages


def process_message(message):
    now = datetime.fromtimestamp(time.time())
    now_str = now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    message_with_time = f"{message} | {now_str}"
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
            messages = receive_data(sock)
            for msg in messages:
                print("msg: %s" % msg)
                #process_message(msg)
            num += 1
            print("num: %d" % num)
            sleep(1)
            
    except socket.error as e:
        print("Socket error: %s" % str(e))
    except Exception as e:
        print("Other exception: %s" % str(e))
    finally:
        print("Closing connection to the server")
        sock.close()

client()