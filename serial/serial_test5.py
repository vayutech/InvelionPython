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

    start_time = time.time()
    while True:
        # Lendo resposta
        byte = ser.read()
        check_sum = byte
        int_byte = int.from_bytes(byte, byteorder='big')

        if int_byte == 0xA0:
            # cabeçalho encontrado, proximo byte é o tamanho da mensagem
            tamanho = ser.read()
            tamanho_mensagem = int.from_bytes(tamanho, byteorder='big')
            check_sum = check_sum + tamanho
            print("o tamanho da mensagem é", tamanho_mensagem)
            if(tamanho_mensagem == 10):
                print("mensagem de 10 bytes - saida do loop")
                print("mensagem de saida do loop", ser.read(tamanho_mensagem))
                break
            else:
                mensagem = ser.read(tamanho_mensagem)
                check_sum = check_sum + mensagem[:-1]
                checksum = sum(check_sum) % 256
                if checksum == mensagem[-1]:
                    print("checksum correto")
                print(mensagem)
                mensagem_completa = bytearray()
                mensagem_completa.append(int_byte)
                mensagem_completa.append(tamanho_mensagem)
                mensagem_completa.extend(mensagem)

                checksum = 0
                for i in range(len(mensagem_completa) - 1):
                    checksum += mensagem_completa[i]
                    
                checksum &= 0xFF  # garante que o valor do checksum esteja entre 0 e 255

                if checksum == mensagem_completa[-1]:
                    print("O checksum está correto!")
                else:
                    print("O checksum está incorreto!")
                print(mensagem_completa)
    end_time = time.time()
    print("tempo de execução: ", end_time - start_time)
    # Esperando 1 segundo antes do próximo envio
    sleep_time = 1 - (end_time - start_time)
    if sleep_time > 0:
        time.sleep(sleep_time)
    else:
        print("tempo de execução maior que 1 segundo")
        

# Fechando conexão serial
ser.close()
