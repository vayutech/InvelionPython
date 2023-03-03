from time import sleep
import socket
def client(host = '192.168.0.178', port=4001): 
    # Create a TCP/IP socket 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # Connect the socket to the server 
    server_address = (host, port) 
    print ("Connecting to %s port %s" % server_address) 
    sock.connect(server_address) 
    # Send data 
    try:
        num = 0
        while True:
            message = "A006FF8B010001CE" 
            print ("Sending %s" % message) 
            sock.sendall(bytes.fromhex(message)) 
            data = sock.recv(1024 * 4)
            data = data.hex() 
            print ("Received: %s" % data) 
            num += 1
            print("num: %d" % num)
            sleep(1)

    except socket.error as e: 
        print ("Socket error: %s" %str(e)) 
    except Exception as e: 
        print ("Other exception: %s" %str(e)) 
    finally: 
        print ("Closing connection to the server") 
        sock.close() 

client()