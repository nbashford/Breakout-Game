"""
main app class to run the  breakout game
"""
from turtle import Turtle, Screen
import time
from score import Score  # for the score, level, and lives
from bricks import Bricks  # adding bricks to the game
from paddle import Paddle  # the paddle
from ball import Ball  # the ball

# game setup variables
screen_size = 1000, 700
lives = 7
columns = 10
# rows = 5
rows = 2

# create tk screen and set up
screen = Screen()
screen.tracer(0)
screen.setup(width=screen_size[0], height=screen_size[1])
screen.title("Breakout!")
screen.bgcolor('black')

# set up game components
score = Score(screen_size, lives)
bricks = Bricks(screen_size, columns, rows)
paddle = Paddle(screen_size)
ball = Ball(paddle, screen_size)

# get brick x and y coordinates - for removing bricks
bricks_y_coordinates = bricks.get_brick_y_axis()
bricks_x_coordinates = bricks.get_brick_x_axis()


def move_left():
    """
    moves paddle left, and the ball if on the paddle
    """
    if paddle.move_left() and ball_on_pad:
        ball.move_left()


def move_right():
    """
    moves paddle right, and the ball if on the paddle
    """
    if paddle.move_right() and ball_on_pad:
        ball.move_right()


def ball_start():
    """
    updates ball_on_pad variable to False
    """
    global ball_on_pad
    ball_on_pad = False


def end_game():
    """
    ends the app
    """
    screen.bye()


# event binding
screen.listen()
screen.onkey(move_left,"Left")
screen.onkey(move_right, "Right")
screen.onkey(ball_start, "space")
screen.onkey(end_game, "n")

# variables for game functionality
ball_on_pad = True
# original_ball_speed = 0.03
original_ball_speed = 0.015
ball_speed = original_ball_speed
# ball_speed = 0.015
play = True

while play:
    time.sleep(ball_speed)  # initial speed of the game
    screen.update()

    # if all lives are lost
    if score.lives == 0:
        # clear screen and show game over text
        bricks.remove_all_bricks()
        screen.update()
        score.game_over()
        screen.update()
        time.sleep(5)  # game will restart in 5 unless presses 'q'
        # place items in starting position
        paddle.starting_position()
        ball.starting_position()
        ball_on_pad = True
        # reset and display text
        score.reset_level()
        score.reset_score()
        score.lives = lives
        score.display_all_texts()
        # add the new bricks
        bricks.add_bricks()
        bricks_y_coordinates = bricks.get_brick_y_axis()
        bricks_x_coordinates = bricks.get_brick_x_axis()
        # set to original ball speed
        ball_speed = original_ball_speed

    # if ball is moving
    if not ball_on_pad:
        ball.move_forward()  # moves ball forward

        # change ball direction if ball hits left, right, or top wall
        if ball.xcor() - 10 <= - screen_size[0]/2:  # left wall
            ball.reverse_direction("left")
        if ball.xcor() + 10 >= screen_size[0]/2:  # right wall
            ball.reverse_direction("right")
        if ball.ycor() + 10 >= screen_size[1]/2:  # top wall
            ball.reverse_direction("top")

        # change direction if ball hits the paddle
        if (ball.ycor() - 20 <=  paddle.ycor()  # if ball at paddle y coordinate
            and paddle.xcor() - 50
                <= ball.xcor()
                <= paddle.xcor() + 50):  # if ball within paddle x coordinate
            difference = ball.xcor() - paddle.xcor()  # where the ball hit paddle
            ball.reverse_direction("paddle",  # change direction
                                   difference=difference)  # value to affect direction

        # if ball goes past paddle
        if ball.ycor() - 10 <= - screen_size[1]/2:  # if passed bottom of screen
            score.reduce_lives()  # life lost
            ball.starting_position()  # reset ball position
            paddle.starting_position()  # reset paddle position
            ball_on_pad = True  # update variable

        # functionality to remove bricks if ball hits
        for i, row in enumerate(bricks.bricks_list, start=0):  # iterate over rows of bricks
            # if ball moving up
            if ball.up:
                # if ball within y-coordinate of a brick row
                if (ball.ycor() + 10 >= bricks_y_coordinates[i] - 25 and
                    ball.ycor() <= bricks_y_coordinates[i]+ 20):
                    for j, brick in enumerate(row):  # iterate over bricks in current row
                        # if ball within bricks x-coordinates
                        if (bricks_x_coordinates[j]-50 <= ball.xcor()
                                <= bricks_x_coordinates[j]+50):
                            # remove brick if brick is visible
                            if bricks.disable_brick(row=i, column=j):
                                ball.reverse_direction("top")
                                score.add_score()  # add score
                            # if brick already removed
                            else:
                                # check if hit side of adjacent left brick
                                if j != 0:  # not the left most brick
                                    if (bricks_x_coordinates[j-1] + 60 >= ball.xcor()
                                    and ball.heading() > 90):
                                        # remove adjacent left brick
                                        if bricks.disable_brick(row=i, column=j-1):
                                            ball.reverse_direction("left")
                                            score.add_score()
                                # check if hit side of adjacent right brick
                                if j != 9:  # not the right most brick
                                    if (bricks_x_coordinates[j+1] - 60 <= ball.xcor()
                                    and ball.heading() < 90):
                                        # remove adjacent right brick
                                        if bricks.disable_brick(row=i, column=j+1):
                                            ball.reverse_direction("right")
                                            score.add_score()

            # if ball moving down - same logic as above
            else:
                if (ball.ycor() - 10 <= bricks_y_coordinates[i] + 25 and
                    ball.ycor() >= bricks_y_coordinates[i]):
                    for j, brick in enumerate(row):
                        if (bricks_x_coordinates[j]-50 <= ball.xcor()
                                <= bricks_x_coordinates[j]+50):
                            if bricks.disable_brick(row=i, column=j):
                                ball.reverse_direction("bottom")
                                score.add_score()
                            else:
                                if j != 0:
                                    #left side
                                    if (bricks_x_coordinates[j-1] + 60 >= ball.xcor()
                                    and ball.heading() < 270):
                                        if bricks.disable_brick(row=i, column=j-1):
                                            ball.reverse_direction("left")
                                            score.add_score()
                                    # right side
                                if j != 9:
                                    if (bricks_x_coordinates[j+1] - 60 <= ball.xcor()
                                    and ball.heading() > 270):
                                        if bricks.disable_brick(row=i, column=j+1):
                                            ball.reverse_direction("right")
                                            score.add_score()

        # checking if finished current level
        if all(value is None for row in bricks.bricks_list for value in row):
            # put paddle and ball in starting position
            paddle.starting_position()
            ball.starting_position()
            ball_on_pad = True
            # show user next level info
            score.add_level()
            score.display_next_level()
            screen.update()
            time.sleep(3)
            score.display_all_texts()
            # add the new bricks
            bricks.add_bricks()
            bricks_y_coordinates = bricks.get_brick_y_axis()
            bricks_x_coordinates = bricks.get_brick_x_axis()
            # increase ball speed and activate multiball brick
            ball_speed *= 0.95
            bricks.add_multi_ball(score.level)


screen.mainloop()