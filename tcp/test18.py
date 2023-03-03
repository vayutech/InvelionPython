import time
import socket
import threading

def on_message_received(message):
    print(f"New message received: {message}")

def receive_data(sock):
    buffer = b''
    while True:
        byte = sock.recv(1)
        if not byte:
            break
        if byte == b'\xa0':
            message = buffer.hex()
            threading.Thread(target=on_message_received, args=(message,)).start()
            buffer = b''
        buffer += byte

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
            receive_data(sock)
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