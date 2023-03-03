import serial
import time

# Configuração da porta serial
porta = "COM6"  # altere para a porta serial apropriada
baud_rate = 115200
bytesize = serial.EIGHTBITS
parity = serial.PARITY_NONE
stopbits = serial.STOPBITS_ONE

# Abrindo a conexão serial
ser = serial.Serial(porta, baud_rate, bytesize, parity, stopbits)

# Buffer de dados para armazenar bytes recebidos
buffer = bytearray()

while True:
    # Enviando comando
    comando = bytes.fromhex("A0 06 FF 8B 01 00 01 CE")
    ser.write(comando)

    # Lendo resposta
    while True:
        # Lendo um byte da porta serial
        byte = ser.read()

        # Convertendo o byte para int e adicionando ao buffer
        buffer.append(int.from_bytes(byte, byteorder='big'))

        # Verificando se o buffer contém o cabeçalho 0xA0
        if buffer[:1] == b"\xA0":
            # Extraindo a mensagem do buffer
            mensagem = buffer[1:]

            # Processando a mensagem
            # ...
            print(mensagem)

            # Limpando o buffer
            buffer = bytearray()
            break

    # Esperando 1 segundo antes do próximo envio
    time.sleep(1)

# Fechando conexão serial
ser.close()
