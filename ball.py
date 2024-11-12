"""
ball class - controls movement of the ball
"""
from turtle import Turtle
import random

# angle of the ball direction when hits paddle
directions = [50, 25, 0, -25, -50]


class Ball(Turtle):
    def __init__(self, paddle, screen_dims):
        super().__init__()
        self.shape('circle')
        self.color('white')
        self.speed("fastest")
        self.penup()
        self.screen_dims = screen_dims
        # place on the paddle
        self.starting_coordinates = paddle.xcor(), paddle.ycor()+20
        self.goto(self.starting_coordinates)
        # set a random angle from the list of directions
        self.setheading((self.heading()+90) + random.choice(directions))
        self.up = True  # if ball moving up or down
        self.on_pad = True  # if ball currently on paddle

    def move_left(self):
        """
        moves ball left
        """
        self.goto(self.xcor()-20, self.ycor())

    def move_right(self):
        """
        moves ball right
        """
        self.goto(self.xcor()+20, self.ycor())

    def move_forward(self):
        """
        moves ball forward
        """
        self.forward(10)

    def add_difference_angle(self, difference):
        """
        returns the angle based on where the ball has hit the paddle
        :param difference: diff between ball and paddle x-coordinate
        :return: angle
        """
        if difference < -30:
            i = 0
        elif difference < -10:
            i = 1
        elif difference < 10:
            i = 2
        elif difference < 30:
            i = 3
        else:
            i = 4
        return directions[i]

    def reverse_direction(self, side, difference=None):
        """
        changes ball direction based on what the ball has it
        """
        current_angle = self.heading()
        if side == 'left':  # hit left wall or right side of brick
            y = current_angle - 90
            new_angle = 90 - y
        elif side == "right":  # hit right wall or left side of brick
            y = 90 - current_angle
            new_angle = 90 + y
        elif side == 'top':  # hit top wall or bottom side of brick
            y = 90 - current_angle
            new_angle = 270 + y
            self.up = False  # ball moving down
        elif side == "bottom":  # hit top side of brick
            y = 270 - current_angle
            new_angle = 90 + y
            self.up = True  # ball moving up
        elif side == "paddle":  # hit paddle - get angle based on where ball hit
            new_angle = 90 + self.add_difference_angle(difference)
            self.up = True  # ball moving up

        self.setheading(new_angle)  # update ball direction

    def starting_position(self, paddle=None):
        """
        places ball on the centre of the paddle
        """
        starting_coordinates = self.starting_coordinates
        if paddle:
            starting_coordinates = paddle.xcor(), paddle.ycor() + 20
        self.goto(starting_coordinates)
        self.setheading(90 + random.choice(directions))
        self.up = True


