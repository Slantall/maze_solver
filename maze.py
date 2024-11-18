from graphics import *
import time
import random


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.maze_list = []
        if seed is not None:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()



    def _create_cells(self):
        for col in range(self.num_cols):
            row_list = []
            for row in range(self.num_rows):
                point_a = Point(self.x1 + row*self.cell_size_x, self.y1 + col*self.cell_size_y)
                point_b = Point(self.x1 + (row +1 )*self.cell_size_x, self.y1+(col+ 1)*self.cell_size_y)
                row_list.append(Cell(point_a, point_b, self.win))
            self.maze_list.append(row_list)
        for i in range(len(self.maze_list)):
            for j in range(len(self.maze_list[i])):
                self._draw_cell(i, j)


    def _draw_cell(self, i, j):
        if self.win is None:
            return
        self.maze_list[i][j].draw("black")
        #self._animate()

    def _animate(self):
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(0.05)
    
    def _break_entrance_and_exit(self):
        self.maze_list[0][0].has_top_wall = False
        self.maze_list[-1][-1].has_bottom_wall = False
        if self.win is None:
            return
        self.maze_list[0][0]._top.draw(self.win.get_canvas(), "#d9d9d9")
        self.maze_list[-1][-1]._bottom.draw(self.win.get_canvas(), "#d9d9d9")

    def _break_walls_r(self, i, j):
        self.maze_list[i][j].visited = True
        while True:
            new_neighbors = []
            if i-1 >= 0:
                if not self.maze_list[i-1][j].visited:
                    new_neighbors.append((i-1, j, "up"))
            if j-1 >= 0:
                if not self.maze_list[i][j-1].visited:
                    new_neighbors.append((i, j-1, "left"))
            if i+1 < len(self.maze_list):
                if not self.maze_list[i+1][j].visited:
                    new_neighbors.append((i+1, j, "down"))
            if j+1 < len(self.maze_list[0]):
                if not self.maze_list[i][j+1].visited:
                    new_neighbors.append((i, j+1, "right"))
            if len(new_neighbors) == 0:
                if self.win is not None:
                    self.maze_list[i][j].draw("black")
                return
            next_neighbor = new_neighbors[random.randrange(0, len(new_neighbors))]
            next_cell = self.maze_list[next_neighbor[0]][next_neighbor[1]]
            match next_neighbor[2]:
                case "up":
                    self.maze_list[i][j].has_top_wall = False
                    self.maze_list[i-1][j].has_bottom_wall = False
                    if self.win is not None:
                        self.maze_list[i][j]._top.draw(self.win.get_canvas(), "#d9d9d9")
                        self.maze_list[i-1][j]._bottom.draw(self.win.get_canvas(), "#d9d9d9")
                        #self._animate()
                    self._break_walls_r(i-1, j)
                case "left":
                    self.maze_list[i][j].has_left_wall = False
                    self.maze_list[i][j-1].has_right_wall = False
                    if self.win is not None:
                        self.maze_list[i][j]._left.draw(self.win.get_canvas(), "#d9d9d9")
                        self.maze_list[i][j-1]._right.draw(self.win.get_canvas(), "#d9d9d9")
                        #self._animate()
                    self._break_walls_r(i, j-1)
                case "down":
                    self.maze_list[i][j].has_bottom_wall = False
                    self.maze_list[i+1][j].has_top_wall = False
                    if self.win is not None:
                        self.maze_list[i][j]._bottom.draw(self.win.get_canvas(), "#d9d9d9")
                        self.maze_list[i+1][j]._top.draw(self.win.get_canvas(), "#d9d9d9")
                        #self._animate()
                    self._break_walls_r(i+1, j)
                case "right":
                    self.maze_list[i][j].has_right_wall = False
                    self.maze_list[i][j+1].has_left_wall = False
                    if self.win is not None:
                        self.maze_list[i][j]._right.draw(self.win.get_canvas(), "#d9d9d9")
                        self.maze_list[i][j+1]._left.draw(self.win.get_canvas(), "#d9d9d9")
                        #self._animate()
                    self._break_walls_r(i, j+1)

    def _reset_cells_visited(self):
        for i in range(len(self.maze_list)):
            for j in range(len(self.maze_list[i])):
                self.maze_list[i][j].visited = False

    def solve(self):
        return self._solve_r(0, 0)
        
    
    def _solve_r(self, i, j):
        print(f"cell {i}, {j}")
        self._animate()
        self.maze_list[i][j].visited = True
        if self.maze_list[i][j] == self.maze_list[-1][-1]:
            print("End!")
            return True
        #down
        if i+1 < len(self.maze_list) and not self.maze_list[i][j].has_bottom_wall and not self.maze_list[i+1][j].visited:
            self.maze_list[i][j].draw_move(self.maze_list[i+1][j])
            next_cell= self._solve_r(i+1, j)
            if next_cell:
                return True
            self.maze_list[i][j].draw_move(self.maze_list[i+1][j], True)
        #right
        if j+1 < len(self.maze_list[0]) and not self.maze_list[i][j].has_right_wall and not self.maze_list[i][j+1].visited:
            self.maze_list[i][j].draw_move(self.maze_list[i][j+1])
            next_cell= self._solve_r(i, j+1)
            if next_cell:
                return True
            self.maze_list[i][j].draw_move(self.maze_list[i][j+1], True)
        #up
        if i-1 >= 0 and not self.maze_list[i][j].has_top_wall and not self.maze_list[i-1][j].visited:
            self.maze_list[i][j].draw_move(self.maze_list[i-1][j])
            next_cell= self._solve_r(i-1, j)
            if next_cell:
                return True
            self.maze_list[i][j].draw_move(self.maze_list[i-1][j], True)
        #left
        if j-1 >= 0 and not self.maze_list[i][j].has_left_wall and not self.maze_list[i][j-1].visited:
            self.maze_list[i][j].draw_move(self.maze_list[i][j-1])
            next_cell= self._solve_r(i, j-1)
            if next_cell:
                return True
            self.maze_list[i][j].draw_move(self.maze_list[i][j-1], True)
        return False