"""
paddle class - controls paddle movement
"""
from turtle import Turtle


class Paddle(Turtle):
    def __init__(self, screen_dims):
        super().__init__()
        self.screen_dims = screen_dims
        self.shape('square')
        self.penup()
        self.color("white")
        self.shapesize(stretch_len=5)  # stretches the paddle
        # sets paddle to the bottom center of screen
        self.starting_coordinates = 0, - (self.screen_dims[1]/2) + 50
        self.goto(self.starting_coordinates)

    def move_left(self):
        """
        moves the paddle left if paddle will not hit the left edge
        :return True if paddle moves, False if not
        """
        if self.xcor() - 20 > - (self.screen_dims[0] / 2) + 50:
            self.goto(self.xcor()-20, self.ycor())
            return True
        return False

    def move_right(self):
        """
        moves the paddle right if paddle will not hit the right edge
        :return True if paddle moves, False if not
        """
        if self.screen_dims[0]/2 - (self.xcor() + 20) > 50:
            self.goto(self.xcor()+20, self.ycor())
            return True
        return False

    def starting_position(self):
        """
        puts paddle back to starting position
        """
        self.goto(self.starting_coordinates)
