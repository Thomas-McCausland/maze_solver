from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height) -> None:
        self.__window_running = False
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root,
                               height=height,
                               width=width,
                               bg="white"
                        )
        self.__canvas.pack(fill=BOTH, expand=1)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
        
    def wait_for_close(self):
        self.__window_running = True
        while self.__window_running:
            self.redraw()
            
    def draw_line(self, line, colour="black"):
        line.draw(self.__canvas, colour)
    
    def close(self):
        self.__window_running = False

class Point:
    def __init__(self, x=0, y=0) -> None:
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2) -> None:
        self.p1 = p1
        self.p2 = p2
    
    def draw(self, canvas, colour):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=colour, width=2)
        canvas.pack()
