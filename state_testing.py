class State:
    def run(self):
        assert 0, "Run not implemented"
    def next(self, input):
        assert 0, "Next not implemented"

class StateMachine:
    def __init__(self, initalState):
        self.currentState = initialState
        self.currentState.run()
    # Template method:
    def runAll(self, inputs):
        for i in inputs:
            print(i)
            self.currentState = self.currentState.next(i)
            self.currentState.run()



class Event:
    __init__(self, square, piece_lifted)
    # square is a string, e.g. 'e2'.
    # piece_lifted is a boolean: True means lifted, False means put down.
    self.square = square
    self.is_lift = piece_lifted

class MoveBuilder:
    _state = 'Waiting'

