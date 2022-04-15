import time
import json
import socket
from cache import CACHE_HOST, CACHE_PORT, MESSAGE_SIZE_IN_BYTES

def make_connection_to_server(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    time.sleep(1)
    return client

def print_result(temperature_informations):
    is_from_cache = "WAS" if temperature_informations.get("is_from_cache") else "WAS NOT"
    temperature = temperature_informations.get("temperature")
    server = temperature_informations.get("server_name")

    print("Temperature on {} is {} and {} received from cache".format(server, temperature, is_from_cache))

if __name__ == '__main__':
    pass
    client = make_connection_to_server(CACHE_HOST, CACHE_PORT)

    while True:
        client.sendall(b"Get temperature")

        temperatures = client.recv(MESSAGE_SIZE_IN_BYTES)
        temperatures = json.loads(temperatures.decode("utf-8"))

        for temperature in temperatures:
            print_result(temperature)
        print()


