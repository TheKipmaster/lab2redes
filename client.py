import socket
import re
import sys
from threading import Thread
import multiprocessing as mp
from time import sleep

port = 65000
host = '192.168.0.16'

class Client:
    numClients = 0

    def __init__(self, ipv4, sock, nickname="USR"+str(numClients), hostname="", channel=""):
        self.ipv4     = ipv4
        self.sock     = sock
        self.nickname = nickname
        self.hostname = hostname
        self.channel  = channel

        Client.numClients += 1

    def sendMsg(self, msg):
        self.sock.send(bytes(msg, "utf-8"))

sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sck.connect((host, 65000))

# Le mensagem do usuario
def outbound():
    open = True

    while open:
        try:
            outbound = input('>> ')
            sck.send(bytes(outbound, 'utf-8'))
            sleep(0.2)
        except:
            print('Não pode completar a ação') 
            open = False   
    return

# Imprime mensagens para o usuario
def inbound():  
    open = True

    while open:
        try:
            inbound = sck.recv(512)
            if(len(inbound) > 0):
                print('<<', inbound.decode())
        except:
            print('Não pode completar a ação')
            open = False
    return

def main():
    processes = []

    # Cria os processos
    processes.append(Thread(target=outbound))
    processes.append(Thread(target=inbound))

    #Inicia os processos
    for process in processes:
        process.start()

    for process in processes:
        process.join()

    return


if __name__ == '__main__':
    main()

