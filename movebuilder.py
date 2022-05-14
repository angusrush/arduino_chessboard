import chess

class MoveBuilder:
    def __init__(self, board):
        self.curent_position = board

    def listen():
        while True:
            raw_event = ser.readline().decode('utf-8').split()
            event = BoardEvent(raw_event[0]

            reading_endsquare = ser.readline().decode('utf-8')
            print("Starting move down:" + reading_endsquare)

            x = reading_startsquare.split()
            y = reading_endsquare.split()

            fromsquare = BoardEvent(int(x[0]), x[1])

            tosquare = BoardEvent(int(y[0]), y[1])
