import socket
port = 65000

# requisita API do SO uma conexao AF_INET (IPV4)
#   com protocolo de transporte SOCK_STREAM (TCP)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# requisita ao SO a posse de uma porta associada a um IP
sock.bind((socket.gethostname(), port))

# requisita ao SO que a porta indicada de um dado IP seja
#   reservado para escuta
sock.listen(5)

while 1:
    # aceita requisicao de conexao do processo 1,
    #   e recebe um socket para o cliente e o
    #   endereco de IP dele
    (clientsocket, address) = sock.accept()

    while 1:
        # recebe do socket do cliente (processo 1) uma mensagem de 10 bytes
        mensagem_recebida = clientsocket.recv(512)

        print("Servidor:", mensagem_recebida)
        print("Socket:", clientsocket)
