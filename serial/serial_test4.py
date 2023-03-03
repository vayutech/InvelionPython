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

    # Verificando se a resposta não está vazia
    if resposta:

        # Verificando se o pacote começa com o cabeçalho correto (0xA0)
        if resposta[0] == 0xA0:

            # Obtendo o tamanho do pacote
            tamanho = resposta[1]

            # Verificando se o pacote está completo
            if ser.in_waiting >= tamanho + 3:

                # Lendo o restante do pacote
                pacote = resposta + ser.read(tamanho + 2)

                # Verificando o checksum
                checksum = sum(pacote[:-1]) % 256
                if checksum == pacote[-1]:

                    # Extraindo os dados
                    endereco = pacote[2]
                    dados = pacote[3:-1]

                    # Processando os dados aqui
                    print("Endereço:", endereco)
                    print("Dados:", dados)

    # Esperando 1 segundo antes do próximo envio
    time.sleep(1)

# Fechando conexão serial
ser.close()
