from signal import signal, SIGINT
from sys import exit
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket successfully created")

port = 1337

s.bind(('', port))
print("Socket bound to %s" % (port))

s.listen(5)
print("Socket is listening")

def handler(signal_recieved, frame):
  print('\nQuitting 1337 c2...')
  s.close()
  exit(0)

def main():
  while True:
    c, addr = s.accept()
    print("Beacon connected from:", addr)

    print("Got data from beacon: " + bytes.decode(c.recv(1024)))

    strToSend = input("Command to send: ")
    binCommand = strToSend.ljust(1024, '\0').encode("utf-8")
    print("Len of binCommand: " + str(len(binCommand)))
    c.send(binCommand, len(binCommand))
    
    c.close()

if __name__ == "__main__":
  signal(SIGINT, handler)
  main()