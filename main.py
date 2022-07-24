#!/usr/bin/python

import serial
import chess
import chess.pgn
import logging
from movebuilder import *

def main():
    logging.basicConfig(filename='example.log', level=logging.DEBUG)
    
    #ser = serial.Serial('/dev/ttyACM0', 9600)
    ser = serial.Serial('/dev/pts/2', 9600)
    
    #starting_fen = "5rk1/5ppp/8/8/8/8/1q3PPP/Q4RK1 w - - 0 1"
    #board = chess.Board(fen = starting_fen)
    board = chess.Board()
    
    mb = MoveBuilder(board, ser)
    
    logging.info("Starting new game.")
    
    while True:
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
            print(f"{to_move}'s move complete.")
            #print(board)
    
        if board.is_checkmate() == True:
            print(f"Checkmate! {to_move} wins!")
            print_game = input("Press y to print the game, anything else to exit")
            if print_game == 'y':
                game = chess.pgn.Game.from_board(board)
                print(game)
            break
    
if __name__ == '__main__':
    main()
