import time
from time import sleep
import socket
from datetime import datetime
import binascii

def receive_data(sock):
    buffer = ""
    message_started = False
    message = ""
    while True:
        # Recebe um byte de cada vez com timeout curto
        try:
            byte = sock.recv(1, socket.MSG_DONTWAIT).decode()
            if byte:
                buffer += byte
                if buffer.endswith("a0"):
                    # Começou uma nova mensagem
                    if message_started:
                        # Se já tinha uma mensagem em progresso, termina ela antes
                        yield message
                    message_started = True
                    message = buffer[-2:]
                    print("New message started: %s" % message)
                elif len(message) > 0:
                    # Continua a mensagem em progresso
                    message += buffer[-2:]
        except socket.error:
            pass
        
        # Verifica se a mensagem atual terminou
        if message_started and len(message) == 42:
            message_started = False
            yield message
        
        # Verifica se já passou tempo suficiente
        if not message_started:
            sleep(0.1)

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
                print("New message received: %s" % msg)
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
