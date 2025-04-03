import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

game_board = [' '] * 9
turn = 'X'
clients = []


def print_board():
    print(f"{game_board[0]} | {game_board[1]} | {game_board[2]}")
    print("- + - + -")
    print(f"{game_board[3]} | {game_board[4]} | {game_board[5]}")
    print("- + - + -")
    print(f"{game_board[6]} | {game_board[7]} | {game_board[8]}")


def check_winner():
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for a, b, c in win_conditions:
        if game_board[a] == game_board[b] == game_board[c] and game_board[a] != ' ':
            return game_board[a]
    if ' ' not in game_board:
        return 'T'
    return None


def handle_client(conn, player):
    global turn
    control = 0
    conn.sendall(f"Benvenuto! Sei il giocatore {player}\n".encode())
    while True:
        if turn == player:
            control = 0
            conn.sendall("TOCCA A TE. Inserisci una posizione (0-8): ".encode())
            data = conn.recv(1024).decode().strip()
            if not data.isdigit() or int(data) not in range(9) or game_board[int(data)] != ' ':
                conn.sendall("Mossa non valida. Riprova.\n".encode())
                continue
            game_board[int(data)] = player
            print_board()
            winner = check_winner()
            if winner:
                msg = "Pareggio!\n" if winner == 'T' else f"Giocatore {winner} ha vinto!\n"
                for c in clients:
                    c.sendall(msg.encode())
                break
            turn = 'O' if turn == 'X' else 'X'
        else:
            if control == 0:
                conn.sendall("Aspetta il tuo turno...\n".encode())
                control = 1


def start_server():
    global clients
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)
    print("Server in attesa di giocatori...")

    while len(clients) < 2:
        conn, addr = server.accept()
        player = 'X' if len(clients) == 0 else 'O'
        clients.append(conn)
        threading.Thread(target=handle_client, args=(conn, player)).start()

    print("Partita iniziata!")
    for c in clients:
        c.sendall("La partita è iniziata!\n".encode())


if __name__ == "__main__":
    start_server()
