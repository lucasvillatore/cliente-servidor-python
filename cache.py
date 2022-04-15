import time
import json
import socket

from datetime import datetime, timedelta
from servidor1 import HOST as HOST_1, PORT as PORT_1
from servidor2 import HOST as HOST_2, PORT as PORT_2
from servidor3 import HOST as HOST_3, PORT as PORT_3
from utils import create_connection

MESSAGE_SIZE_IN_BYTES = 1024
CACHE_TABLE = []
CACHE_DURATION_IN_SECONDS = 30
CACHE_HOST = 'localhost'
CACHE_PORT = 8000


def make_connection_to_server(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    time.sleep(1)
    return client

def make_server_row(temperature, timestamp, server_name, connection):
    row = {
        "temperature": temperature,
        "timestamp": timestamp,
        "server_name": server_name,
        "initialized": False,
        "connection": connection
    }

    return row

def init_cache_table(servers):
    print("Initializing cache table")
    time.sleep(1)
    cache_table = []
    for i in range (0, 3):
        row = make_server_row(
            0, 
            datetime.now(), 
            "server {}".format(i + 1),
            servers[i]
        )
        cache_table.append(row)
    
    return cache_table

def already_expired_cache_server_row(row):
    current_time = datetime.now()
    cache_time = row.get("timestamp")

    if not row.get("initialized") or current_time > cache_time + timedelta(seconds=CACHE_DURATION_IN_SECONDS):
        return True

    return False

def request_temperature_from_server(server_row):

    server_row.get("connection").sendall(b"Get temperature")
    
    temperature = server_row.get("connection").recv(MESSAGE_SIZE_IN_BYTES)
    temperature = temperature.decode("utf-8")
    
    timestamp = datetime.now()
    return {
        "temperature": temperature,
        "timestamp": timestamp,
        "server_name": server_row["server_name"],
        "initialized": True,
        "connection": server_row.get("connection")
    }

def update_cache_table(new_row):
    global CACHE_TABLE
    new_cache_table = []

    for row in CACHE_TABLE:
        if row.get("server_name") == new_row.get("server_name"):
            new_cache_table.append(new_row)
        else:
            new_cache_table.append(row)

    CACHE_TABLE = new_cache_table

def print_result(temperature_informations):
    is_from_cache = "WAS" if temperature_informations.get("is_from_cache") else "WAS NOT"
    temperature = temperature_informations.get("temperature")
    server = temperature_informations.get("server_name")

    print("Temperature on {} is {} and {} received from cache".format(server, temperature, is_from_cache))

if __name__ == "__main__":
    servers = []
    print("Establishing connection with server 1")
    servers.append(make_connection_to_server(HOST_1, PORT_1))
    print("Establishing connection with server 2")
    servers.append(make_connection_to_server(HOST_2, PORT_2))
    print("Establishing connection with server 3")
    servers.append(make_connection_to_server(HOST_3, PORT_3))

    CACHE_TABLE = init_cache_table(servers)

    connection, address = create_connection(CACHE_HOST, CACHE_PORT)

    print("Connected by {}".format(address))
    while(True):
        data = connection.recv(MESSAGE_SIZE_IN_BYTES)
        temperature_from_servers = []
        for cache_row in CACHE_TABLE:
            is_from_cache = True
            if already_expired_cache_server_row(cache_row):
                is_from_cache = False
                print("Cache from {} is expired, requesting a new temperature".format(cache_row.get("server_name")))
                cache_row = request_temperature_from_server(cache_row)
                print("Updating row {} from cache table".format(cache_row.get("server_name")))
                update_cache_table(cache_row)
            else:
                print("Cache from {} stil valid, getting temperature from cache".format(cache_row.get("server_name")))
            print()

            temperature_from_servers.append({
                "temperature": cache_row.get("temperature"),
                "is_from_cache": is_from_cache,
                "server_name": cache_row.get("server_name")
            })
        connection.sendall(str(json.dumps(temperature_from_servers)).encode("utf-8"))

        time.sleep(5)

        

