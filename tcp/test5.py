from time import sleep
import socket

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
        buffer = b''
        while True:
            message = "A006FF8B010001CE"
            print("Sending %s" % message)
            sock.sendall(bytes.fromhex(message))
            
            # Read response
            data = sock.recv(1024)
            buffer += data
            
            # Check if we have a complete message
            while len(buffer) >= 20:
                if buffer[0] == 0xA0:
                    msg_len = int.from_bytes(buffer[1:3], byteorder='big')
                    if len(buffer) >= msg_len + 3:
                        msg = buffer[:msg_len+3]
                        buffer = buffer[msg_len+3:]
                        process_message(msg)
                    else:
                        break
                else:
                    buffer = buffer[1:]
            
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

def process_message(msg):
    data = msg.hex()
    print("Received message: %s" % data)

client()
