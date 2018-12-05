import board
import neopixel
import os

led = neopixel.NeoPixel(board.D18, 270, auto_write = False)


board = [[(0,0,0)] * 15] * 18

def setPixel(x, y, color):
    board[x][y] = color
    led[positionAt(x,y)] = color
    led.show()


def setBoard(newBoard):
    board = newBoard
    reload()

def reload():
    for x in range(0,18):
        for y in range(0,15):
            led[positionAt(x,y)] = board[x][y]
    led.show()

def positionAt(x, y):
    if x % 2 != 0:
        return 252 - 18*x + y
    else:
        return 269 - 18*x - y