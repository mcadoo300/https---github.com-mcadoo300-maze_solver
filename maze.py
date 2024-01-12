import copy
import random
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
        self._root.update_idletasks()
        self._root.update()


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
        self.visited = False

    def draw(self,x1=None,y1=None,x2=None,y2=None):
        if x1 is not None:
            self.x1 = x1
            self.x2 = x2
            self.y1 = y1
            self.y2 = y2
        # left wall: (x1,y1) --> (x1,y2)
        wall_line = Line(Point(self.x1,self.y1),Point(self.x1,self.y2))
        if self.has_left_wall:
            self._window.drawLine(wall_line,"blue")
        else:
            self._window.drawLine(wall_line,"white")
        # right wall: (x2,y1) --> (x2,y2)
        wall_line = Line(Point(self.x2,self.y1),Point(self.x2,self.y2))
        if self.has_right_wall:
            self._window.drawLine(wall_line,"blue")
        else:
            self._window.drawLine(wall_line,"white")
        # top wall: (x1,y1) --> (x2,y1)
        wall_line = Line(Point(self.x1,self.y1),Point(self.x2,self.y1))
        if self.has_top_wall:
            self._window.drawLine(wall_line,"blue")
        else:
            self._window.drawLine(wall_line,"white")
        # bot wall: (x1,y2) --> (x2,y2)
        wall_line = Line(Point(self.x1,self.y2),Point(self.x2,self.y2))
        if self.has_bot_wall:
            self._window.drawLine(wall_line,"blue")
        else:
            self._window.drawLine(wall_line,"white")
    
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
        cell_y1 = row*self.cell_size_y + self.y1
        cell_y2 = cell_y1+self.cell_size_y 

        cell_x1 = col*self.cell_size_x + self.x1
        cell_x2 = cell_x1+self.cell_size_x

        self.cells[row][col].draw(cell_x1,cell_y1,cell_x2,cell_y2)
        self._animate()

    def _animate(self):
        if self._window is None:
            return
        self._window.redraw()
        time.sleep(0.005)
    
    def _break_entrance_and_exit(self):
        entrance = [0,0]
        exit_cell = [self.num_rows-1,self.num_cols-1]
        self.cells[entrance[0]][entrance[1]].has_top_wall=False
        self.cells[entrance[0]][entrance[1]].draw()
        self.cells[exit_cell[0]][exit_cell[1]].has_bot_wall=False
        self.cells[exit_cell[0]][exit_cell[1]].draw()
    
    def _break_walls_r(self,row,col):
        dirs = [[0,1],[0,-1],[1,0],[-1,0]]
        self.cells[row][col].visited = True
        while True:
            adj_moves = []
            for d in dirs:
                if 0 <= row+d[0] < self.num_rows and 0 <= col + d[1] < self.num_cols:
                    if self.cells[row+d[0]][col+d[1]].visited is False:
                        adj_moves.append([[row+d[0],col+d[1]],d])
            
            if len(adj_moves) == 0:
                return
            else:
                rand_move = random.randint(0,len(adj_moves)-1)
                new_p, d1 = adj_moves[rand_move]
                if dirs.index(d1) == 0:
                    self.cells[row][col].has_right_wall = False
                    self.cells[row][col].draw()
                    self._window.redraw()
                    self.cells[new_p[0]][new_p[1]].has_left_wall = False
                    self.cells[new_p[0]][new_p[1]].draw()
                    self._window.redraw()
                elif dirs.index(d1) == 1:
                    self.cells[row][col].has_left_wall = False
                    self.cells[row][col].draw()
                    self._window.redraw()
                    self.cells[new_p[0]][new_p[1]].has_right_wall = False
                    self.cells[new_p[0]][new_p[1]].draw()
                    self._window.redraw()
                elif dirs.index(d1) == 2:
                    self.cells[row][col].has_bot_wall = False
                    self.cells[row][col].draw()
                    self._window.redraw()
                    self.cells[new_p[0]][new_p[1]].has_top_wall = False
                    self.cells[new_p[0]][new_p[1]].draw()
                    self._window.redraw()
                else:
                    self.cells[row][col].has_top_wall = False
                    self.cells[row][col].draw()
                    self._window.redraw()
                    self.cells[new_p[0]][new_p[1]].has_bot_wall = False
                    self.cells[new_p[0]][new_p[1]].draw()
                    self._window.redraw()
                time.sleep(0.05)
                self._break_walls_r(new_p[0],new_p[1])
    
    def reset_visited(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self.cells[i][j].visited = False

    def draw_enter(self):
        center_enter = Point(self.cell_size_x/2 + self.x1,self.cell_size_y/2 + self.y1)
        upper_enter = Point(self.cell_size_x/2 + self.x1,self.y1)
        enter_line = Line(center_enter,upper_enter)
        self._window.drawLine(enter_line,"gray")

    def draw_exit(self):
        center_y = (self.num_rows-1)*self.cell_size_y + self.y1 + self.cell_size_y/2
        center_x = (self.num_cols-1)*self.cell_size_x + self.x1 + self.cell_size_x/2

        center_exit = Point(center_x,center_y)
        lower_exit = Point(center_x,center_y+ self.cell_size_x/2)
        enter_line = Line(center_exit,lower_exit)
        self._window.drawLine(enter_line,"gray")


    def solve(self):
        self.draw_enter()
        
        self._window.redraw()
        row = 0
        col = 0
        searching = True
        dirs = [[0,1],[0,-1],[1,0],[-1,0]]
        self.cells[row][col].visited = True
        paths = [[[row,col]]]
        while searching:
            cur_path = paths.pop(0)
            if len(cur_path) > 1:
                previous_cell = self.cells[cur_path[-2][0]][cur_path[-2][1]]
                next_cell = self.cells[cur_path[-1][0]][cur_path[-1][1]]
                previous_cell.draw_move(next_cell)
                self._window.redraw()
                time.sleep(0.05)
                if cur_path[-1] == [self.num_rows-1,self.num_cols-1]:
                    searching = False
                    self.draw_exit()
                    self._window.redraw()
            if searching:
                row = cur_path[-1][0]
                col = cur_path[-1][1]
                for d in dirs:
                    new_path = copy.deepcopy(cur_path)
                    if 0 <= row+d[0] < self.num_rows and 0 <= col + d[1] < self.num_cols:
                        if self.cells[row+d[0]][col+d[1]].visited is False:
                            # move right
                            if dirs.index(d) == 0:
                                if self.cells[row][col].has_right_wall is False:
                                    new_path.append([row+d[0],col+d[1]])
                                    self.cells[row+d[0]][col+d[1]].visited = True
                                    paths.append(new_path)
                            #move left
                            elif dirs.index(d) == 1:
                                if self.cells[row][col].has_left_wall is False:
                                    new_path.append([row+d[0],col+d[1]])
                                    self.cells[row+d[0]][col+d[1]].visited = True
                                    paths.append(new_path)
                                    
                            # move down
                            elif dirs.index(d) == 2:
                                if self.cells[row][col].has_bot_wall is False:
                                    new_path.append([row+d[0],col+d[1]])
                                    self.cells[row+d[0]][col+d[1]].visited = True
                                    paths.append(new_path)
                            else:
                                if self.cells[row][col].has_top_wall is False:
                                    new_path.append([row+d[0],col+d[1]])
                                    self.cells[row+d[0]][col+d[1]].visited = True
                                    paths.append(new_path)
                        

    def solve2(self):
        self.draw_enter()
        
        self._window.redraw()
        row = 0
        col = 0
        searching = True
        dirs = [[0,1],[0,-1],[1,0],[-1,0]]
        self.cells[row][col].visited = True
        paths = [[[row,col]]]
        while searching:
            cur_path = paths.pop(0)
            if len(cur_path) > 1:
                previous_cell = self.cells[cur_path[-2][0]][cur_path[-2][1]]
                next_cell = self.cells[cur_path[-1][0]][cur_path[-1][1]]
                previous_cell.draw_move(next_cell)
                self._window.redraw()
                time.sleep(0.08)
                if cur_path[-1] == [self.num_rows-1,self.num_cols-1]:
                    searching = False
                    self.draw_exit()
                    self._window.redraw()
            if searching:
                row = cur_path[-1][0]
                col = cur_path[-1][1]
                for d in dirs:
                    new_path = copy.deepcopy(cur_path)
                    if 0 <= row+d[0] < self.num_rows and 0 <= col + d[1] < self.num_cols:
                        if self.cells[row+d[0]][col+d[1]].visited is False:
                            # move right
                            if dirs.index(d) == 0:
                                if self.cells[row][col].has_right_wall is False:
                                    new_path.append([row+d[0],col+d[1]])
                                    self.cells[row+d[0]][col+d[1]].visited = True
                                    #paths.append(new_path)
                                    paths.insert(0,new_path)
                            #move left
                            elif dirs.index(d) == 1:
                                if self.cells[row][col].has_left_wall is False:
                                    new_path.append([row+d[0],col+d[1]])
                                    self.cells[row+d[0]][col+d[1]].visited = True
                                    #paths.append(new_path)
                                    paths.insert(0,new_path)
                                    
                            # move down
                            elif dirs.index(d) == 2:
                                if self.cells[row][col].has_bot_wall is False:
                                    new_path.append([row+d[0],col+d[1]])
                                    self.cells[row+d[0]][col+d[1]].visited = True
                                    #paths.append(new_path)
                                    paths.insert(0,new_path)
                            else:
                                if self.cells[row][col].has_top_wall is False:
                                    new_path.append([row+d[0],col+d[1]])
                                    self.cells[row+d[0]][col+d[1]].visited = True
                                    #paths.append(new_path)
                                    paths.insert(0,new_path)


def main():
    win = Window(1800,1800)
    maze_test = Maze(x1=200,y1=200,num_rows=30,num_cols=30,cell_size_x=30,cell_size_y=30,window=win)
    maze_test._break_entrance_and_exit()
    maze_test._break_walls_r(0,0)
    maze_test.reset_visited()
    maze_test.solve()
    win.waitForClose()

if __name__ == "__main__":
    main()