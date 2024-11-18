from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("aMazing")
        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=True)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        
    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

    def draw_cell(self, cell, fill_color):
        cell.draw(self.__canvas, fill_color)
    
    def get_canvas(self):
        return self.__canvas






class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"{self.x}, {self.y}"
    

class Line:
    def __init__(self, point_a, point_b):
        self.point_a = point_a
        self.point_b = point_b

    def draw(self, canvas, fill_color):
        canvas.create_line(self.point_a.x, self.point_a.y, self.point_b.x, self.point_b.y, fill=fill_color, width=2)


class Cell:
    def __init__(self, point_a, point_b, win):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = point_a.x
        self._y1 = point_a.y
        self._x2 = point_b.x
        self._y2 = point_b.y
        self._top_left = Point(min(self._x1, self._x2), min(self._y1, self._y2))
        self._bottom_left = Point(min(self._x1, self._x2), max(self._y1, self._y2))
        self._top_right = Point(max(self._x1, self._x2), min(self._y1, self._y2))
        self._bottom_right = Point(max(self._x1, self._x2), max(self._y1, self._y2))
        self._center = Point(((self._x1+self._x2)/2), ((self._y1+self._y2)/2))
        self._top = Line(self._top_left, self._top_right)
        self._bottom = Line(self._bottom_left, self._bottom_right)
        self._left = Line(self._top_left, self._bottom_left)
        self._right = Line(self._top_right, self._bottom_right)
        self.visited = False
        
        if win is not None:
            self._canvas = win.get_canvas()


    def draw(self, fill_color):
        if self.has_left_wall:
            self._left.draw(self._canvas, fill_color)
        if self.has_right_wall:
            self._right.draw(self._canvas, fill_color)
        if self.has_top_wall:
            self._top.draw(self._canvas, fill_color)
        if self.has_bottom_wall:
            self._bottom.draw(self._canvas, fill_color)

    def draw_move(self, to_cell, undo=False):
        color = "red"
        if undo:
            color = "gray"
        Line(self._center, to_cell._center).draw(self._canvas, color)

    
