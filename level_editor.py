import pygame
from button import Button
import csv

pygame.init()

clock = pygame.time.Clock()
fps = 60
screen_width = 1100
screen_height = 675
side_margin = 200
bottom_margin = 100

screen = pygame.display.set_mode((screen_width + side_margin, screen_height + bottom_margin))
pygame.display.set_caption('Level Editor')

#Variables
clicked = False
rows = 15
cols = 25
current_tile = 0
tile_size = screen_height // rows
tile_type = 2
level = 1

#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (144, 201, 120)
AQUA = (51, 255, 255)
RED = (200, 25, 25)

font = pygame.font.SysFont('Futura', 24)
title_font = pygame.font.Font('font/tittle.ttf', 30)

#Images
bg_img = pygame.image.load('pic/gameimg.jpg').convert_alpha()

img_list = []
for x in range(tile_type):
    img = pygame.image.load(f'pic/Tile/{x}.png')
    img = pygame.transform.scale(img, (tile_size, tile_size))
    img_list.append(img)

save_img = pygame.image.load('pic/save_btn.png').convert_alpha()
load_img = pygame.image.load('pic/load_btn.png').convert_alpha()

#Create empty tile list
world_data = []
for row in range(rows):
    r = [-1] * cols
    world_data.append(r)

for tile in range(0, cols):
    world_data[rows - 1][tile] = 0

def draw_bg():
        screen.fill(GREEN)
        screen.blit(bg_img, (0, 0))

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_grid():
    for c in range(cols + 1):
        pygame.draw.line(screen, WHITE, (c * tile_size, 0), (c * tile_size, screen_height))
    for r in range(rows + 1):
        pygame.draw.line(screen, WHITE, (0, r * tile_size), (screen_width, r * tile_size))

def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if 0 <= tile < len(img_list):
                screen.blit(img_list[tile], (x * tile_size, y * tile_size))

save_button = Button(screen_width // 2, screen_height + bottom_margin - 50, save_img, 1)
load_button = Button(screen_width // 2 + 200, screen_height + bottom_margin - 50, load_img, 1)

button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = Button(screen_width + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0

run = True
while run:
    clock.tick(fps)

    draw_bg()
    draw_grid()
    draw_world()
    draw_text(f'Level: {level}', font, WHITE, tile_size, screen_height + 20) 
    draw_text('Press UP or DOWN to change level', font, WHITE, tile_size, screen_height + 45)

    if save_button.draw(screen):
        with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            for row in world_data:
                writer.writerow(row)
    if load_button.draw(screen):
        with open(f'level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)
                
    pygame.draw.rect(screen, GREEN, (screen_width, 0, side_margin, screen_height))

    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count
    
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    pos = pygame.mouse.get_pos()
    x = (pos[0]) // tile_size
    y = (pos[1]) // tile_size

    if pos[0] < screen_width and pos[1] < screen_height:
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not clicked:
            clicked = True
            pos = pygame.mouse.get_pos()
            x = pos[0] // tile_size
            y = pos[1] // tile_size
            if x < cols and y < rows:
                if pygame.mouse.get_pressed()[0] == 1:
                    world_data[y][x] += 1
                    if world_data[y][x] >= 3:
                        world_data[y][x] = 0
                elif pygame.mouse.get_pressed()[2] == 1:
                    world_data[y][x] -= 1
                    if world_data[y][x] < 0:
                        world_data[y][x] = tile_type - 1
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            elif event.key == pygame.K_DOWN and level > 1:
                level -= 1

    pygame.display.update()

pygame.quit()