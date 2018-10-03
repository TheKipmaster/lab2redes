import socket
import re
import multiprocessing as mp

port = 65000
host = '172.29.19.222'

sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sck.connect((host, 65000))

def outbound():
    while True:
        outbound = raw_input(">>")
        sck.send(bytes(outbound))

    return

def inbound():
    while True:
        inbound = sck.recv(512)
        print(inbound)

    return

def main():
    processes = []

    processes += [mp.Process(target=outbound)]
    processes += [mp.Process(target=inbound)]


    for process in processes:
        process.start()

    for process in processes:
        process.join()

    return


if __name__ == '__main__':
    main()
