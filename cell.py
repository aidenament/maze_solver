from window import Window, Line, Point

class Cell:
    def __init__(self, x1, y1, x2, y2, win=None, has_left_wall=True, has_right_wall=True, has_top_wall=True, has_bottom_wall=True):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.win = win
        self.visited = False
        self.moves = []  # Store moves from this cell

    def draw(self):
        top_left = Point(self.x1, self.y1)
        top_right = Point(self.x2, self.y1)
        bottom_left = Point(self.x1, self.y2)
        bottom_right = Point(self.x2, self.y2)
        if self.has_left_wall:
            self.win.draw_line(Line(top_left, bottom_left), "black")
        else:
            self.win.draw_line(Line(top_left, bottom_left), "#d9d9d9")
        if self.has_right_wall:
            self.win.draw_line(Line(top_right, bottom_right), "black")
        else:
            self.win.draw_line(Line(top_right, bottom_right), "#d9d9d9")
        if self.has_top_wall:
            self.win.draw_line(Line(top_left, top_right), "black")
        else:
            self.win.draw_line(Line(top_left, top_right), "#d9d9d9")
        if self.has_bottom_wall:
            self.win.draw_line(Line(bottom_left, bottom_right), "black")
        else:
            self.win.draw_line(Line(bottom_left, bottom_right), "#d9d9d9")

    def draw_move(self, to_cell, undo=False):
        if not undo:
            color = "red"
        else:
            color = "gray"  # Corrected color code
        # use x y coordinates of two cells to draw a line between them
        center_self = Point((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)
        center_to_cell = Point((to_cell.x1 + to_cell.x2) / 2, (to_cell.y1 + to_cell.y2) / 2)
        line = Line(center_self, center_to_cell)
        self.win.draw_line(line, color)
        
        # Store the move information
        self.moves.append((to_cell, undo, line))
        
    def redraw_moves(self):
        """Redraw all moves from this cell."""
        for to_cell, undo, line in self.moves:
            color = "gray" if undo else "red"
            self.win.draw_line(line, color)

