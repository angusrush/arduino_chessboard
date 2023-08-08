#!/usr/bin/python

import serial
import chess
import chess.pgn
import logging
import argparse
import sys
from datetime import date
from curses import wrapper

# My code is mostly in ./src/*
sys.path.insert(0, "src")

from movebuilder import *
from curses_tui import *
from simple_tui import *
from write_pgn import write_pgn

WHITE = "White"
BLACK = "Black"

def main():
    # Parse arguments

    wrapper(chess_game)
    pass

def chess_game(stdscr):
    stdscr.clear()

    # If we start with the --testing, or -t, flag, we use virtual ports
    # governed by the computer. If we don't, we start listening at the usual
    # port connected to by our arduino.
    parser = argparse.ArgumentParser(
        description="parse arguments for smart chess board"
    )
    parser.add_argument(
        "-t",
        "--testing",
        action="store_true",
        help="Testing mode, handles input differently",
    )
    parser.add_argument(
        "-n",
        "--nocurses",
        action="store_true",
        help="Use simple interface printing to command line instead of ncurses",
    )

    args = parser.parse_args()

    # This records events and legal moves to events.log. Very handy!
    logging.basicConfig(level=logging.DEBUG, filename="events.log")

    # This is set when the game ends, so the rest of the program
    # knows what happened. Hacky, but it works fine.
    gameover_message: str = ""

    if args.nocurses:
        tui = SimpleTui()
    else:
        tui = CursesBoardTui()

    # What exactly we initialize will depend on whether we're using the arduino.
    if args.testing:
        ser = serial.Serial("/dev/pts/4", 9600)
        board = chess.Board()
        mb = MoveBuilder(board, ser, tui)
        tui.print_board(board)

    else:
        ser = serial.Serial("/dev/ttyACM0", 9600)
        starting_fen = "5rk1/5ppp/8/8/8/8/1q3PPP/Q4RK1 w - - 0 1"
        board = chess.Board(fen=starting_fen)
        mb = MoveBuilder(board, ser, tui)
        tui.print_message("Board set with starting configuration")
        tui.print_board(board)
        mb.set_up_pieces()

    tui.print_message("Starting new game.")
    logging.info("Starting new game.")

    while True:
        if board.turn:
            to_move = WHITE
            not_to_move = BLACK
        else:
            to_move = BLACK
            not_to_move = WHITE

        if board.fullmove_number == 1 and to_move == WHITE:
            tui.print_message(f"{to_move} to move.")
        else:
            tui.print_message(f"{not_to_move}'s move complete. {to_move} to move.")

        # Starts listening for a move. This will print out a
        # bunch of intermediate board positions.
        move: chess.Move | None = None
        try:
            move = mb.listen_for_move()
        except KeyboardInterrupt:
            sys.exit(0)
        except ParsingError:
            tui.print_board(board)
            mb.pieces_in_air.queue.clear()
            tui.print_pieces(mb.pieces_in_air)
            tui.print_warning_and_wait(
                "Parsing error! Please place the "
                "board in the\n displayed position, then "
                "press any key."
            )

        if move:
            board.push(move)
        elif move == chess.Move.null():
            tui.print_board(board)
            tui.print_warning_and_wait(
                "The move was illegal! Please place the "
                "board in the\n displayed position, then "
                "press any key."
            )

        game = chess.pgn.Game.from_board(board)
        tui.print_board(board)
        tui.print_pgn(game)

        # Check for various things which would mean that the game was over
        if board.is_checkmate():
            gameover_message = f"Checkmate! {to_move} wins!"
        elif board.is_stalemate():
            gameover_message = "Stalemate!"
        elif board.is_insufficient_material():
            gameover_message = "Nobody has sufficient material to mate. Draw!"
        elif board.is_seventyfive_moves():
            gameover_message = "Game is a draw by the 75 move rule. Astonishing."
        elif board.is_repetition():
            gameover_message = "Draw by fivefold repetition."

        # And if the game is over...
        if gameover_message:
            tui.print_message(gameover_message)

            game = chess.pgn.Game.from_board(board)
            game.headers["Date"] = str(date.today())
            tui.print_board(board)

            player_names = tui.prompt_name()
            game.headers["White"] = player_names[0]
            game.headers["Black"] = player_names[1]
            tui.print_pgn(game)

            tui.print_warning("Press 'q' to exit,\n" "or 'w' to write PGN")

            keypress = tui.prompt_quit()
            if keypress == "q":
                sys.exit(0)
            elif keypress == "w":
                write_pgn(game)
                sys.exit(0)

if __name__ == "__main__":
    main()
