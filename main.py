import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

square_translations = ["a1", "a2", "b1", "b2"]

class BoardEvent:
    def __init__(self, square, piece_lifted):
        # square is a string, e.g. 'e2'.
        # piece_lifted is a boolean: True means lifted, False means put down.
        self.square = square
        self.is_lift = piece_lifted

modes = ["Waiting", "Move in progress", "Take/Castle in progress", "Castle in progress"]
mode = 0

while True:
    reading = ser.readline().decode('utf-8')
    x = reading.split()

    board_event = BoardEvent(x[0], x[1])

    print(board_event.square)
    print(board_event.is_lift)



