from graphics import Window
from maze import Maze


def main():
    win = Window(18,18)
    pad=5
    maze_test = Maze(x1=pad,y1=pad,num_rows=15,num_cols=15,cell_size_x=60,cell_size_y=40,window=win)
    
    horizontal = maze_test.num_cols *maze_test.cell_size_x + (pad*2)
    vert = (maze_test.num_rows * maze_test.cell_size_y) + (pad*2)
    win.setCanvasSize(vert,horizontal)
    maze_test.start()
    maze_test._break_entrance_and_exit()
    maze_test._break_walls_r(0,0)
    maze_test.reset_visited()
    
    maze_test.solveBFS()
    win.getInputs()
    win.waitForClose()

if __name__ == "__main__":
    main()