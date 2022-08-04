#!/usr/bin/python

import serial
import chess
import chess.pgn
import logging
import argparse
import sys
from movebuilder import *
import curses
from curses import wrapper

def main(stdscr):
    stdscr.clear()

    # If we start with the --testing, or -t, flag, we use virtual ports
    # governed by the computer. If we don't, we start listening at the usual
    # port connected to by our arduino.
    parser = argparse.ArgumentParser(description='parse arguments'
                                     + 'for smart chess board')
    parser.add_argument('-t',
                        '--testing',
                        action='store_true',
                        help='Testing mode, handles input differently')

    args = parser.parse_args()

    # This records events and legal moves to events.log. Very handy!
    logging.basicConfig(level=logging.DEBUG, filename='events.log')

    gameover_message = ""

    boardwin = curses.newwin(8, 16, 0, 0)
    messagewin = curses.newwin(1, 80, 9, 0)
    warningwin = curses.newwin(2, 60, 3, 20)
    gameprintwin = curses.newwin(15, 80, 11, 0)

    # What exactly we initialize will depend on whether we're using the arduino.
    if args.testing:
        ser = serial.Serial('/dev/pts/2', 9600)
        board = chess.Board()
        mb = MoveBuilder(board, ser, boardwin, messagewin, warningwin)
        boardwin.addstr(str(board))
        boardwin.refresh()

    else:
        ser = serial.Serial('/dev/ttyACM0', 9600)
        starting_fen = "5rk1/5ppp/8/8/8/8/1q3PPP/Q4RK1 w - - 0 1"
        board = chess.Board(fen = starting_fen)
        mb = MoveBuilder(board, ser, boardwin, messagewin, warningwin)
        messagewin.addstr("Board set with starting configuration")
        messagewin.refresh()
        boardwin.addstr(str(board))
        boardwin.refresh()
        mb.set_up_pieces()

    messagewin.clear()
    messagewin.addstr("Starting new game.")
    messagewin.refresh()
    logging.info("Starting new game.")

    while True:
        if board.turn:
            to_move = "White"
            not_to_move = "Black"
        else:
            to_move = "Black"
            not_to_move = "White"

        if board.fullmove_number == 1 and to_move == "White":
            messagewin.clear()
            messagewin.addstr(f"{to_move} to move.")
            messagewin.refresh()
        else:
            messagewin.clear()
            messagewin.addstr(f"{not_to_move}'s move complete. {to_move} to move.")
            messagewin.refresh()

        # Starts listening for a move. This will print out a bunch of board positions.
        move = mb.listen_for_move()

        if not move:
            warningwin.clear()
            warningwin.addstr("The move was illegal! Please place the board in the\n"
                              "displayed position, then press any key.")
            warningwin.refresh()
            boardwin.addstr(0, 0, str(board))
            input("")
        else:
            board.push(move)

        if board.is_checkmate():
            gameover_message = f"Checkmate! {to_move} wins!"
        elif board.is_stalemate():
            gameover_message = "Stalemate!"
        elif board.is_insufficient_material():
            gameover_message = "Nobody has sufficient material to mate. Draw!"
        elif board.is_seventyfive_moves():
            gameover_message = "Game is a draw by the 75 move rule. Astonishing."
        elif board.is_repetition():
            gameover_message = "This is a fivefold repetition, leading to a draw."

        if gameover_message:
            messagewin.clear()
            messagewin.addstr(gameover_message)
            messagewin.refresh()

            game = chess.pgn.Game.from_board(board)
            gameprintwin.addstr(str(game))
            gameprintwin.refresh()
            input("")
            sys.exit(0)

if __name__ == '__main__':
    wrapper(main)
