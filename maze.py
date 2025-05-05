from window import Window, Line, Point
from cell import Cell
import time as timer
import random

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed is not None:
            random.seed(seed)
        self._create_cells()
        self._break_entrence_and_exit()
        self._break_walls_r(0, 0)
        self.solve()
    
    
    def _create_cells(self):
        self.cells = []
        for i in range(self.num_cols):  # Outer loop for columns
            row = []
            for j in range(self.num_rows):  # Inner loop for rows
                x1 = self.x1 + j * self.cell_size_x
                y1 = self.y1 + i * self.cell_size_y
                x2 = x1 + self.cell_size_x
                y2 = y1 + self.cell_size_y
                cell = Cell(x1, y1, x2, y2, self.win)
                cell.visited = False  # Initialize visited attribute
                row.append(cell)
            self.cells.append(row)
        self._animate()

    def _animate(self):
        # First draw all cell walls
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                cell = self.cells[i][j]
                if self.win:
                    cell.draw()
                    
        # Then redraw all moves to ensure they appear on top
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                cell = self.cells[i][j]
                if self.win and hasattr(cell, 'moves'):
                    cell.redraw_moves()
                    
        timer.sleep(0.05)
        if self.win:
            self.win.redraw()

    def _break_entrence_and_exit(self):
        self.cells[0][0].has_top_wall = False
        self.cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False

        if self.win:
            self.cells[0][0].draw()
            self.cells[self.num_cols - 1][self.num_rows - 1].draw()

    def _break_walls_r(self, i, j):
        self._animate()
        current = self.cells[i][j]
        current.visited = True
        while True:
            will_visit = []
            # Check adjacent cells not visited and not out of bounds
            if i > 0 and not self.cells[i - 1][j].visited:
                will_visit.append((i - 1, j))
            if i < self.num_cols - 1 and not self.cells[i + 1][j].visited:
                will_visit.append((i + 1, j))
            if j > 0 and not self.cells[i][j - 1].visited:
                will_visit.append((i, j - 1))
            if j < self.num_rows - 1 and not self.cells[i][j + 1].visited:
                will_visit.append((i, j + 1))
            
            if len(will_visit) == 0:
                break
                
            # Pick a random cell indices from the list
            next_i, next_j = random.choice(will_visit)
            next_cell = self.cells[next_i][next_j]
            
            # Remove wall between current and next cell
            if next_i < i:  # next cell is above
                current.has_top_wall = False
                next_cell.has_bottom_wall = False
            elif next_i > i:  # next cell is below
                current.has_bottom_wall = False
                next_cell.has_top_wall = False
            elif next_j < j:  # next cell is to the left
                current.has_left_wall = False
                next_cell.has_right_wall = False
            elif next_j > j:  # next cell is to the right
                current.has_right_wall = False
                next_cell.has_left_wall = False
                
            # Draw the walls if window exists
            if self.win:
                current.draw()
                next_cell.draw()
            # Move to next cell with recursive _break_walls_r
            self._break_walls_r(next_i, next_j)
        
    def _reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.cells[i][j].visited = False
    
    def solve(self):
        self._reset_cells_visited()
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        current = self.cells[i][j]
        current.visited = True
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True
        # Check adjacent cells not visited and not out of bounds
        if i > 0 and not self.cells[i - 1][j].visited and not current.has_top_wall:
            #draw move
            current.draw_move(self.cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            current.draw_move(self.cells[i - 1][j], undo=True)
        if i < self.num_cols - 1 and not self.cells[i + 1][j].visited and not current.has_bottom_wall:
            current.draw_move(self.cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            current.draw_move(self.cells[i + 1][j], undo=True)
        if j > 0 and not self.cells[i][j - 1].visited and not current.has_left_wall:
            current.draw_move(self.cells[i][j-1])
            if self._solve_r(i, j - 1):
                return True
            current.draw_move(self.cells[i][j-1], undo=True)
        if j < self.num_rows - 1 and not self.cells[i][j + 1].visited and not current.has_right_wall:
            current.draw_move(self.cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            current.draw_move(self.cells[i][j + 1], undo=True)
        return False

