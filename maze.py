import time, random
from cell import Cell
from graphics import Point

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols,
                 cell_size_x, cell_size_y,
                 win = None, seed = None
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        
        if seed is not None:
            random.seed(seed)
            
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(
            random.randint(0, self._num_cols-1),
            random.randint(0, self._num_rows-1)    
        )
        self._reset_cells_visited()
        self.solve()
    
    def _create_cells(self): # make specified amount of cells in rows & columns

        for i in range(0, self._num_cols):
            self._cells.append([])

        for column in self._cells:
            for i in range(0, self._num_rows):
                column.append(Cell(self._win))
                
        if self._win is None:
            return
        
        for i, column in enumerate(self._cells):
            for j, cell in enumerate(column):
                self._draw_cell(i, j)
                
    
    def _draw_cell(self, i, j): # draw specific cell
        cell = self._cells[i][j]
        # figuring out where to place the cell
        ## add cell_size_x/y at end to compensate for index starting at 0
        start_x = (i*self._cell_size_x)+self._x1
        start_y = (j*self._cell_size_y)+self._y1
        
        cell._top_left = Point(start_x, start_y)
        cell._bottom_right = Point(start_x + self._cell_size_x,
                                   start_y + self._cell_size_y)
        
        cell.draw(cell._top_left, cell._bottom_right)
        self._animate()
        
    def _animate(self):
        self._win.redraw()
        time.sleep(0.01)
        
    def _break_entrance_and_exit(self): # create the entrance and exit (same in every maze)
        entrance = self._cells[0][0]
        entrance.has_top_wall = False
        exit = self._cells[-1][-1]
        exit.has_bottom_wall = False
        
        if self._win is not None:
            self._draw_cell(0,0)
            
        if self._win is not None:
            self._draw_cell(self._num_cols - 1, self._num_rows - 1)
            # x-1 to account for list index starting at 0
            
    def _break_walls_r(self, i, j): # recursively break walls
        self._cells[i][j].visited = True
        
        while True:
            visitable_cells = []
            # finding visitable cells
            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                visitable_cells.append((i - 1, j))
            # right
            if (i < self._num_cols - 1 and
                not self._cells[i + 1][j].visited):
                visitable_cells.append((i + 1, j))
            # up 
            if j > 0 and not self._cells[i][j - 1].visited:
                visitable_cells.append((i, j - 1))
            # down
            if (j < self._num_rows - 1 and
                not self._cells[i][j + 1].visited):
                visitable_cells.append((i, j + 1))
                
            # exit if there is nowhere to go
            if not visitable_cells:
                if self._win is not None:
                    self._draw_cell(i, j)
                return
            
            # randomly choose the next direction to go
            direction_index = random.randrange(len(visitable_cells))
            next_index = visitable_cells[direction_index]
            
            # remove walls from the cells
            # left
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # right
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # up
            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False
            # down
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False            
            
            self._break_walls_r(next_index[0], next_index[1])
                  
    def _reset_cells_visited(self):
        for column in self._cells:
            for cell in column:
                cell.visited = False
    
    def solve(self):
        i, j = 0, 0
        return self._solve_r(i, j)
        
    def _solve_r(self, i, j):
        self._animate()
        current_cell = self._cells[i][j]
        current_cell.visited = True
        
        
        # checking if you're at the end cell
        if current_cell == self._cells[-1][-1]:
            return True
        
        # checking each direction
        if (current_cell.has_left_wall == False and
            self._cells[i - 1][j].visited == False and 
            self._cells[i - 1][j].has_right_wall == False
            ):
            next_cell = self._cells[i - 1][j]
            current_cell.draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            next_cell.draw_move(current_cell, undo = True)
            
        if (current_cell.has_right_wall == False and
              self._cells[i + 1][j].visited == False and
              self._cells[i+1][j].has_left_wall == False
              ):
            next_cell = self._cells[i + 1][j]
            current_cell.draw_move(next_cell)
            if self._solve_r(i + 1, j):
                return True
            next_cell.draw_move(current_cell, undo = True)
            
        if (current_cell.has_top_wall == False and
              self._cells[i][j - 1].visited == False and
              self._cells[i][j - 1].has_bottom_wall == False
              ):
            next_cell = self._cells[i][j - 1]
            current_cell.draw_move(next_cell)
            if self._solve_r(i, j - 1):
                return True
            next_cell.draw_move(current_cell, undo = True)
            
        if (current_cell.has_bottom_wall == False and
              self._cells[i][j + 1].visited == False and
              self._cells[i][j + 1].has_top_wall == False
              ):
            next_cell = self._cells[i][j + 1]
            current_cell.draw_move(next_cell)
            if self._solve_r(i, j + 1):
                return True
            next_cell.draw_move(current_cell, undo = True)
        # Return false if there's no direction to go in.    
        return False
