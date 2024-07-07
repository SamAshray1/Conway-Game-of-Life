import tkinter as tk
from tkinter import messagebox

# Define the dimensions of the grid and the cell size
GRID_ROWS = 15
GRID_COLS = 15
CELL_SIZE = 50

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

# Draw the grid with activefill
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

    print("update state: ", updatedStateDict)
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

def startGame():
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


def clearAll():
    for key in cells.keys():
        canvas.itemconfig(cells[key], fill="white")

# Bind the click event to the canvas
canvas.bind("<Button-1>", on_canvas_click)

# Initial draw of the grid
draw_grid()

myButton = tk.Button(text="start", command=startGame)
myButton.pack()

myButton = tk.Button(text="reset", command=clearAll)
myButton.pack()


# Run the tkinter main loop
root.mainloop()
