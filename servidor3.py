import time
from random import randrange
from utils import create_connection

MESSAGE_SIZE_IN_BYTES = 1024
HOST = "localhost"
PORT = 8003

def get_temperature():
    print("Checking temperature on server 3")
    time.sleep(randrange(5))
    return randrange(30) - 80

if __name__ == "__main__":
    connection, address = create_connection(HOST, PORT)

    print("Connected by {}".format(address))
    while True:
        data = connection.recv(MESSAGE_SIZE_IN_BYTES)
        temperature = get_temperature()
        print("Temperature on server 3 is {}".format(temperature))
        connection.sendall(str(temperature).encode("utf-8"))
