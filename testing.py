#!/usr/bin/python

from movebuilder import *
import chess
import serial

ser = serial.Serial('/dev/pts/2', 9600)

board = chess.Board()

mb = MoveBuilder(board, ser)
print(mb.listen_for_move())


