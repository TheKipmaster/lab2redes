import socket
import urllib.request
from channel import Channel

port = 65000
#host = '192.168.0.16'
host = '172.29.37.38'

class Server:

    def __init__(self):
        # Estruturas de clientes e canais
        self.clients = {}
        self.canais   = {}

        self.canais[""] = Channel("")

        # Handlers para comandos
        self.handlers = {"NICK"   : self.nickClientHandler,
                         "USUARIO": self.userClientHandler,
                         "SAIR"   : self.quitClientHandler,
                         "ENTRAR" : self.subscribeChannelHandler,
                         "SAIRC"  : self.quitChannelHandler,
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

                if '/SAIR' in message.decode():
                    open = False
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
            message = message [1:] 
            #answer += 'Tratar comando: '
            #answer += message
            answer = self.commands(clientsock, clientAddr, message)

        else:
            answer = 'Enviar para o canal: '
            answer += message

        return answer

    def commands(self, clientsock, clientAddr, message):
        from client import Client

        answer = ''

        if clientAddr not in self.clients.keys():
            self.clients[clientAddr] = Client(clientAddr, clientsock)
            self.canais[""].clients[clientAddr] = self.clients[clientAddr]

        if message in self.handlers.keys():
            #Verificar canal

        else:
            answer += 'Comando inválido, tente:'
            answer += '\n/NICK'
            answer += '\n/USUARIO'
            answer += '\n/SAIR'
            answer += '\n/ENTRAR'
            answer += '\n/SAIRC'
            answer += '\n/LISTAR'


        """
        commands = message.split('\n') # comandos separados por nova linha
        unrecognized_commands = []
        invalid_parameters = []


        if clientAddr not in self.clients.keys():
            self.clients[clientAddr] = Client(clientAddr, clientsock)
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

    #Enviar mensagem para o canal
    def sendMsgChannel(self, msg, channel):
        for client in self.canais[channel].clients:
            client.sendMsg(msg)
        print('Enviar mensagem para o canal')

    # Criar apelido ou mudar anterior
    def nickClientHandler(self, clientAddr, args):
        print('Criar apelido')
        pass

   # Especificar nome do usuario
    def userClientHandler(self, clientAddr, args):
        print('Nome usr')
        pass

    # Sair do canal
    def quitClientHandler(self, clientAddr, args):
        print('Sair do servidor')
        pass

    # Entrar no canal
    def subscribeChannelHandler(self, clientAddr, args):
        print('Entrar no canal')
        pass

    # Sair do canal
    def quitChannelHandler(self, clientAddr, args):
        print('Sair do canal')
        pass

    # Listar canais
    def listChannelHandler(self, clientAddr, args):
        print('Listar os canais')
        pass

def main():
    Sever()

    pass

# Para evitar dar pau com multiprocessos em python,
#   sempre colocar essa guarda, que evita processos filhos
#   de executarem a o conteúdo da função
if __name__ == '__main__':
    Server()