#!/usr/bin/python

import serial
import chess
from movebuilder import *

#ser = serial.Serial('/dev/ttyACM0', 9600)
ser = serial.Serial('/dev/pts/2', 9600)

#square_translations = [0, 1, 8, 9]
square_translations = [0, 1, 2, 3]

starting_fen = "5rk1/5ppp/8/8/8/8/1q3PPP/Q4RK1 w - - 0 1"

board = chess.Board(fen = starting_fen)

print(board)

move_in_progress = False

while board.is_checkmate() == False:
    if board.turn:
        to_move = "White"
    else:
        to_move = "Black"

    print(to_move + " to move.")

    reading_startsquare = ser.readline().decode('utf-8')
    print("Starting move up:" + reading_startsquare)
    reading_endsquare = ser.readline().decode('utf-8')
    print("Starting move down:" + reading_endsquare)

    x = reading_startsquare.split()
    y = reading_endsquare.split()

    fromsquare = BoardEvent(reading_startsquare)

    tosquare = BoardEvent(reading_endsquare)

    move = chess.Move(fromsquare.square, tosquare.square)
    print(move)

    if move in board.legal_moves:
        board.push(move)
        print(board)
        print("-------------")
    else:
        print(board)
        input("Not a legal move! Put the board in the above position, then press enter.")

