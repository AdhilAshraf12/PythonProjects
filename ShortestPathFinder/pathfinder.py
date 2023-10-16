import pygame
import math
from tkinter import *
from tkinter import ttk, messagebox
import os
import sys

pygame.init()
screen = pygame.display.set_mode((800, 800))

cols = 50
rows = 50
grid = [[0 for _ in range(rows)] for _ in range(cols)]
openSet = []
closedSet = []
w = 800 // cols
h = 800 // rows

class Spot:
    def __init__(self, x, y):
        self.i = x
        self.j = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.previous = None
        self.obs = False
        self.closed = False
        self.value = 1

    def show(self, color, st):
        if not self.closed:
            pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), st)
            pygame.display.update()

    def path(self, color, st):
        pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), st)

    def addNeighbors(self):
        i, j = self.i, self.j
        if i < cols - 1 and not grid[i + 1][j].obs:
            self.neighbors.append(grid[i + 1][j])
        if i > 0 and not grid[i - 1][j].obs:
            self.neighbors.append(grid[i - 1][j])
        if j < rows - 1 and not grid[i][j + 1].obs:
            self.neighbors.append(grid[i][j + 1])
        if j > 0 and not grid[i][j - 1].obs:
            self.neighbors.append(grid[i][j - 1])

for i in range(cols):
    for j in range(rows):
        grid[i][j] = Spot(i, j)

start = grid[12][5]
end = grid[3][6]

# Initialize GUI
window = Tk()
window.title("A* Pathfinding Visualization")

def onsubmit():
    global start, end
    st = startBox.get().split(',')
    ed = endBox.get().split(',')
    start = grid[int(st[0])][int(st[1])]
    end = grid[int(ed[0])][int(ed[1])]
    window.quit()
    window.destroy()

label = Label(window, text='Start(x,y): ')
startBox = Entry(window)
label1 = Label(window, text='End(x,y): ')
endBox = Entry(window)
var = IntVar()
showPath = ttk.Checkbutton(window, text='Show Steps:', onvalue=1, offvalue=0, variable=var)
submit = Button(window, text='Submit', command=onsubmit)

showPath.grid(columnspan=2, row=2)
submit.grid(columnspan=2, row=3)
label1.grid(row=1, pady=3)
endBox.grid(row=1, column=1, pady=3)
startBox.grid(row=0, column=1, pady=3)
label.grid(row=0, pady=3)
window.update()
mainloop()

openSet.append(start)

def mousePress(x):
    t, w = x[0] // (800 // cols), x[1] // (800 // rows)
    access = grid[t][w]
    if access != start and access != end and not access.obs:
        access.obs = True
        access.show((255, 255, 255), 0)

end.show((255, 8, 127), 0)
start.show((255, 8, 127), 0)

loop = True
while loop:
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.QUIT:
            pygame.quit()
        if pygame.mouse.get_pressed()[0]:
            try:
                pos = pygame.mouse.get_pos()
                mousePress(pos)
            except AttributeError:
                pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                loop = False
                break

for i in range(cols):
    for j in range(rows):
        grid[i][j].addNeighbors()

def heuristic(n, e):
    return math.sqrt((n.i - e.i) ** 2 + (n.j - e.j) ** 2)

def main():
    end.show((255, 8, 127), 0)
    start.show((255, 8, 127), 0)
    if openSet:
        lowestIndex = 0
        for i in range(len(openSet)):
            if openSet[i].f < openSet[lowestIndex].f:
                lowestIndex = i

        current = openSet[lowestIndex]
        if current == end:
            print('done', current.f)
            start.show((255, 8, 127), 0)
            temp = current.f
            for _ in range(round(current.f)):
                current.closed = False
                current.show((0, 0, 255), 0)
                current = current.previous
            end.show((255, 8, 127), 0)

            Tk().wm_withdraw()
            result = messagebox.askokcancel('Program Finished', ('The program finished, the shortest distance \n to the path is ' + str(temp) + ' blocks away, \n would you like to re-run the program?'))
            if result:
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                ag = True
                while ag:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.KEYDOWN:
                            ag = False
                            break
            pygame.quit()

        openSet.pop(lowestIndex)
        closedSet.append(current)

        neighbors = current.neighbors
        for neighbor in neighbors:
            if neighbor not in closedSet:
                tempG = current.g + current.value
                if neighbor in openSet:
                    if neighbor.g > tempG:
                        neighbor.g = tempG
                else:
                    neighbor.g = tempG
                    openSet.append(neighbor)

            neighbor.h = heuristic(neighbor, end)
            neighbor.f = neighbor.g + neighbor.h

            if neighbor.previous is None:
                neighbor.previous = current

    if var.get():
        for node in openSet:
            node.show((0, 255, 0), 0)
        for node in closedSet:
            if node != start:
                node.show((255, 0, 0), 0)
    current.closed = True

while True:
    ev = pygame.event.poll()
    if ev.type == pygame.QUIT:
        pygame.quit()
    pygame.display.update()
    main()
