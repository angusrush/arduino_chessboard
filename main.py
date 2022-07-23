#!/usr/bin/python

import serial
import chess
import logging
from movebuilder import *

logging.basicConfig(filename='example.log', level=logging.DEBUG)

#ser = serial.Serial('/dev/ttyACM0', 9600)
ser = serial.Serial('/dev/pts/2', 9600)

#starting_fen = "5rk1/5ppp/8/8/8/8/1q3PPP/Q4RK1 w - - 0 1"

#board = chess.Board(fen = starting_fen)
board = chess.Board()

move_in_progress = False

mb = MoveBuilder(board, ser)

while board.is_checkmate() == False:
    if board.turn:
        to_move = "White"
    else:
        to_move = "Black"

    print(to_move + " to move.")

    move = mb.listen_for_move()
    if move == chess.Move.null():
        print("The move was illegal! Please place the board in the position")
        print(board)
        input("then press any key:")
    else:
        board.push(move)
        print(to_move + " made a move! The board is now in the position:")
        print(board)

