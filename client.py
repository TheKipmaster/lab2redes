import socket
import re
import sys
from threading import Thread
import multiprocessing as mp
from time import sleep


port = 65000
host = '127.0.0.1'

sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sck.connect((host, 65000))

def outbound():
    while True:
        outbound = input('>> ')
        sck.send(bytes(outbound, 'utf-8'))
        sleep(0.2)
    return

def inbound():
    while True:
        inbound = sck.recv(512)
        print('<<', inbound.decode())
    return

def main():
    processes = []

    processes.append(Thread(target=outbound))
    processes.append(Thread(target=inbound))

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    return


if __name__ == '__main__':
    main()
