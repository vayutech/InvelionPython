import socket

# Define o endereço IP e a porta do servidor
host = '192.168.0.178'
port = 4001

# Cria o objeto socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Define um tempo limite para a conexão
    s.settimeout(10)

    # Conecta-se ao servidor
    print(f"Conectando a {host}:{port}")
    s.connect((host, port))
    
    # Envia a mensagem em hexadecimal
    message_hex = 'A006FF8B010001CE'
    message_bytes = bytes.fromhex(message_hex)
    s.send(message_bytes)

    # Recebe a resposta do servidor byte a byte
    data = b''
    while True:
        byte = s.recv(1)
        if not byte:
            break
        data += byte

    # Verifica se a resposta é vazia
    if not data:
        raise Exception("Resposta vazia do servidor")

    # Exibe a resposta do servidor
    print(f"Resposta do servidor: {data}")

except Exception as e:
    print(f"Erro ao conectar ao servidor: {e}")

finally:
    # Fecha a conexão
    s.close()
