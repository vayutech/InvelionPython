from time import sleep
import socket

def process_byte(byte):
    if(byte == "a0"):
        print("Found header")
    else:   
        print("Found byte: %s" % byte)

def receive_data(sock):
    while True:
        byte = sock.recv(1)
        hex = byte.hex()
        if not byte:
            # Connection closed by the server
            break
        process_byte(hex)

def client(host='192.168.0.178', port=4001):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    print("Connecting to %s port %s" % server_address)
    sock.connect(server_address)
    try:
        while True:
            message = "A006FF8B010001CE"
            print("Sending %s" % message)
            sock.sendall(bytes.fromhex(message))
            receive_data(sock)
            sleep(1)
    except socket.error as e:
        print("Socket error: %s" % str(e))
    except Exception as e:
        print("Other exception: %s" % str(e))
    finally:
        print("Closing connection to the server")
        sock.close()

client()
