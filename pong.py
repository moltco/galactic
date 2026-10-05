import pgzero, pgzrun, random

# Window setup
WIDTH = 600
HEIGHT = 450

# Paddle
paddle = Actor("paddle-1")
paddle.pos = (300, 420)

# Ball
ball = Actor("ball")
ball.pos = (300, 400)
ball.xvel = 4
ball.yvel = -4

# warp pad logic
is_warp_mode = False  # Are we already in the warp mode
hit_count = 0  # How many brick hits
score_position = (0, 420)


# Blocks are w72 h50 px -> we can fit approx sprites per row
# as screen width is 600px, each sprite is 72px
# 0 means no sprite
# 1 black, 2 green, 3 orange, 4 purple, 5 white

sprite_width = 72
sprite_height = 50

map_1 = [
    [2, 0, 0, 0, 3, 0, 5, 0],
    [3, 0, 0, 0, 3, 3, 2, 0],
    [4, 5, 2, 0, 3, 0, 4, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]


def map_to_actors(map):
    rows = len(map)
    cols = len(map[0])

    # actors = [[None for _ in range(cols)] for _ in range(rows)]
    new_actors = []

    for row in range(rows):
        for col in range(cols):

            value = map[row][col]

            if value == 1:
                current_actor = Actor("brick-black")
            elif value == 2:
                current_actor = Actor("brick-green")
            elif value == 3:
                current_actor = Actor("brick-orange")
            elif value == 4:
                current_actor = Actor("brick-purple")
            elif value == 5:
                current_actor = Actor("brick-white")
            else:
                current_actor = None

            # new_actors[row][col] = current_actor
            new_actors.append(current_actor)

            if current_actor is not None:
                current_actor.x = (col * sprite_width) + 0.5 * current_actor.width
                current_actor.y = (row * sprite_height) + 0.5 * current_actor.height

    return new_actors


def draw_actors(actors_to_draw):
    """Go across rows and columns, find the actor and draw it"""
    # rows = len(actors_to_draw)
    # cols = len(actors_to_draw[0])

    # for row in range(rows):
    #     for col in range(cols):
    #         actor = actors_to_draw[row][col]
    #         if actor is not None:  # Only if actor exists!
    #             actor.draw()  # Draw actor

    for new_actor in actors_to_draw:
        if new_actor is not None:
            new_actor.draw()


print(vars(ball))
print("Actors", Actor("brick-black").width, Actor("brick-black").height)


# Game over boolean
game_over = False

actors = map_to_actors(map_1)


def ball_hit_actor():
    global actors, ball, hit_count

    hit_detected = False
    found = None
    for actor in actors:
        if actor != None and ball.colliderect(actor):
            hit_count += 1
            hit_detected = True
            print(f"Killed: {actor.image}")
            found = actor
            break

    if found != None:
        actors.remove(found)
        found = None

    return hit_detected


def draw():
    global actors

    screen.clear()

    # Draw solid color background
    screen.fill((216, 21, 16))

    # Draw paddle
    paddle.draw()
    # Draw ball
    ball.draw()

    draw_actors(actors)

    screen.draw.text(
        f"Score: {hit_count}",
        score_position,
        color="black",
        fontname="mojang-regular",
        fontsize=22,
    )


def update():
    global game_over, hit_count, is_warp_mode, paddle

    # Stop the update function if game over is true
    if game_over == True:
        return
    # Set game over true if ball hits bottom of screen
    if ball.y > 450:
        game_over = True

    # Paddle movement
    if keyboard.right:
        paddle.x += 8
    if keyboard.left:
        paddle.x -= 8

    # Ball movement
    if is_warp_mode:
        ball.x = ball.x + ball.xvel * 2
        ball.y = ball.y + ball.yvel * 2
    else:
        ball.x = ball.x + ball.xvel
        ball.y = ball.y + ball.yvel

    # Ball bouncing
    if ball.x > 600:
        ball.xvel = ball.xvel * -1
    if ball.x < 0:
        ball.xvel = ball.xvel * -1
    if ball.y < 0:
        ball.yvel = ball.yvel * -1

    # Paddle-ball contact
    if ball.colliderect(paddle):
        ball.yvel = -ball.yvel

    had_hit = ball_hit_actor()

    if had_hit:
        ball.xvel = ball.xvel * -1
        ball.yvel = ball.yvel * -1

    if hit_count > 10 and not is_warp_mode:
        is_warp_mode = True
        x = paddle.x
        y = paddle.y
        paddle = Actor("warp_pad")
        paddle.x = x
        paddle.y = y

    draw()

    # screen.draw.text(
    #     f"Score: {hit_count}",
    #     score_position,
    #     color="black",
    #     fontname="mojang-regular",
    #     fontsize=22,
    # )


pgzrun.go()  # Keep this at the end
