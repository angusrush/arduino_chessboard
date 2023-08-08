import curses
import chess
import chess.pgn
import queue
from curses.textpad import Textbox


class CursesBoardTui:
    def __init__(self) -> None:
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        # print(board) is a 2d array of length 16x8
        self.boardwin = curses.newwin(8, 16, 0, 0)
        # messagewin should be a full-length
        self.messagewin = curses.newwin(1, 80, 9, 0)
        self.warningwin = curses.newwin(2, 60, 3, 20)
        self.gameprintwin = curses.newwin(15, 80, 11, 0)
        self.pieceswin = curses.newwin(2, 30, 0, 20)

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def print_board(self, board: chess.Board) -> None:
        self.boardwin.clear()
        self.boardwin.addstr(str(board))
        self.boardwin.refresh()

    def print_message(self, message: str) -> None:
        self.messagewin.clear()
        self.messagewin.addstr(message)
        self.messagewin.refresh()

    def print_warning(self, warning: str) -> None:
        self.warningwin.clear()
        self.warningwin.addstr(warning)
        self.warningwin.refresh()

    def print_warning_and_wait(self, warning: str) -> None:
        self.warningwin.clear()
        self.warningwin.addstr(warning)
        self.warningwin.refresh()
        self.warningwin.getkey()
        self.warningwin.clear()
        self.warningwin.refresh()

    def print_pgn(self, pgn: chess.pgn.Game) -> None:
        self.gameprintwin.clear()
        self.gameprintwin.addstr(str(pgn))
        self.gameprintwin.refresh()

    def print_pieces(self, pieces: queue.Queue[chess.Piece]) -> None:
        piece_list = list(map(lambda x: x.symbol(), list(pieces.queue)))
        string = "Pieces in air:\n" + ", ".join(piece_list)
        self.pieceswin.clear()
        self.pieceswin.addstr(string)
        self.pieceswin.refresh()

    def prompt_name(self) -> list[str]:
        namewin_white = curses.newwin(1, 30, 15, 8)
        namebox_white = Textbox(namewin_white)
        namebox_white.edit()
        namewin_black = curses.newwin(1, 30, 16, 8)
        namebox_black = Textbox(namewin_black)
        namebox_black.edit()
        white_player = namebox_white.gather().strip()
        black_player = namebox_black.gather().strip()

        return [white_player, black_player]

    def prompt_quit(self) -> str:
        keypress = self.messagewin.getkey()
        return keypress
