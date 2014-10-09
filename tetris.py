from Tkinter import *
import random
import time

from game import *
root = Tk()
root.geometry("400x500")
game = Tetris(root)
quit_button = Button(root, text="quit", command=root.quit)
quit_button.pack( side = TOP )

def down_callback():
    if game.lost == True:
        game.quit()
        score = game.score
        end_screen = Label(root, text="you lose. ("+str(score)+")")
        end_screen.pack()
        play_again_button = Button(root, text="play again?", command=play_again)
        play_again_button.pack()
        return
    game.moveDown()
    root.after(200, down_callback)

def force_down(e):
    game.moveDown()

def left_callback(e):
    game.moveLeft()

def right_callback(e):
    game.moveRight()

def up_callback(e):
    game.rotate()

def play_again():
    Label(root, text="Too bad").pack()

root.bind("<Left>", left_callback)
root.bind("<Right>", right_callback)
root.bind("<Up>", up_callback)
root.bind("<Down>",force_down)
root.after(200, down_callback)
root.mainloop()