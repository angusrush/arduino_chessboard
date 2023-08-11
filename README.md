# Smart Chessboard (Name TBD)

## What is this?

Smart Chessboard is a smart chessboard. The hardware consists of a grid of reed switches read by an arduino. The arduino sends information about the states of the switches to the computer over a serial connection.

This information is then parsed by a python program. The state of the board is displayed live, and the moves are checked for legality and recorded. At the end of the game, the moves can be exported as a PGN file, which can be loaded into any modern chess software.

## Why does this exist?

My girlfriend and I like to play chess, and we like to analyze our games with engines in order to improve. However, we both got tired of recording our moves during games. Existing smart chessboards are either much worse (one has to manually enter the moves after you play them) or very expensive. And honestly, it seemed like a nice project.

## License

Smart Chessboard is licensed under the GPL 3 (or any later version at your preference). Full text of the license is available in LICENSE.txt

