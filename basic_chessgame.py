#!/usr/bin/python

import serial
import chess


class BoardEvent:
    def __init__(self, square, piece_lifted):
        # square is a string, e.g. 'e2'.
        # piece_lifted is a boolean: True means lifted, False means put down.
        self.square = square
        self.is_lift = piece_lifted


ser = serial.Serial('/dev/ttyACM0', 9600)

square_translations = ["a1", "a2", "b1", "b2"]

starting_fen = "5rk1/5ppp/8/8/8/8/1q3PPP/Q4RK1 w - - 0 1"

board = chess.Board(fen = starting_fen)

print(board)

move_in_progress = False

while board.is_checkmate() == False:
    # if board.turn:
    #     to_move = "White"
    # else:
    #     to_move = "Black"

        # print(to_move + " to move.")

    reading_startsquare = ser.readline().decode('utf-8')
    print("Starting move up:" + reading_startsquare)
    reading_endsquare = ser.readline().decode('utf-8')
    print("Starting move down:" + reading_endsquare)

    x = reading_startsquare.split()
    y = reading_endsquare.split()

    try:
        fromsquare = BoardEvent(chess.parse_square(square_translations[int(x[0])]), x[1])
    except ValueError:
        print("Not a valid fromsquare!")

    try:
        tosquare = BoardEvent(chess.parse_square(square_translations[int(y[0])]), y[1])
    except ValueError:
        print("Not a valid tosquare!")
    
    move = chess.Move(fromsquare.square, tosquare.square)
    print(move)

    if move in board.legal_moves:
        board.push(move)
        print(board)
        print("-------------")
    else:
        print("Not a legal move! Try again.")

