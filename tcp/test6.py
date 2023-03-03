from time import sleep
import socket
import threading

def receive_data(sock, buffer):
    data = sock.recv(1024 * 4)
    if not data:
        return False
    buffer += data.hex()
    return True

def process_message(message):
    # Aqui você pode fazer o processamento desejado para cada mensagem
    print("Received message: " + message)

def client(host='192.168.0.178', port=4001):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the server
    server_address = (host, port)
    print("Connecting to %s port %s" % server_address)
    sock.connect(server_address)
    # Send data
    try:
        buffer = ""
        while True:
            message = "A006FF8B010001CE"
            print("Sending %s" % message)
            sock.sendall(bytes.fromhex(message))
            while receive_data(sock, buffer):
                index = buffer.find("a0")
                if index == -1:
                    break
                message = buffer[index:index+28]
                process_message(message)
                buffer = buffer[index+28:]
            sleep(1)

    except socket.error as e:
        print("Socket error: %s" % str(e))
    except Exception as e:
        print("Other exception: %s" % str(e))
    finally:
        print("Closing connection to the server")
        sock.close()

client()
