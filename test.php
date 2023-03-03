<?php

$host = '192.168.0.178'; // Endereço IP do servidor
$port = 4001; // Porta do servidor

// Valor hexadecimal a ser enviado
$value = "A006FF8B010001CE";

// Converter o valor hexadecimal em uma string binária
$data = hex2bin($value);

$socket = stream_socket_client("tcp://$host:$port", $errno, $errstr, 30);

if (!$socket) {
    echo "$errstr ($errno)<br />\n";
} else {
    while(true) {
        fwrite($socket, $data);
        $response = fgets($socket, 8192);

        // Converter a resposta em uma string hexadecimal
        $hex_response = bin2hex($response);

        echo "Resposta do servidor: $hex_response\n";
        fclose($socket);
    }
}
