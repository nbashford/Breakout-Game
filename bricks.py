"""
creates bricks and removes them
"""
import random
from turtle import Turtle

# colour options for the bricks
colours = ["green", "yellow", "orange", "red", "purple", "blue"]


class Bricks:
    def __init__(self, screen_dims, columns, rows):
        self.rows = rows  # no. of rows
        self.columns = columns  # no. of columns
        self.screen_dims = screen_dims
        # set the length and width of each brick relative to screen size
        self.brick_length = self.screen_dims[0] / self.columns
        self.brick_width = self.screen_dims[1] / 20
        # ratio to increase brick length/width by from default square size
        self.brick_stretch_len_ratio = self.brick_length / 20
        self.brick_stretch_wid_ratio = self.brick_width / 20

        # create the bricks in a 2D matrix
        self.bricks_list = []
        self.add_bricks()

    def add_bricks(self):
        """
        Adds bricks based on the number of rows and columns
        """
        if self.bricks_list:  # ensures empty list
            self.bricks_list = []
        y = 100  # initial y-coordinate for first row
        for j in range(self.rows):
            brick_row = []  # hold bricks for each row
            # x-coordinate for the first brick
            brick_center = - (self.screen_dims[0]/2) + (self.brick_length / 2)
            colour = colours[j]
            for i in range(self.columns):
                # create rick object
                brick = Brick(colour, self.brick_stretch_len_ratio, self.brick_stretch_wid_ratio, brick_center, y)
                brick_row.append(brick)  # add brick
                brick_center += self.brick_length  # update the next brick x-coordinate
            self.bricks_list.append(brick_row)  # add row of bricks to list
            y += (self.brick_stretch_wid_ratio * 20)  # increase the y-coordinate for next row

    def disable_brick(self, row,  column):
        """
        removes brick based on row and column. Puts None in place
        :param row: row number
        :param column: column number
        :return: True if brick removed, False if already removed
        """
        try:
            self.bricks_list[row][column].hideturtle()
        except AttributeError:
            return False
        self.bricks_list[row][column] = None
        return True

    def remove_all_bricks(self):
        """
        removes all bricks from view
        """
        for row in self.bricks_list:
            for brick in row:
                try:
                    brick.hideturtle()
                except AttributeError:
                    pass
                brick = None


    def get_brick_y_axis(self):
        """
        :return: list of y-coordinates for each row of bricks
        """
        y_coordinates = []
        for row in self.bricks_list:
            y_coordinates.append(row[0].ycor())
        return y_coordinates

    def get_brick_x_axis(self):
        """
        :return: list of x-coordinates for each column of bricks
        """
        x_coordinates = []
        for column in self.bricks_list[0]:
            x_coordinates.append(column.xcor())
        return x_coordinates

    def add_multi_ball(self, level):
        """
        selects n number of bricks at random to activate as 'multi-ball' bricks
        """
        selected_bricks = []

        def get_random_brick():
            rand_row = random.choice(self.bricks_list)
            rand_brick = random.choice(rand_row)
            rand_brick.make_multi_ball()  # make random brick multi-ball brick
            if rand_brick not in selected_bricks:
                selected_bricks.append(rand_brick)
            else:  # select different brick
                get_random_brick()

        for _ in range(level):
            get_random_brick()


class Brick(Turtle):
    def __init__(self, colour, length_stretch, width_stretch, x, y):
        super().__init__()
        self.penup()
        self.shape("square")
        self.color(colour)
        self.shapesize(stretch_len=length_stretch,
                       stretch_wid=width_stretch)
        self.goto(x, y)
        self.multi_ball_brick = None

    def make_multi_ball(self):
        """
        activates brick to be the multi-ball brick
        """
        self.multi_ball_brick = True
        self.color("white")
