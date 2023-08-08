import chess
import chess.pgn
import queue


class SimpleTui:
    def __init__(self) -> None:
        pass

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):
        pass

    def print_board(self, board: chess.Board) -> None:
        print(board)
        print("")

    def print_message(self, message: str) -> None:
        print(message)
        print("")

    def print_warning(self, warning: str) -> None:
        print(warning)
        print("")

    def print_warning_and_wait(self, warning: str) -> None:
        print(warning)
        input("")

    def print_pgn(self, pgn: chess.pgn.Game) -> None:
        print(str(pgn))
        print("")

    def print_pieces(self, pieces: queue.Queue[chess.Piece]) -> None:
        piece_list = list(map(lambda x: x.symbol(), list(pieces.queue)))
        string = "Pieces in air:\n" + ", ".join(piece_list)
        print(string)
        print("")

    def prompt_name(self) -> list[str]:
        white_player = input("White player:")
        black_player = input("Black player:")

        return [white_player, black_player]

    def prompt_quit(self) -> str:
        keypress = input("Print 'q' to quit or 'w' to write pgn");
        return keypress

