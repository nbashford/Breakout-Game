"""
creates bricks and removes them
"""
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
        y = 100  # initial y-coordinate for first row
        for j in range(self.rows):
            brick_row = []  # hold bricks for each row
            # x-coordinate for the first brick
            brick_center = - (self.screen_dims[0]/2) + (self.brick_length / 2)
            colour = colours[j]
            for i in range(self.columns):
                brick_row.append(self.create_brick(brick_center, y, colour))  # add brick
                brick_center += self.brick_length  # update the next brick x-coordinate
            self.bricks_list.append(brick_row)
            y += (self.brick_stretch_wid_ratio * 20)  # increase the y-coordinate for next row

    def create_brick(self, x, y, colour):
        """
        creates brick turtle object
        :param x: x-coordinate
        :param y: y-coordinate
        :param colour: colour
        :return: square turtle object
        """
        brick = Turtle()
        brick.penup()
        brick.shape("square")
        brick.color(colour)
        brick.shapesize(stretch_len=self.brick_stretch_len_ratio,
                        stretch_wid=self.brick_stretch_wid_ratio)
        brick.goto(x, y)
        return brick

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

