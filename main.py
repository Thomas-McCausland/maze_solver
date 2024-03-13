from graphics import Window
from maze import Maze

if __name__ == "__main__":
    win = Window(800, 600)
    
    Maze(
        x1=25, y1=25,
        num_rows=11, num_cols=15, # 11 , 15
        cell_size_x=50, cell_size_y=50,
        win=win, seed = 10
    )
    
    win.wait_for_close()
