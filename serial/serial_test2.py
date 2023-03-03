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

while True:
    # Enviando comando
    comando = bytes.fromhex("A0 06 FF 8B 01 00 01 CE")
    ser.write(comando)

    # Lendo resposta
    resposta = ser.read()
    print(resposta)

    # Esperando 1 segundo antes do próximo envio
    time.sleep(1)

# Fechando conexão serial
ser.close()
