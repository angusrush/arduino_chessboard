import chess
import queue
import logging

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

            # This part is just because the chessboard is only 2x2. Should be
            # removed later.
            if self.square == 2:
                self.square = 8
            elif self.square == 3:
                self.square = 9

            if raw_event[1] == "up":
                self.is_lift = True
            elif raw_event[1] == "down":
                self.is_lift = False
            else:
                print("Parsing error")

    # The string associated to such an event should have the form of the original one
    def __str__(self):
        if self.is_lift == True:
            movement = "up"
        else:
            movement = "down"

        if self.square == -1:
            square = "B"
        else:
            square = self.square

        return str(square) + " " + movement

# The brains of the operation. Defines a function that
class MoveBuilder:
    def __init__(self, board, serial_connection):
        # We want to store a copy of the board position, not the actual board
        # position! i.e. we want to pass by value, not reference
        self.start_position = chess.Board()
        self.start_position.set_fen(board.fen())
        # Same as above
        self.current_position = chess.Board()
        self.current_position.set_fen(board.fen())
        self.pieces_in_air = queue.Queue()
        self.ser = serial_connection

    def set_up_pieces(self):
        # listen for raw events until b is pressed
        while BoardEvent(self.ser.readline().decode('utf-8')).square != -1:
            continue

    def set_up_pieces_and_check(self):
        self.set_up_pieces()

        # then request the bitmap of covered squares from the arduino
        self.ser.write('a'.encode())
        # and for now, just print it
        print(self.ser.readline().decode('utf-8'))

    def listen_for_move(self): # Returns a legal Move
        scratchboard = chess.Board()
        while True:
            # Whenever an event comes over the serial connection, return it,
            # and log it
            raw_event = self.ser.readline().decode('utf-8')
            event = BoardEvent(raw_event)
            logging.info("Event recognized: " + str(event))

            # The button is the square indexed by -1
            if event.square == -1:
                scratchboard.set_fen(self.start_position.fen())
                for move in self.start_position.legal_moves:
                    scratchboard.push(move)

                    # This will be the case for all legal moves except promotions
                    if scratchboard.piece_map() == self.current_position.piece_map():

                        logging.info(f"Legal move made: {move}")

                        self.start_position.push(move)
                        self.pieces_in_air.queue.clear()
                        return move

                    scratchboard.pop()
                return chess.Move.null()
            else:
                if event.is_lift == True:
                    piece = self.current_position.remove_piece_at(event.square)
                    if piece == None:
                        logging.error(f"Piece lifted from square {event.square}."
                                      + "But that square is empty!")
                    self.pieces_in_air.put(piece)
                if event.is_lift == False:
                    piece = self.pieces_in_air.get()
                    self.current_position.set_piece_at(event.square, piece)
            
            print(str(self.current_position) + '\n\n')

