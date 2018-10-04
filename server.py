import socket
port = 65000
host = '127.0.0.1'

# requisita API do SO uma conexao AF_INET (IPV4)
#   com protocolo de transporte SOCK_STREAM (TCP)
sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# requisita ao SO a posse de uma porta associada a um IP
sck.bind((host, port))

# requisita ao SO que a porta indicada de um dado IP seja
#   reservado para escuta
sck.listen(5)

# loop principal.
print(sck.getsockname())
open = True
while open:
    (clientsocket, address) = sck.accept()
    print((clientsocket, address))

    while open:
        message = clientsocket.recv(512)
        clientsocket.send(bytes('Entregue', 'utf-8'))
        clientsocket.send(bytes('Continuando...', 'utf-8'))
        # sck.send(bytes('continuando...'))

        print("Mensagem: ", message.decode())
        print("Endereco: ", address)

        if '/quit' in message.decode():
            open = False
sck.close()
