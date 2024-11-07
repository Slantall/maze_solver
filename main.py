from graphics import *

win = Window(800, 600)

point_a = Point(6, 200)
point_b = Point(40.5, 300)
cell = Cell(point_a, point_b, win)
cell2 = Cell(Point(20, 300), Point(60, 400), win)
cell.draw("black")
cell2.draw("black")
cell.draw_move(cell2, True)
win.wait_for_close()