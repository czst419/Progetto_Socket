import socket

HOST = '127.0.0.1'
PORT = 12345


def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    while True:
        data = client.recv(1024).decode()
        if "TOCCA A TE" in data:
            move = input(data)
            client.sendall(move.encode())
        else:
            print(data)
        if "ha vinto" in data or "Pareggio" in data:
            break
    client.close()


if __name__ == "__main__":
    start_client()

