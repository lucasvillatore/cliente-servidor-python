import socket

def create_connection(host, port):
    print("Creating server")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print("Cache server is listening on port {}".format(port))
    return server.accept()

if __name__ == '__main__':
    pass