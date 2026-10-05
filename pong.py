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
    [2, 5, 3, 4, 3, 2, 5, 2],
    [3, 4, 2, 3, 3, 3, 2, 3],
    [4, 5, 2, 4, 3, 5, 4, 3],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

map_2 = [
    [1, 2, 3, 4, 3, 2, 5, 2],
    [1, 2, 3, 3, 3, 3, 2, 3],
    [1, 2, 3, 4, 3, 5, 4, 3],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

map_ultimate = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]


def create_random_map(number_of_rows, number_of_columns=8):
    map = []
    for row in range(number_of_rows):
        single_line = []
        for col in range(number_of_columns):
            single_line.append(random.randint(2, 5))
        map.append(single_line)
    return map


levels = [
    create_random_map(2),
    create_random_map(3),
    create_random_map(4),
    create_random_map(5),
    create_random_map(6),
    map_ultimate,
]
current_level = 0


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


def get_map_for_level_up(level):
    return levels[level]


def get_actors_for_level(level):
    return map_to_actors(get_map_for_level_up(level))


actors = get_actors_for_level(current_level)


def count_actors(actors_array):
    cnt = 0
    for actor in actors_array:
        if actor != None:
            cnt += 1
    return cnt


def ball_hit_actor():
    global actors, ball, hit_count, current_level

    hit_detected = False
    found = None
    if count_actors(actors) == 0:
        current_level += 1
        actors = get_actors_for_level(current_level)

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
    global actors, current_level, hit_count

    screen.clear()

    # Draw solid color background
    screen.fill((216, 21, 16))

    # Draw paddle
    paddle.draw()
    # Draw ball
    ball.draw()

    draw_actors(actors)

    screen.draw.text(
        f"Score: {hit_count}, remaining: {count_actors(actors)}, level {current_level}",
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

    # if hit_count > 10 and not is_warp_mode:
    #     is_warp_mode = True
    #     x = paddle.x
    #     y = paddle.y
    #     paddle = Actor("warp_pad")
    #     paddle.x = x
    #     paddle.y = y

    draw()

    # screen.draw.text(
    #     f"Score: {hit_count}",
    #     score_position,
    #     color="black",
    #     fontname="mojang-regular",
    #     fontsize=22,
    # )


pgzrun.go()  # Keep this at the end
