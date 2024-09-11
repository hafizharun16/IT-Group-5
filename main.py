import pygame
import csv

pygame.init()

#Screen settings
WIDTH = 1100
HEIGHT = 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")
clock = pygame.time.Clock()

#Variables
level = 1

#Images
background_img = pygame.image.load("pic/background0.jpg")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
BG = pygame.image.load('pic/gameimg.jpg')
Control_bg = pygame.image.load('pic/controlbg.jpg')
Shop_bg = pygame.image.load('pic/shopbg.jpg')
Credit_bg = pygame.image.load('pic/creditbg.jpg')
Infinity = pygame.image.load('pic/infinity.jpg')

icon_play = pygame.image.load('pic/musicOn.png')
icon_play = pygame.transform.scale(icon_play, (50, 50))
icon_pause = pygame.image.load('pic/musicOff.png')
icon_pause = pygame.transform.scale(icon_pause, (50, 50))

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
AQUA = (51, 255, 255)
GREEN = (144, 201, 120)
RED = (255, 0, 0)

#Tile size
tile_size = 50

#Fonts
title_font = pygame.font.Font('font/tittle.ttf', 30)
title_font2 = pygame.font.Font('font/tittle.ttf', 50)
font = pygame.font.SysFont('font/tittle.ttf', 30)

#State
MAIN_MENU = 0
PLAYING = 1
CONTROLS = 2
SHOP = 3
CREDITS = 4

current_state = MAIN_MENU

#Button
button_width = 150
button_height = 40

buttons = {
    'START': pygame.Rect(((button_width) // 2) + 10, (HEIGHT - button_height + 50) // 2 - 65, button_width, button_height),
    'CONTROL': pygame.Rect(((button_width) // 2) + 10, (HEIGHT - button_height + 50) // 2 + 10, button_width, button_height),
    'SHOP': pygame.Rect(((button_width) // 2) + 10, (HEIGHT - button_height + 50) // 2 + 85, button_width, button_height),
    'CREDIT': pygame.Rect((WIDTH - button_width * 2), (HEIGHT - button_height + 50) // 2 - 65, button_width, button_height),
    'QUIT': pygame.Rect((WIDTH - button_width * 2), (HEIGHT - button_height + 50) // 2 + 10, button_width, button_height)
}

#Music
pygame.mixer.music.load('music/spaceman.mp3')
pygame.mixer.music.play(-1)
icon_rect = pygame.Rect(WIDTH - 60, HEIGHT - 60, 50, 50)
music_playing = True
current_icon = icon_play

def draw_button(button_rect, text, hover):
    button_color = (255, 153, 51) if hover else AQUA
    pygame.draw.rect(screen, button_color, button_rect)
    text_surface = title_font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

def draw_text(text, font, text_col, x, y):
     img = font.render(text, True, text_col)
     screen.blit(img, (x, y))

def draw_icon(icon_image, rect):
    screen.blit(icon_image, rect)

def toggle_music():
    global music_playing, current_icon
    if music_playing:
        pygame.mixer.music.pause()
        current_icon = icon_pause
    else:
        pygame.mixer.music.unpause()
        current_icon = icon_play
    music_playing = not music_playing

#Function
def start_game():
    global current_state
    
    while current_state == PLAYING:
        screen.blit(BG, (0, 0))
        world.draw()
        pygame.display.set_caption("Game")

        draw_text("HEALTH: ", font, RED, 10, 20)
        draw_text("AMMO: ", font, GREEN, 10, 40)

        back_button = pygame.Rect(WIDTH // 2 + 440, HEIGHT // 2 - 320, 100, 50)
        pygame.draw.rect(screen, AQUA, back_button)
        back_text = title_font.render("BACK", True, BLACK)
        back_text_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                current_state = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(pygame.mouse.get_pos()):
                    current_state = MAIN_MENU
                    return

        pygame.display.update()
        clock.tick(60)
    current_state = MAIN_MENU

def draw_grid():
    for line in range(0, 22):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (WIDTH, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, HEIGHT))

def open_control():
    screen.blit(Control_bg, (0, 0))
    control_font = pygame.font.Font(None, 45)
    
    control_texts = [
        "D: Move to the right",
        "A: Move to the left",
        "W: Jump",
        "Mouse: To Aim",
        "Left Click: To Shoot"
    ]
    
    for i, text in enumerate(control_texts):
        control_text = control_font.render(text, True, WHITE)
        text_rect = control_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200 + i * 50))
        screen.blit(control_text, text_rect)

    back_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 250, 150, 50)
    pygame.draw.rect(screen, AQUA, back_button)
    
    back_text = title_font.render("BACK", True, BLACK)
    back_text_rect = back_text.get_rect(center=back_button.center)
    screen.blit(back_text, back_text_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(pygame.mouse.get_pos()):
                    return

        clock.tick(60)

def open_shop():
    screen.blit(Shop_bg, (0, 0))
    shop_font = pygame.font.Font(None, 45)
    shop_text = shop_font.render("Under Maintenance!", True, WHITE)
    shop_rect = shop_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(shop_text, shop_rect)

    back_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 200, 150, 50)
    pygame.draw.rect(screen, AQUA, back_button)
    
    back_text = title_font.render("BACK", True, BLACK)
    back_text_rect = back_text.get_rect(center=back_button.center)
    screen.blit(back_text, back_text_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(pygame.mouse.get_pos()):
                    return
        clock.tick(60)

def open_credit():
    screen.blit(Credit_bg, (0, 0))
    credit_font = pygame.font.Font(None, 45)
    
    credit_texts = [
        "The Main Character: Hafiz",
        "The Author: Imran",
        "The Designer: John Doe",
        "The Final Boss: Mr. Willie"
    ]
    
    for i, text in enumerate(credit_texts):
        credit_text = credit_font.render(text, True, WHITE)
        text_rect = credit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150 + i * 50))
        screen.blit(credit_text, text_rect)

    back_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 200, 150, 50)
    pygame.draw.rect(screen, AQUA, back_button)
    
    back_text = title_font.render("BACK", True, BLACK)
    back_text_rect = back_text.get_rect(center=back_button.center)
    screen.blit(back_text, back_text_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(pygame.mouse.get_pos()):
                    return
        clock.tick(60)

class World():
	def __init__(self, data):
		self.tile_list = []

		#load images
		dirt_img = pygame.image.load('pic/Tile/0.png')
		stone_img = pygame.image.load('pic/Tile/1.png')

		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = pygame.transform.scale(stone_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				col_count += 1
			row_count += 1

	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])

world_data = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], 
[0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 2, 2, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[2, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0], 
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

world = World(world_data)

#Main loop
while True:
    screen.fill((30, 90, 200))
    screen.blit(background_img, (0, 0))
    screen.blit(title_font2.render('CAPTAIN INVADER', True, WHITE), (WIDTH // 2 - 230, 120))

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button_text, button_rect in buttons.items():
                if button_rect.collidepoint(mouse_pos):
                    if button_text == 'START':
                        current_state = PLAYING
                    elif button_text == 'CONTROL':
                        current_state = CONTROLS
                    elif button_text == 'SHOP':
                        current_state = SHOP
                    elif button_text == 'CREDIT':
                        current_state = CREDITS
                    elif button_text == 'QUIT':
                        pygame.quit()
                        exit()
            if icon_rect.collidepoint(mouse_pos):
                toggle_music()

    for button_text, button_rect in buttons.items():
        hover = button_rect.collidepoint(mouse_pos)
        draw_button(button_rect, button_text, hover)

    draw_icon(current_icon, icon_rect)
    pygame.display.update()

    #State handling
    if current_state == PLAYING:
        start_game()
    elif current_state == CONTROLS:
        open_control()
        current_state = MAIN_MENU
    elif current_state == SHOP:
        open_shop()
        current_state = MAIN_MENU
    elif current_state == CREDITS:
        open_credit()
        current_state = MAIN_MENU

    clock.tick(60)

pygame.quit()