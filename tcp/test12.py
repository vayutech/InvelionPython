import socket
import select

def process_byte(byte):
    hex_byte = byte.hex()
    if(hex_byte == "a0"):
        print("Found header")
    else:   
        print("Found byte: %s" % hex_byte)

def receive_data(sock):
    while True:
        ready, _, _ = select.select([sock], [], [], 1)
        if ready:
            byte = sock.recv(1)
            if not byte:
                # Connection closed by the server
                break
            process_byte(byte)

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
    except socket.error as e:
        print("Socket error: %s" % str(e))
    except Exception as e:
        print("Other exception: %s" % str(e))
    finally:
        print("Closing connection to the server")
        sock.close()

client()
