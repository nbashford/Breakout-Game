"""
score, level and lives functionality
"""

from turtle import Turtle

FONT = ("Arial", 20, "bold")


class Score:
    def __init__(self, screen_dims, lives):

        self.score = 0
        self.level = 0
        self.lives = lives
        self.screen_dims = screen_dims

        # setup turtle text objects
        self.score_turtle = self.create_score_turtle()
        self.level_turtle = self.create_level_turtle()
        self.lives_turtle = self.create_lives_turtle()

    def create_score_turtle(self):
        """
        creates score turtle
        """
        turtle = Turtle()
        turtle.hideturtle()
        turtle.penup()
        turtle.goto(x=-self.screen_dims[0]//2 + 100,
                    y=self.screen_dims[1]//2 - 50)
        turtle.pencolor('white')
        turtle.write(arg=f"Score: {self.score}", move=False, font=FONT,
                     align="center")
        return turtle

    def create_level_turtle(self):
        """
        creates level turtle
        """
        turtle = Turtle()
        turtle.hideturtle()
        turtle.penup()
        turtle.goto(x=-self.screen_dims[0]//2 + 200,
                    y=self.screen_dims[1]//2 - 50)
        turtle.pencolor('white')
        turtle.write(arg=f"Level: {self.level}", move=False, font=FONT,
                     align="center")
        return turtle

    def create_lives_turtle(self):
        """
        creates lives turtle
        """
        turtle = Turtle()
        turtle.hideturtle()
        turtle.penup()
        turtle.goto(x=self.screen_dims[0]//2 - 100,
                    y=self.screen_dims[1]//2 - 50)
        turtle.pencolor('blue')
        turtle.write(arg=f"Lives: {self.lives}", move=False, font=FONT,
                     align="center")
        return turtle

    def add_score(self):
        """
        adds a single score and updates the text
        """
        self.score += 1
        self.score_turtle.clear()
        self.score_turtle.write(arg=f"Score: {self.score}", move=False,
                                font=FONT, align="center")

    def add_level(self):
        """
        adds a single level and updates the text
        """
        self.level += 1
        self.level_turtle.clear()
        self.level_turtle.write(arg=f"Level: {self.level}", move=False,
                                font=FONT, align="center")

    def reset_score(self):
        """
        score is set to 0
        """
        self.score = 0

    def reset_level(self):
        """
        level is set to 0
        """
        self.level = 0

    def reduce_lives(self):
        """
        reduces lives by one if not 0 and updates the text
        """
        if self.lives != 0:
            self.lives -= 1
            self.lives_turtle.clear()
            self.lives_turtle.write(arg=f"Lives: {self.lives}",
                                    move=False, font=FONT, align="center")
