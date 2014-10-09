from Tkinter import *
import random
import time

class Tetris:
    def __init__(self, parent):
        self.parent = parent
        self.squares = self.importColors()
        self.the_pile = [[0 for x in range(10)] for x in range(18)]
        self.master_frame = Frame(self.parent)
        self.master_frame.pack()
        self.makePiece()
        self.lost = False
        self.score = 0
        self.speed = 300
        self.level = 1
    
    def __repr__(self):
        string = ''
        for row in self.the_pile:
            string += (str(row))
            string += '\n'
        return string

    def refresh(self):
        self.master_frame.destroy()
        self.master_frame = Frame(self.parent)
        self.master_frame.pack()
        self.row_frames = [Frame(self.master_frame) for x in range(18)]
        self.current_piece.on = self.current_piece.getOn()
        for row in range(18):
            self.row_frames[row].pack( side = TOP )
            for col in range(10):
                if self.the_pile[row][col] != 0:
                    Label(self.row_frames[row], image = self.squares[self.the_pile[row][col]]).pack( side = LEFT )
                elif (row,col) in self.current_piece.on:
                    Label(self.row_frames[row], image = self.squares[self.current_piece.color]).pack( side = LEFT )
                else:
                    Label(self.row_frames[row], image = self.squares[0]).pack( side = LEFT )
    
    def makePiece(self):
        piece_types = ["square","I","L1","L2","N1","N2","T"]
        color_options = {"square":4,"I":2,"L1":7,"L2":1,"N1":5,"N2":6,"T":3}
        rand_type = random.choice(piece_types)
        color = color_options[rand_type]
        if rand_type != "square":
            row = 4
            col = 1
        else:
            row = 4
            col = 0
        self.current_piece = Piece(rand_type, "north", col, row, color)
        for cell in self.current_piece.on:
            if self.the_pile[cell[0]][cell[1]] != 0:
                self.lost = True
                self.current_piece.on = []
    
    def rotate(self):
        self.current_piece.rotateClockwise()
        self.refresh()
    
    def moveDown(self):
        for cell in self.current_piece.on:
            row = cell[0]
            col = cell[1]
            if row == 17 or self.the_pile[row+1][col] != 0:
                self.addToPile()
                return
        self.current_piece.row += 1
        self.current_piece.on = self.current_piece.getOn()
        self.refresh()
    
    def moveLeft(self):
        for cell in self.current_piece.on:
            row = cell[0]
            col = cell[1]
            if col == 0: return
            if self.the_pile[row][col-1] != 0: return
        self.current_piece.col -= 1
        self.refresh()
    
    def moveRight(self):
        for cell in self.current_piece.on:
            row = cell[0]
            col = cell[1]
            if col == 9: return
            if self.the_pile[row][col+1] != 0: return
        self.current_piece.col += 1
        self.refresh()
    
    def addToPile(self):
        self.score += 1
        self.level = self.score % 100
        self.speed = (self.level)/1000
        for cell in self.current_piece.on:
            self.the_pile[cell[0]][cell[1]] = self.current_piece.color
        for row in range(18):
            if 0 in self.the_pile[row]: pass
            else:
                new_board = [[0 for x in range(10)]]
                new_board += (self.the_pile[0:row])
                new_board += (self.the_pile[row+1:18])
                self.the_pile = new_board
        self.makePiece()
        self.refresh()

    def importColors(self):
        squares = []
        for i in range(8):
            filename = "square_"+str(i)+".gif"
            squares.append(PhotoImage(file=filename))
        return squares

    def quit(self):
        time.sleep(0.5)
        self.master_frame.destroy()

class Piece:
    def __init__(self, typeName, orientation, row, col, color):
        self.typeName = typeName
        self.color = color
        self.orientation = orientation
        self.layout = self.getLayout()
        self.row = row
        self.col = col
        self.on = self.getOn()
    
    def getOn(self):
        offset = [-2,-1,0,1,2]
        on = []
        for row in range(5):
            for col in range(5):
                if self.layout[row][col] != 0: on.append((self.row + offset[row],self.col + offset[col]))
        return on
    
    def getLayout(self):
        # Square- only has 1 orientation
        if self.typeName == "square":
            return [
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 1, 1, 0],
                    [0, 0, 1, 1, 0],
                    [0, 0, 0, 0, 0]
                    ]
        #I
        if self.typeName == "I":
            if self.orientation == "north":
                return [
                        [0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 1, 0, 0]
                        ]
            if self.orientation == "east":
                return [
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0]
                        ]
            if self.orientation == "south":
                return [
                        [0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 1, 0, 0]
                        ]
            if self.orientation == "west":
                return [
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0]
                        ]
        #L1
        if self.typeName == "L1":
            if self.orientation == "north":
                return [
                        [0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 1, 1, 0],
                        [0, 0, 0, 0, 0]
                        ]
            if self.orientation == "east":
                return [
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 1, 1, 1, 0],
                        [0, 1, 0, 0, 0],
                        [0, 0, 0, 0, 0]
                        ]
            if self.orientation == "south":
                return [
                        [0, 0, 0, 0, 0],
                        [0, 1, 1, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0]
                        ]
            if self.orientation == "west":
                return [
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0],
                        [0, 1, 1, 1, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0]
                        ]
        #L2
        if self.typeName == "L2":
            if self.orientation == "north":
                return [
                        [0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 1, 1, 0, 0],
                        [0, 0, 0, 0, 0]
                        ]
            if self.orientation == "east":
                return [
                        [0, 0, 0, 0, 0],
                        [0, 1, 0, 0, 0],
                        [0, 1, 1, 1, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0]
                        ]
            if self.orientation == "south":
                return [
                        [0, 0, 0, 0, 0],
                        [0, 0, 1, 1, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0]
                        ]
            if self.orientation == "west":
                return [
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 1, 1, 1, 0],
                        [0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 0]
                        ]
        #N1
        if self.typeName == "N1":
            if self.orientation == "north":
                return [
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0],
                        [0, 0, 1, 1, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0]
                        ]
            if self.orientation == "east":
                return [
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 1, 1, 0, 0],
                        [0, 0, 1, 1, 0],
                        [0, 0, 0, 0, 0]
                        ]
            if self.orientation == "south":
                return [
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0],
                        [0, 0, 1, 1, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0]
                        ]
            if self.orientation == "west":
                return [
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 1, 1, 0, 0],
                        [0, 0, 1, 1, 0],
                        [0, 0, 0, 0, 0]
                        ]
        #N2
        if self.typeName == "N2":
            if self.orientation == "north":
                return [
                        [0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 1, 1, 0],
                        [0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 0]
                        ]
            if self.orientation == "east":
                return [
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 1, 1, 0],
                        [0, 1, 1, 0, 0],
                        [0, 0, 0, 0, 0]
                        ]
            if self.orientation == "south":
                return [
                        [0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 1, 1, 0],
                        [0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 0]
                        ]
            if self.orientation == "west":
                return [
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 1, 1, 0],
                        [0, 1, 1, 0, 0],
                        [0, 0, 0, 0, 0]
                        ]
        #T
        if self.typeName == "T":
            if self.orientation == "north":
                return [
                        [0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 1, 1, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0]
                        ]
            if self.orientation == "east":
                return [
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 1, 1, 1, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0]
                        ]
            if self.orientation == "south":
                return [
                        [0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 1, 1, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0]
                        ]
            if self.orientation == "west":
                return [
                        [0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 1, 1, 1, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0]
                        ]
    
    def rotateClockwise(self):
        if self.orientation == "north":
            self.orientation = "east"
        
        elif self.orientation == "east":
            self.orientation = "south"
        
        elif self.orientation == "south":
            self.orientation = "west"
        
        elif self.orientation == "west":
            self.orientation = "north"
        self.layout = self.getLayout()
