from tkinter import Tk, BOTH, Canvas, messagebox
import tkinter as tk
import sys


class WelcomeWindow():
    def __init__(self):
        self._root = Tk()
        self._root.title("Maze Solver")
        self._root.geometry("500x200")
        self.not_ready=True
        self.num_col = None
        self.num_row = None
        num_col_input = tk.StringVar()
        num_rows_input = tk.StringVar()

        col_input_label = tk.Label(self._root, text="Input number of columns in the maze (min=2,max=30): ", font=('calibre',10,'bold'))
        col_entry = tk.Entry(self._root,textvariable=num_col_input,font=('calibre',10,'bold'))
        col_input_label.grid(row=0,column=0)
        col_entry.grid(row=0,column=1)
        
        row_input_label = tk.Label(self._root, text="Input number of rows in the maze (min=2,max=30): ", font=('calibre',10,'bold'))
        row_entry = tk.Entry(self._root,textvariable=num_rows_input,font=('calibre',10,'bold'))
        row_input_label.grid(row=1,column=0)
        row_entry.grid(row=1,column=1)

        def start():
            if col_entry.get().isdigit() is False:
                messagebox.showerror("Warning", "Please enter a valid digit from 2-30 for columns.")
            elif row_entry.get().isdigit() is False:
                messagebox.showerror("Warning", "Please enter a valid digit from 2-30 for rows.")
            else:
                self.num_col = int(col_entry.get())
                self.num_row = int(row_entry.get())
                if self.num_col < 2:
                    messagebox.showerror("Warning", "The number of columns is too low.")
                elif self.num_col > 30:
                    messagebox.showerror("Warning", "The number of columns is too high.")
                elif self.num_row < 2:
                    messagebox.showerror("Warning", "The number of rows is too low.")
                elif self.num_row > 30:
                    messagebox.showerror("Warning", "The number of rows is too high.")
                else:
                    self.not_ready=False
        start_button = tk.Button(self._root,text= "Start", command= start)
        start_button.grid(row=2,column=0)
    
    def GenNewMaze(self):
        while self.not_ready:
            self._root.update_idletasks()
            self._root.update()
            pass
        x_winfo = self._root.winfo_x()
        y_winfo = self._root.winfo_y()
        self._root.destroy()
        return MazeWindow(1000,1000,x_winfo,y_winfo), [self.num_row,self.num_col]


class MazeWindow():
    def __init__(self, height,width,x_winfo,y_winfo):
        self._root = Tk()
        self._root.title("Maze Solver")
        self.canvas = Canvas(self._root,bg="white",height=height,width=width)
        self.canvas.pack(fill="both",expand=True)
        self.running = True
        self._root.protocol("WM_DELETE_WINDOW",self.close)
        self.height = height
        self.width = width
        self.x_winfo = x_winfo
        self.y_winfo = y_winfo


    

    def setCanvasSize(self,height,width):
        self._root.destroy()
        self._root = Tk()
        self._root.geometry(f"{height}x{width}+{self.x_winfo}+{self.y_winfo}")
        self.canvas = Canvas(self._root,bg="white",height=height,width=width)
        self.canvas.pack(fill="both")
        self.redraw()

    def redraw(self):
        self._root.update_idletasks()
        self._root.update()
    
    def waitForClose(self):
        self.running = True
        while self.running:
            self.redraw()
        self._root.destroy()
        sys.exit()
    
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
        canvas.create_line(self.point1.pos_x,self.point1.pos_y,self.point2.pos_x,self.point2.pos_y,fill=fill_color,width=4)
        canvas.pack(fill="both", expand=True)