"""Galactic Mess Game"""

import random

import pgzero
import pgzrun

WIDTH = 600
HEIGHT = 450
TITLE = "Space Explorer"

hero = Actor("hero1", (80, 225))
monster = Actor("monster3", (520, 80))
monster2 = Actor("monster1", (100, 80))
warp_pad = Actor("warp_pad", (530, 380))

game_over = False  # if this is True the game stops
monster_active = False  # if True the monster appears
time_on_planet = 0

# Planet variables
planet_images = ["planet1", "planet2", "planet3"]
planet_number = 0

# Monster movement variables
xvel = 3
yvel = 3

# Crystals list
crystals = []
crystals_collected = 0
ammo = 0

# monsters list
monsters = [monster, monster2]


# Going to a new planet
def new_planet():
    global time_on_planet, monster_active

    time_on_planet = 0
    monster_active = False

    # Reset positions
    hero.pos = (80, 225)
    monster.pos = (520, 80)

    # Remove any old crystals
    crystals.clear()

    # Create 3 crystals
    for i in range(3):
        new_crystal()


# Make a new crystal
def new_crystal():
    # Random coordinates
    x = random.randint(100, 500)
    y = random.randint(100, 350)

    crystal = Actor("crystal1", (x, y))
    crystals.append(crystal)  # store in list


def draw():
    global crystals_collected, ammo

    # Draw background image
    screen.blit(planet_images[planet_number], (0, 0))

    # Draw monster if active
    if monster_active:
        for monster in monsters:
            monster.draw()

    # Draw warp pad
    warp_pad.draw()

    # Draw crystals
    for crystal in crystals:
        crystal.draw()

    # Draw hero actor
    hero.draw()

    # Update scores
    screen.draw.text(f"Crystals: {crystals_collected}", (0, 0), color="green")
    screen.draw.text(f"Ammo: {ammo}", (0, 15), color="green")


def convert_crystals_to_ammo():
    global crystals_collected, ammo
    ammo = crystals_collected * 10
    crystals_collected = 0


def update(dt):
    global game_over, time_on_planet, monster_active, xvel, yvel, planet_number, crystals_collected

    if game_over:
        return  # don't update anything

    # Hero movement
    if keyboard.left:
        hero.x -= 10
    if keyboard.right:
        hero.x += 10
    if keyboard.up:
        hero.y -= 10
    if keyboard.down:
        hero.y += 10

    # Calculate time on planet
    time_on_planet += dt

    # Activate monster after some time
    if time_on_planet > 3:
        monster_active = True

    if monster_active:
        for monster in monsters:
            # Monster movement
            monster.x += xvel
            monster.y += yvel

            if monster == monster2:
                print(monster.x, monster.y)
                # time.sleep(0.2)
                screen.draw.text(
                    f"x:{monster.x} y:{monster.y}",
                    (int(monster.x), int(monster.y)),
                    color="green",
                )

            # Bounce off the left/right
            if monster.left < 0 or monster.right > 600:
                xvel = -xvel

            # Bounce off the top/bottom edges
            if monster.top < 0 or monster.bottom > 450:
                yvel = -yvel

            # Monster-hero collision
            if monster.collidepoint(hero.pos) and (monster != monster2):
                game_over = True

    # Check if hero used warp pad
    if hero.collidepoint(warp_pad.pos):
        if planet_number < 2:
            planet_number += 1
        else:
            planet_number = 0

        new_planet()

    # Hero-crystal collision
    for crystal in crystals:
        # crystal movement
        crystal.x += 1

        if crystal.x > 600:
            crystal.x = 0

        if hero.colliderect(monster2):
            convert_crystals_to_ammo()

        if hero.colliderect(crystal):
            crystals.remove(crystal)
            crystals_collected += 1


pgzrun.go()  # Keep this at the bottom
