from datetime import datetime


def filename(pgn):
    now = datetime.now()
    datestring = now.strftime("%y.%m.%d_%H:%M")

    white_name = pgn.headers["White"]
    black_name = pgn.headers["Black"]
    game_result = pgn.headers["Result"]

    if game_result == "1/2-1/2":
        game_result = "Draw"

    string_blocks = [datestring, white_name, game_result, black_name]

    return "_".join(string_blocks) + ".pgn"


def write_pgn(pgn):
    name = filename(pgn)
    folder = "./past_games/"
    f = open(folder + name, "a")
    f.write(str(pgn))
    f.close()
