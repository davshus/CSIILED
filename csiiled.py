import board
import neopixel
import os

led = neopixel.NeoPixel(board.D18, 270, auto_write = False)


board = [[(0,0,0) for i in range(15)] for i in range(18)]

def setPixel(x, y, color):
    board[x][y] = color
    led[positionAt(x,y)] = color
    led.show()


def setBoard(newBoard):
    for x in range(0,18):
        for y in range(0,15):
            board[x][y] = newBoard[x][y]
    #board = newBoard
    print(board)
    reload()

def reload():
    print(board)
    for x in range(0,18):
        for y in range(0,15):
            led[positionAt(x,y)] = board[x][y]
            print(str(positionAt(x,y)) + "\t" + str((x,y)) + "\t" + str(board[x][y]))
    led.show()

def positionAt(x, y):
    if y % 2 != 0:
        return 269 - 18*y - (17-x)
    else:
        return 269 - 18*y - x
