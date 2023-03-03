import serial

# Configura a porta serial
ser = serial.Serial('COM6', 115200, timeout=1)

ser.write(bytes.fromhex("A0 06 FF 8B 01 00 01 CE"))

# Lê os dados da porta serial até encontrar o caractere de final de linha LF
data = ser.readline()

# Converte os dados para string e remove os caracteres de fim de linha
data = data.decode('utf-8').rstrip()

# Imprime os dados lidos
print(data)

# Fecha a porta serial
ser.close()