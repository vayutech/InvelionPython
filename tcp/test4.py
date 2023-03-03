from time import sleep
import socket
import threading

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
        num = 0
        while True:
            message = "A006FF8B010001CE"
            print("Sending %s" % message)
            sock.sendall(bytes.fromhex(message))
            messages = receive_data(sock)
            for msg in messages:
                process_message(msg)
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
