import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

game_board = [' '] * 9
turn = 'X'
clients = []

