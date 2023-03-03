import socket
import datetime
import time
import select

def receive_data(sock):
    messages = []
    message = ''
    sock.setblocking(False)
    while True:
        ready = select.select([sock], [], [], 1)
        if ready[0]:
            buffer = sock.recv(1)
            if buffer.hex() == 'a0':
                #timestamp = datetime.datetime.now()
                #messages.append(message)
                #message = buffer.hex() + " | " + str(timestamp)
                #print("header found")
                message += buffer.hex()
            else:
                message += buffer.hex()
                
            if len(message) == 42:
                messages.append(message)
                message = ''

            if message == '0a018b00000000000000ca':
                break
            
            #if len(messages) > 0:
                #break
        else:
            break
    return messages

""" 
def receive_data(sock):
    message = ''
    sock.setblocking(False)
    while True:
        ready = select.select([sock], [], [], 1)
        if ready[0]:
            buffer = sock.recv(1)
            if buffer.hex() == 'a0':
                print("header found")
            message += buffer.hex()
        else:
            break
    return message
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
