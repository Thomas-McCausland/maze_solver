from graphics import Window, Line, Point

class Cell:
    def __init__(self, _win):
        self._win = _win
        self._top_left = None
        self._bottom_right = None
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
    
    def draw(self, top_left, bottom_right):
        self._top_left = top_left # expecting point object
        self._bottom_right = bottom_right # expecting point object
        
        line = Line(top_left, Point(top_left.x, bottom_right.y))
        if self.has_left_wall:
            self._win.draw_line(line)
        else:
            self._win.draw_line(line, colour="white")
            
        line = Line(Point(bottom_right.x, top_left.y), bottom_right)
        if self.has_right_wall:
            self._win.draw_line(line)
        else:
            self._win.draw_line(line, colour="white")
            
        line = Line(top_left, Point(bottom_right.x, top_left.y))
        if self.has_top_wall:
            self._win.draw_line(line)
        else:
            self._win.draw_line(line, colour="white")
            
        line = Line(Point(top_left.x, bottom_right.y), bottom_right)
        if self.has_bottom_wall:
            self._win.draw_line(line)
        else:
            self._win.draw_line(line, colour="white")
            
                        
    def draw_move(self, to_cell, undo=False):
        if not undo:
            fill_colour = "red"
        else:
            fill_colour = "grey"
            
        cell_midpoint = Point(
            (self._top_left.x + self._bottom_right.x) / 2,
            (self._top_left.y + self._bottom_right.y) / 2
        )
        
        to_cell_midpoint = Point(
            (to_cell._top_left.x + to_cell._bottom_right.x) / 2,
            (to_cell._top_left.y + to_cell._bottom_right.y) / 2
        )
        
        midpoint_line = Line(cell_midpoint, to_cell_midpoint)
        self._win.draw_line(midpoint_line, colour = fill_colour)
        