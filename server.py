import socket
port = 65000
host = '192.168.0.16'


class Channel:
    def __init__(self, name):
        self.name = name
        self.clients = {}

class Server:

    def __init__(self):
        # Estruturas de clientes e canais
        self.clients = {}
        self.canais   = {}

        self.canais[""] = Channel("")

        # Handlers para comandos
        self.handlers = {"NICK"   : self.nickClientHandler,
                         "USUARIO": self.newClientHandler,
                         "SAIR"   : self.deleteClientHandler,
                         "ENTRAR" : self.subscribeChannelHandler,
                         "SAIRC"  : self.unsubscribeChannelHandler,
                         "LISTAR" : self.listChannelHandler,
                        }
        
        # requisita API do SO uma conexão AF_INET (IPV4) com protocolo de transporte SOCK_STREAM (TCP)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # requisita ao SO a posse de uma porta associada a um IP
        self.sock.bind((host, port))

        # requisita ao SO que a porta indicada de um dado IP seja reservado para escuta
        self.sock.listen(5)

        print("Conexão aberta porta: ", port)

        self.run()

    def run(self):
        open = True

        while open:
            # aceita requisição de conexão
            (clientsock, address) = self.sock.accept()

            while open:
                # recebe do socket do cliente e uma mensagem de 512 bytes
                message = clientsock.recv(512)

                print("Mensagem: ", message.decode())
                print("Endereco: ", address)

                if '/quit' in message.decode():
                    open = False
                    clientsock.send(bytes('Conexão Fechada', 'utf-8'))
                    pass

                #clientsock.send(bytes('Entregue', 'utf-8'))
                #clientsock.send(bytes('Continuando...', 'utf-8'))

                # processa mensagem
                answer = self.parseCommands(clientsock, address, message)
                if len(answer) > 0:
                    self.sendMessage(clientsock, answer)
        self.sock.close()
        pass

    def sendMessage(self, clientsock, answer):
        clientsock.send(bytes(answer, 'utf-8'))

    def parseCommands(self, clientsock, clientAddr, message):
        message = message.decode()

        answer = ''

        if(message[0] == '/'):
            answer += 'Tratar comando: '
            answer += message

        else:
            answer = 'Enviar para o canal: '
            answer += message

        """
        commands = message.split('\n') # comandos separados por nova linha
        unrecognized_commands = []
        invalid_parameters = []


        if clientAddr not in self.clients.keys():
            self.clients[clientAddr] = ServerClient(clientAddr, clientsock)
            self.canais[""].clients[clientAddr] = self.clients[clientAddr]

        client = self.clients[clientAddr]

        for command in commands:
            comm_n_args = command.split(' ')
            if comm_n_args[0][0] is '?':
                if comm_n_args[0][1:] in self.handlers.keys():
                    ans = self.handlers[comm_n_args[0][1:]](clientAddr, comm_n_args[1:])
                    if len(ans) > 0:
                        invalid_parameters += ans
                else:
                    unrecognized_commands += comm_n_args[0]
            else:
                self.sendMsgChannel(comm_n_args[1:], client.channel)

        answer = ""
        if len(unrecognized_commands) > 0:
            answer += "Unrecognized commands: %s" % unrecognized_commands
        if len(invalid_parameters) > 0:
            answer += "Invalid parameters: %s\n" % invalid_parameters
        """
        return answer

    def sendMsgChannel(self, msg, channel):
        for client in self.canais[channel].clients:
            client.sendMsg(msg)

    def nickClientHandler(self, clientAddr, args):
        pass

    def newClientHandler(self, clientAddr, args):
        pass

    def deleteClientHandler(self, clientAddr, args):
        pass

    def subscribeChannelHandler(self, clientAddr, args):
        pass

    def unsubscribeChannelHandler(self, clientAddr, args):
        pass

    def listChannelHandler(self, clientAddr, args):
        pass

def main():
    Sever()

    pass

# Para evitar dar pau com multiprocessos em python,
#   sempre colocar essa guarda, que evita processos filhos
#   de executarem a o conteúdo da função
if __name__ == '__main__':
    Server()