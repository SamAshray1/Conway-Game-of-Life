import math
import time
import tkinter as tk
from tkinter import messagebox
import random

# Define the dimensions of the grid and the cell size
GRID_ROWS = 15
GRID_COLS = 15
CELL_SIZE = 30

# Create the main window
root = tk.Tk()
root.title("Game of Life")

# Define the dimensions of the canvas
canvas_width = GRID_COLS * CELL_SIZE
canvas_height = GRID_ROWS * CELL_SIZE

# Create the canvas widget
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

# Store the grid cells
cells = {}

# Draw the grid with activefill( color when mouse hovers)
def draw_grid():
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x1 = col * CELL_SIZE
            y1 = row * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            rect = canvas.create_rectangle(x1, y1, x2, y2, outline="gray", fill="white", activefill="lightgray")
            cells[(row, col)] = rect

# Handle mouse click event
def on_canvas_click(event):
    col = event.x // CELL_SIZE
    row = event.y // CELL_SIZE
    if (row, col) in cells:
        current_fill = canvas.itemcget(cells[(row, col)], "fill")
        new_fill = "black" if current_fill == "white" else "white"
        canvas.itemconfig(cells[(row, col)], fill=new_fill)

def checkEmptyCanvas(): 
    cordsList = cells.keys()
    emptyFlag = 1
    for key in cordsList:
        current_fill = canvas.itemcget(cells[key], "fill")
        if current_fill == "black":
            emptyFlag = 0
            break

    if emptyFlag == 1:
        print("No cell selected")
        messagebox.showwarning('No Cells Selected!', 'Please select cells..')
        return True

def drawCanvas(dict):
    for key in dict:
        if dict[key] == 1:
            canvas.itemconfig(cells[key], fill="black")
        else:
            canvas.itemconfig(cells[key], fill="white")

def updateState(stateCount):
    
    updatedStateDict = {}
    for key in stateCount.keys():
        currentCellState = stateCount[key][0]
        surroundCells = stateCount[key][1]

        updateCellState = ()
        # Any live cell with two or three live neighbors survives.
        if currentCellState == 1 and (surroundCells == 2 or surroundCells == 3):
            updateCellState = 1
        
        # Any dead cell with exactly three live neighbors becomes a live cell.
        elif currentCellState == 0 and surroundCells == 3:
            updateCellState = 1
        
        else:
            updateCellState = 0
        
        # updatedState[key] = (currentCellState, updateCellState)
        updatedStateDict[key] = updateCellState

    # print("update state: ", updatedStateDict)
    return updatedStateDict


def getState(key, list):

    cellColor = 0
    if canvas.itemcget(cells[key], "fill") == "black":
        cellColor = 1
    else:
        pass
    
    # print(key, list)
    blackCount = 0
    for coords in list:
        # print(coords)
        if coords != key:
            current_fill = canvas.itemcget(cells[coords], "fill")
            if current_fill == "black":
                # print("Black: ", coords)
                blackCount += 1

    return (cellColor, blackCount)

def getNeighbours(key):
    xcord = key[0]
    ycord = key[1]

    neighbourList = []
    for x in [xcord-1, xcord, xcord+1]:
        for y in [ycord-1, ycord, ycord+1]:
            if x >= 0 and x <= GRID_COLS-1 and y >=0 and y <= GRID_ROWS-1:
                neighbourList.append((x, y))
    
    # print(neighbourDict)
    return neighbourList

def nextState():
    cordsList = cells.keys()

    neighbouringDict = {}
    for key in cordsList:
        neighbouringDict[key] = getNeighbours(key)

    # print(neighbouringDict)

    stateCount = {}
    for key in cordsList:
        stateCount[key] = getState(key, neighbouringDict[key])

    # print("State: \n", stateCount)

    updatedStateDict = {}
    updatedStateDict = updateState(stateCount)

    drawCanvas(updatedStateDict)

    return updatedStateDict

def autoRun():
    currentState = nextState()
    def run_step():
        if checkEmptyCanvas():
            return
        nonlocal currentState
        next_state = nextState()
        if next_state == currentState:
            messagebox.showwarning('Final Game State', 'Please select new cells..')
            return
        currentState = next_state
        root.after(500, run_step)
    run_step()

def getRandom():
    rand_int = random.getrandbits(15)
    rand_str = f'{rand_int:015b}'
    print(rand_str)
    return rand_str

def randomGameState():
    randomDict = {}
    for col in range(GRID_COLS):
        randStr = getRandom()
        print(col)
        for row in range(GRID_ROWS):
            print(row, randStr[row])
            randomDict[(row, col)] = int(randStr[row])
    # print(randomDict)

    drawCanvas(randomDict)

def startGame():
    if checkEmptyCanvas():
        return

    if var.get() == 1:
        autoRun()
    else:
        nextState()

def clearAll():
    for key in cells.keys():
        canvas.itemconfig(cells[key], fill="white")

# Bind the click event to the canvas
canvas.bind("<Button-1>", on_canvas_click)

# Initial draw of the grid
draw_grid()

button_frame = tk.Frame(root)
button_frame.pack()

myButton = tk.Button(button_frame, text="Next", command=startGame)
myButton.pack(side="left", padx=10, pady=10)

myButton1 = tk.Button(button_frame, text="Reset", command=clearAll)
myButton1.pack(side="left", padx=10, pady=10)

myButton2 = tk.Button(button_frame, text="Random", command=randomGameState)
myButton2.pack(side="left", padx=10, pady=10)

var = tk.IntVar()
tk.Checkbutton(button_frame, text="Autorun", variable=var, onvalue=1, offvalue=0,
               padx=10, pady=10).pack()

# Run the tkinter main loop
root.mainloop()
