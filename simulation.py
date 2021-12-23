import pygame
from pygame.locals import (QUIT, KEYDOWN, MOUSEBUTTONUP, MOUSEBUTTONDOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, K_DOWN)
from Box2D import *
from sys import argv
from random import randint

try:
    arg = float(argv[1]) or 10.0
except IndexError:
    arg = 10.0
PPM = arg
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
bodies = []

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pygame.time.Clock()

world = b2World(gravity=(0, -10), doSleep=True)
ground = world.CreateStaticBody(position=(0, 1), shapes=b2PolygonShape(box=(50, 5)))
bodies.append(ground)

running = True

colors = {
    b2_staticBody: (0, 255, 0, 255),
    b2_dynamicBody: (255, 0, 0, 255),
}

previous_fps = None
while running:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
    already_downed = False
    already_upped = False
    selected_body = None
    key = pygame.mouse.get_pressed()[0]
    fixture = b2FixtureDef(shape=b2PolygonShape(box=(1,1)), density=1, friction=1)
    if key:
        print("pressing")
        if not already_downed:
            print("first time, actually selecting now")
            already_downed = True
            selected_body = world.CreateStaticBody(position=pygame.mouse.get_pos(), fixtures=fixture)
            bodies.append(selected_body)
            print("selected and appened")
        else:
            print("still pressing")
            continue
    if already_downed and not key:
        print("just switched from pressing")
        if not already_upped:
            print("first time, deselecting.")
            already_upped = True
            position_old = selected_body.position
            world.DestroyBody(selected_body)
            selected_body = None
            bodies.append(world.CreateDynamicBody(position=position_old, fixtures=fixture))
            print("deselected, destroyed, and remade")
        else:
            continue
    print(len(bodies))
    count = 0
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        if count == 0:
            count = 100
            for body in bodies:
                body.position = (body.position[0]+1, body.position[1])
    if keys[K_RIGHT]:
        if count == 0:
            count = 100
            for body in bodies:
                body.position = (body.position[0]-1, body.position[1])
    if keys[K_UP]:
        if count == 0:
            count = 100
            for body in bodies:
                body.position = (body.position[0], body.position[1]-1)
    if keys[K_DOWN]:
        if count == 0:
            count = 100
            for body in bodies:
                body.position = (body.position[0], body.position[1]+1)

    if count > 0:
        count -= 1
    screen.fill((255, 255, 255))
    for body in bodies:
        for fixture in body.fixtures:
            shape = fixture.shape

            vertices = [(body.transform * v) * PPM for v in shape.vertices]
            vertices = [(v[0], SCREEN_HEIGHT - v[1]) for v in vertices]

            pygame.draw.polygon(screen, colors[body.type], vertices)
    world.Step(TIME_STEP, 10, 10)
    pygame.display.flip()
    clock.tick(TARGET_FPS)
pygame.quit()
