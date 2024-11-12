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
lives = 5
columns = 10
# rows = 5
rows = 2
balls = []  # list to hold all balls in game

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
balls.append(ball)

# get brick x and y coordinates - for removing bricks
bricks_y_coordinates = bricks.get_brick_y_axis()
bricks_x_coordinates = bricks.get_brick_x_axis()


def move_left():
    """
    moves paddle left, and the ball if on the paddle
    """
    moved = paddle.move_left()
    if moved:
        for single_ball in balls:
            if single_ball.on_pad:
                single_ball.move_left()


def move_right():
    """
    moves paddle right, and the ball if on the paddle
    """
    moved = paddle.move_right()
    if moved:
        for single_ball in balls:
            if single_ball.on_pad:
                single_ball.move_right()


def ball_start():
    """
    sets the first or newest ball to be off the paddle (in play)
    """
    on_pad_balls = [single_ball for single_ball in balls if single_ball.on_pad]
    if on_pad_balls:
        on_pad_balls[0].on_pad = False


def end_game():
    """
    ends the app
    """
    screen.bye()


def remove_balls():
    """
    removes all balls except one
    """
    global balls
    # hide all balls
    for single_ball in balls[1:]:
        single_ball.hideturtle()
        single_ball.clear()
    # reset list to only the initial single ball
    balls = balls[0:1]


def remove_single_mulit_ball(_ball):
    """
    removes the passed ball from the game
    :return True if ball removed (multi-ball),
    False if not
    """
    global balls
    if len(balls) > 1:
        ball_index = balls.index(_ball)
        single_ball = balls.pop(ball_index)
        single_ball.hideturtle()
        single_ball.clear()
        return True
    return False


def starting_positions():
    """
    sets the paddle and single ball to starting positions
    """
    paddle.starting_position()
    remove_balls()
    balls[0].starting_position()
    balls[0].on_pad = True

def add_bricks():
    """
    adds bricks to the screen and update x and y coordinates for the bricks
    """
    # add the new bricks
    bricks.add_bricks()
    global bricks_y_coordinates
    global bricks_x_coordinates
    bricks_y_coordinates = bricks.get_brick_y_axis()
    bricks_x_coordinates = bricks.get_brick_x_axis()


def game_over_text():
    """
    removes bricks and text from screen and displays game over text
    """
    bricks.remove_all_bricks()
    screen.update()
    score.game_over()
    screen.update()
    time.sleep(5)  # game restarts in 5 unless presses 'q'


# event binding
screen.listen()
screen.onkey(move_left,"Left")
screen.onkey(move_right, "Right")
screen.onkey(ball_start, "space")
screen.onkey(end_game, "n")

# variables for game functionality
original_ball_speed = 0.023
ball_speed = original_ball_speed  # speed to be increased during game
play = True

# main game loop
while play:
    time.sleep(ball_speed)  # initial speed of the game
    screen.update()

    # if all lives are lost
    if score.lives == 0:
        # clear screen and show game over text
        game_over_text()
        # place game items in starting position
        starting_positions()
        # add bricks to game
        add_bricks()
        # reset and display text
        score.reset_level()
        score.reset_score()
        score.lives = lives
        score.display_all_texts()
        # set to original ball speed
        ball_speed = original_ball_speed

    # for each ball in list balls
    for ball in balls:

        # if ball is moving
        if not ball.on_pad:
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
                if remove_single_mulit_ball(ball):  # multi-ball ball removed and iteration skipped
                    continue
                else:  # ball was not multi-ball
                    score.reduce_lives()  # life lost
                    paddle.starting_position()  # reset paddle position
                    ball.starting_position(paddle)  # reset ball position
                    ball.on_pad = True  # update variable

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
                                brick_removed, multi_ball = bricks.disable_brick(row=i, column=j)
                                if brick_removed:
                                    ball.reverse_direction("top")
                                    score.add_score()  # add score
                                    if multi_ball:
                                        balls.append(Ball(paddle, screen_size))  # add multi-ball

                                # if brick already removed
                                else:
                                    # check if hit side of adjacent left brick
                                    if j != 0:  # not the left most brick
                                        if (bricks_x_coordinates[j-1] + 60 >= ball.xcor()
                                        and ball.heading() > 90):
                                            brick_removed, multi_ball = bricks.disable_brick(row=i, column=j)
                                            if brick_removed:
                                                ball.reverse_direction("left")
                                                score.add_score()  # add score
                                                if multi_ball:
                                                    balls.append(Ball(paddle, screen_size))  # add multi-ball
                                    # check if hit side of adjacent right brick
                                    if j != 9:  # not the right most brick
                                        if (bricks_x_coordinates[j+1] - 60 <= ball.xcor()
                                        and ball.heading() < 90):
                                            brick_removed, multi_ball = bricks.disable_brick(row=i, column=j)
                                            if brick_removed:
                                                ball.reverse_direction("right")
                                                score.add_score()  # add score
                                                if multi_ball:
                                                    balls.append(Ball(paddle, screen_size))  # add multi-ball

                # if ball moving down - same logic as above
                else:
                    if (ball.ycor() - 10 <= bricks_y_coordinates[i] + 25 and
                            ball.ycor() >= bricks_y_coordinates[i]):
                        for j, brick in enumerate(row):
                            if (bricks_x_coordinates[j]-50 <= ball.xcor()
                                    <= bricks_x_coordinates[j]+50):
                                brick_removed, multi_ball = bricks.disable_brick(row=i, column=j)
                                if brick_removed:
                                    ball.reverse_direction("bottom")
                                    score.add_score()  # add score
                                    if multi_ball:
                                        balls.append(Ball(paddle, screen_size))  # add multi-ball
                                else:
                                    if j != 0:
                                        #left side
                                        if (bricks_x_coordinates[j-1] + 60 >= ball.xcor()
                                        and ball.heading() < 270):
                                            brick_removed, multi_ball = bricks.disable_brick(row=i, column=j)
                                            if brick_removed:
                                                ball.reverse_direction("left")
                                                score.add_score()  # add score
                                                if multi_ball:
                                                    balls.append(Ball(paddle, screen_size))  # add multi-ball
                                        # right side
                                    if j != 9:
                                        if (bricks_x_coordinates[j+1] - 60 <= ball.xcor()
                                        and ball.heading() > 270):
                                            brick_removed, multi_ball = bricks.disable_brick(row=i, column=j)
                                            if brick_removed:
                                                ball.reverse_direction("right")
                                                score.add_score()  # add score
                                                if multi_ball:
                                                    balls.append(Ball(paddle, screen_size))  # add multi-ball

    # checking if finished current level
    if all(value is None for row in bricks.bricks_list for value in row):
        # put paddle and ball in starting position
        starting_positions()
        # show user next level info
        score.add_level()
        score.display_next_level()
        screen.update()
        time.sleep(3)
        score.display_all_texts()
        # add the new bricks
        add_bricks()
        # increase ball speed and activate multiball brick
        ball_speed *= 0.95
        bricks.add_multi_ball(score.level)


screen.mainloop()