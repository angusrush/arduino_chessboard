#!/usr/bin/python

import serial
import chess
import chess.pgn
import logging
import argparse
from movebuilder import *

def main():
    parser = argparse.ArgumentParser(description='parse arguments' 
                                     + 'for smart chess board')
    parser.add_argument('-t', 
                        '--testing', 
                        action='store_true', 
                        help='Testing mode, handles input differently')
    args = parser.parse_args()


    if args.testing:
        ser = serial.Serial('/dev/pts/2', 9600)
        board = chess.Board()
        mb = MoveBuilder(board, ser)
        print("Board set with following configuration.")
        print(board)
    else:
        ser = serial.Serial('/dev/ttyACM0', 9600)
        starting_fen = "5rk1/5ppp/8/8/8/8/1q3PPP/Q4RK1 w - - 0 1"
        board = chess.Board(fen = starting_fen)
        mb = MoveBuilder(board, ser)
        print("Set pieces up in the following way, then press B.")
        print(board)
        mb.set_up_pieces()

    logging.basicConfig(level=logging.DEBUG, filename='events.log')
    
    print("Starting new game.")
    logging.info("Starting new game.")

    while True:
        if board.turn:
            to_move = "White"
            not_to_move = "Black"
        else:
            to_move = "Black"
            not_to_move = "White"

        if board.fullmove_number == 1 and to_move == "White":
            print(f"{to_move} to move.")
        else:
            print(f"{not_to_move}'s move complete. {to_move} to move.")
            
        move = mb.listen_for_move()

        if move == chess.Move.null():
            print("The move was illegal! Please place the board in the position")
            print(board)
            input("then press any key:")
        else:
            board.push(move)

        if board.is_checkmate() == True:
            print(f"Checkmate! {to_move} wins!")
            print_game = input("Press y to print the game, anything else to exit")
            if print_game == 'y':
                game = chess.pgn.Game.from_board(board)
                print(game)
            break

if __name__ == '__main__':
    main()
