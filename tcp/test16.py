import socket
import datetime
import time
import select

def receive_data(sock):
    messages = []
    buffer = b''
    sock.setblocking(True)
    while True:
        data = sock.recv(1024)
        if not data:
            break
        buffer += data
        while b'a0' in buffer:
            index = buffer.find(b'a0')
            message = buffer[:index+2].hex()
            messages.append(message)
            buffer = buffer[index+2:]
    return messages


"""
def receive_data(sock):
    messages = []
    buffer = b''
    sock.setblocking(False)
    while True:
        ready = select.select([sock], [], [], 1)
        if ready[0]:
            buffer += sock.recv(1)
            print("buffer: %s" % buffer)
            while b'a0' in buffer:
                index = buffer.find(b'a0')
                message = buffer[:index+2].hex()
                messages.append(message)
                buffer = buffer[index+2:]
        else:
            break
    return messages
"""

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
            #for msg in messages:
                #print("Received message: %s" % msg)
            print("Received message: %s" % messages)
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
