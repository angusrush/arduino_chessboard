import chess
import queue

# Encodes a board event, e.g. "5 up" as:
# self.square = 5
# self.is_lift = True
# Encodes a button press "B pressed" as:
# self.square = -1
# self.is_lift = False
class BoardEvent:
    def __init__(self, event_string):
        # square is a number between 0 and 63
        # is_lift is a boolean: True means lifted, False means put down.
        raw_event = event_string.split()
        if raw_event[0] == 'B':
            self.square = -1
            self.is_lift = False
        else:
            self.square = int(raw_event[0])
            if raw_event[1] == "up":
                self.is_lift = True
            elif raw_event[1] == "down":
                self.is_lift = False
            else:
                print("Parsing error")

    def __str__(self):
        return "square = " + str(self.square) + "; is_lift = " + str(self.is_lift)

# Takes two boards as inputs, returns a list of tuples of the form
# (Square square, Piece old_piece, Piece new_piece)
# One tuple per changed
def compute_deltas(old_board, new_board):
    deltas = []
    for square in chess.SQUARES:
        oldpiece = old_board.piece_at(square)
        newpiece = new_board.piece_at(square)
        if oldpiece != newpiece:
            deltas.append((square, oldpiece, newpiece))

    return deltas

#def interpret_deltas(deltas):
#    if len(deltas) == 2: # Either a normal move or a take
#        for i in deltas:
#            if i[2] == 



class MoveBuilder:
    def __init__(self, board, serial_connection):
        # We want a copy of the board position, not the actual board position!
        self.start_position = chess.Board()
        self.start_position.set_piece_map(board.piece_map())
        # We want a copy of the board position, not the actual board position!
        self.current_position = chess.Board()
        self.current_position.set_piece_map(board.piece_map())
        self.pieces_in_air = queue.Queue()
        self.ser = serial_connection

    def listen_for_move(self): # Returns a Move (Not necessarily legal, but at least well-formed)
        while True:
            raw_event = self.ser.readline().decode('utf-8')

            event = BoardEvent(raw_event)
            
            if event.square == -1:
                print(compute_deltas(self.start_position, self.current_position))
            else:
                if event.is_lift == True:
                    piece = self.current_position.remove_piece_at(event.square)
                    if piece == None:
                        print("You lifted a piece from an empty square!")
                        print("People like you are the reason we have to implement error handling.")
                    self.pieces_in_air.put(piece)
                    print(self.current_position)
                if event.is_lift == False:
                    piece = self.pieces_in_air.get()
                    self.current_position.set_piece_at(event.square, piece)
                    print(self.current_position)

                print(list(self.pieces_in_air.queue))


