from graphics import MazeWindow, WelcomeWindow
from maze import Maze


def main():
    #win = WelcomeWindow()
    win = MazeWindow(500,600)
    pad=25
    maze_test = Maze(x1=pad,y1=pad,num_rows=15,num_cols=15,cell_size_x=15,cell_size_y=15,window=win)

    maze_test.start()
    maze_test._break_entrance_and_exit()
    maze_test._break_walls_r(0,0)
    maze_test.reset_visited()
    
    maze_test.solveBFS()
    win.waitForClose()

if __name__ == "__main__":
    main()