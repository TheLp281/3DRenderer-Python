import pygame
pygame.init()
import pyrr
from math import *
from settings import YAW, PITCH,W_WIDTH, W_HEIGHT,TEXTURE_FOLDER,FOV,WALK_SPEED,SPRINT_MULTIPLIER ,DRAW_DISTANCE,GRID_SIZE,DESIRED_FPS
from game_object import GameObject


pygame.mouse.set_visible(False)
pygame.display.set_caption("3D Renderer")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)


snap_cooldown = 100  # Cooldown time in milliseconds
last_snap_time = pygame.time.get_ticks()
screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT), pygame.RESIZABLE | pygame.OPENGL | pygame.DOUBLEBUF)



objects = []


TILE_SPACING = 1.01

# Create grass grid
for i in range(GRID_SIZE[0]):
    for j in range(GRID_SIZE[1]):
        position = (i * TILE_SPACING, j * TILE_SPACING, 0.0)
        objects.append(GameObject(position,"brick.jpg",rotation=(90,0, 0)) )

from renderer import *

model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
VIEW_LOC = glGetUniformLocation(shader, "view")

# Initialize camera variables
camera_pos = pyrr.Vector3([0.0, 0.0, 3.0])
camera_front = pyrr.Vector3([0.0, 0.0, -1.0])
camera_up = pyrr.Vector3([0.0, 1.0, 0.0])


def handle_mouse_movement(event, yaw, pitch, camera_front):
    global last_mouse_pos

    if last_mouse_pos is None:
        last_mouse_pos = pygame.mouse.get_pos()
        return yaw, pitch, camera_front

    x_offset = event.pos[0] - last_mouse_pos[0]
    y_offset = event.pos[1] - last_mouse_pos[1]
    last_mouse_pos = event.pos

    x_offset *= SENSITIVITY
    y_offset *= SENSITIVITY

    yaw += x_offset
    pitch += y_offset

    # Clamp pitch to avoid camera flipping
    POSITIVE_CLAMP = 89.0  # Adjusted to avoid reaching exactly 90 degrees
    NEGATIVE_CLAMP = -89.0  # Adjusted to avoid reaching exactly -90 degrees
    if pitch > POSITIVE_CLAMP:
        pitch = POSITIVE_CLAMP
    elif pitch < NEGATIVE_CLAMP:
        pitch = NEGATIVE_CLAMP

    # Wrap yaw around 360 degrees
    yaw %= 360

    front = pyrr.Vector3([
        cos(radians(yaw)) * cos(radians(pitch)),
        sin(radians(pitch)),
        sin(radians(yaw)) * cos(radians(pitch))
    ])
    camera_front = pyrr.vector.normalize(front)

    return yaw, pitch, camera_front


def process_input(keys):
    global camera_pos, camera_front, camera_up, YAW, PITCH
    sprint_multiplier = 1
    if keys[pygame.K_LSHIFT]:
        sprint_multiplier = SPRINT_MULTIPLIER

    camera_right = pyrr.vector3.normalize(pyrr.vector3.cross(camera_front, camera_up))
    if keys[pygame.K_w]:
        camera_pos += WALK_SPEED * sprint_multiplier * camera_front
    if keys[pygame.K_s]:
        camera_pos -= WALK_SPEED * sprint_multiplier * camera_front
    if keys[pygame.K_a]:
        camera_pos -= WALK_SPEED * sprint_multiplier * camera_right
    if keys[pygame.K_d]:
        camera_pos += WALK_SPEED * sprint_multiplier * camera_right

    front = pyrr.Vector3([cos(radians(YAW)) * cos(radians(PITCH)), sin(radians(PITCH)), sin(radians(YAW)) * cos(radians(PITCH))])
    camera_front = pyrr.vector.normalize(front)

last_mouse_pos = None

# Function to handle pygame events
def handle_events(yaw, pitch, camera_front):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEMOTION:
            yaw, pitch, camera_front = handle_mouse_movement(event, yaw, pitch, camera_front)
    return yaw, pitch, camera_front

running = True
clock = pygame.time.Clock()
while running:
    keys = pygame.key.get_pressed()
    process_input(keys)

    YAW, PITCH, camera_front = handle_events(YAW, PITCH, camera_front)

    glClearColor(0, 0.1, 0.1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    projection = pyrr.matrix44.create_perspective_projection_matrix(FOV, W_WIDTH / W_HEIGHT, 0.1, DRAW_DISTANCE)
    view = pyrr.matrix44.create_look_at(camera_pos, camera_pos + camera_front, camera_up)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
    glUniformMatrix4fv(VIEW_LOC, 1, GL_FALSE, view)

    for obj in objects:
        obj.render(model_loc, cube)

    fps = clock.get_fps()
    pygame.display.set_caption(f'FPS: {int(fps)}')

    pygame.draw.rect(screen, RED, (10, 10, 100, 50))
    pygame.display.flip()

    clock.tick(DESIRED_FPS)

pygame.mouse.set_visible(True)
# Quit Pygame
pygame.quit()