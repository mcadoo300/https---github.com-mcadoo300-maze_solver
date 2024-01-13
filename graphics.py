from tkinter import Tk, BOTH, Canvas

class Window():
    def __init__(self, height,width):
        self._root = Tk()
        self._root.title("Maze Solver")
        self.canvas = Canvas(self._root,bg="white",height=height,width=width)
        self.canvas.pack(fill="both",expand=True)
        self.running = False
        self._root.protocol("WM_DELETE_WINDOW",self.close)
        self.height = height
        self.width = width
        self._root.update_idletasks()
        self._root.update()


    def getInputs(self):
        self.canvas.delete("all")
        

    def setCanvasSize(self,height,width):
        self.canvas = Canvas(self._root,bg="white",height=height,width=width)
        self.canvas.pack(fill="both",expand=True)

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
        canvas.create_line(self.point1.pos_x,self.point1.pos_y,self.point2.pos_x,self.point2.pos_y,fill=fill_color,width=4)
        canvas.pack(fill="both", expand=True)