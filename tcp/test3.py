from time import sleep
import socket

def process_message(message):
    # Esta é a função que processa a mensagem recebida do servidor
    message = message.hex()
    print("Received message: %s" % message)

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
        buffer = bytearray()
        while True:
            message = "A006FF8B010001CE"
            print("Sending %s" % message)
            sock.sendall(bytes.fromhex(message))
            data = sock.recv(1024 * 4)
            buffer += data
            # Processa o buffer procurando por cabeçalhos de mensagem completos
            while len(buffer) >= 2 and buffer[0] == 0xA0:
                length = int.from_bytes(buffer[1:3], byteorder='big')
                if len(buffer) >= length:
                    message = buffer[:length]
                    process_message(message)
                    buffer = buffer[length:]
                else:
                    break
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
