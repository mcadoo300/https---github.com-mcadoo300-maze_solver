import time
from tkinter import Tk, BOTH, Canvas



class Window():
    def __init__(self, height,width):
        self._root = Tk()
        self._root.title("Maze Solver")
        self.canvas = Canvas(self._root,bg="white",height=height,width=width)
        self.canvas.pack(fill="both",expand=True)
        self.running = False
        self._root.protocol("WM_DELETE_WINDOW",self.close)


    def redraw(self):
        self._root.update_idletasks()
        self._root.update()
    
    def waitForClose(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False
    
    def drawLine(self,line,fill_color="black"):
        line.draw(self.canvas,fill_color)


class Point():
    def __init__(self,pos_x,pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y


class Line():
    def __init__(self,point1,point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self,canvas,fill_color):
        canvas.create_line(self.point1.pos_x,self.point1.pos_y,self.point2.pos_x,self.point2.pos_y,fill=fill_color,width=2)
        canvas.pack(fill="both", expand=True)


class Cell():
    def __init__(self,window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bot_wall = True
        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None
        self._window = window

    def draw(self,x1,y1,x2,y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        # left wall: (x1,y1) --> (x1,y2)
        if self.has_left_wall:
            wall_line = Line(Point(self.x1,self.y1),Point(self.x1,self.y2))
            self._window.drawLine(wall_line,"blue")
        # right wall: (x2,y1) --> (x2,y2)
        if self.has_right_wall:
            wall_line = Line(Point(self.x2,self.y1),Point(self.x2,self.y2))
            self._window.drawLine(wall_line,"red")
        # top wall: (x1,y1) --> (x2,y1)
        if self.has_top_wall:
            wall_line = Line(Point(self.x1,self.y1),Point(self.x2,self.y1))
            self._window.drawLine(wall_line,"green")
        # bot wall: (x1,y2) --> (x2,y2)
        if self.has_bot_wall:
            wall_line = Line(Point(self.x1,self.y2),Point(self.x2,self.y2))
            self._window.drawLine(wall_line,"black")
    
    def draw_move(self,to_cell,undo=False):
        mid_x = (self.x1+self.x2) /2
        mid_y = (self.y1+self.y2) /2

        to_mid_x = (to_cell.x1+to_cell.x2) /2
        to_mid_y = (to_cell.y1+to_cell.y2) /2

        move_line = Line(Point(mid_x,mid_y),Point(to_mid_x,to_mid_y))
        if undo:
            self._window.drawLine(move_line,"red")
        else:
            self._window.drawLine(move_line,"gray")


class Maze():
    def __init__(self,x1,y1,num_rows,num_cols,cell_size_x,cell_size_y,window=None):
        self.x1 =x1
        self.y1 =y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._window = window
        self.cells = []
        self._create_cells()

        

    def _create_cells(self):
        self.cells = []
        for row in range(self.num_rows):
            new_row = []
            for col in range(self.num_cols):
                new_row.append(Cell(self._window))
            self.cells.append(new_row)
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self._draw_cell(row,col)
        
    def _draw_cell(self,row,col):
        if self._window is None:
            return
        cell_x1 = row*self.cell_size_x + self.x1
        cell_x2 = cell_x1+self.cell_size_x 

        cell_y1 = col*self.cell_size_y + self.y1
        cell_y2 = cell_y1+self.cell_size_y

        self.cells[row][col].draw(cell_x1,cell_y1,cell_x2,cell_y2)
        self._animate()

    def _animate(self):
        if self._window is None:
            return
        self._window.redraw()
        time.sleep(0.5)
def main():
    win = Window(800,800)
    maze_test = Maze(x1=200,y1=200,num_rows=5,num_cols=5,cell_size_x=50,cell_size_y=50,window=win)

    win.waitForClose()

if __name__ == "__main__":
    main()