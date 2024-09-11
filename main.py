import pygame
from button import Button
import csv

pygame.init()

#Screen settings
WIDTH = 1200
HEIGHT = 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")
clock = pygame.time.Clock()

#Variables
rows = 15
cols = 25
tile_size = HEIGHT // rows
tile_type = 2
level = 1

#Images
background_img = pygame.image.load("pic/background0.jpg")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
BG = pygame.image.load('pic/gamebg.jpeg')
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
Control_bg = pygame.image.load('pic/controlbg.jpg')
Control_bg = pygame.transform.scale(Control_bg, (WIDTH, HEIGHT))
Shop_bg = pygame.image.load('pic/shopbg.jpg')
Shop_bg = pygame.transform.scale(Shop_bg, (WIDTH, HEIGHT))
Credit_bg = pygame.image.load('pic/creditbg.jpg')
Credit_bg = pygame.transform.scale(Credit_bg, (WIDTH, HEIGHT))
Infinity = pygame.image.load('pic/infinity.jpg')

icon_play = pygame.image.load('pic/musicOn.png')
icon_play = pygame.transform.scale(icon_play, (50, 50))
icon_pause = pygame.image.load('pic/musicOff.png')
icon_pause = pygame.transform.scale(icon_pause, (50, 50))

img_list = []
for x in range(tile_type):
    img = pygame.image.load(f'pic/Tile/{x}.png')
    img = pygame.transform.scale(img, (tile_size, tile_size))
    img_list.append(img)

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
AQUA = (51, 255, 255)
GREEN = (144, 201, 120)
RED = (255, 0, 0)
YELLOW= (255,255,102)
GREY= (192,192,192)

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

        back_button = pygame.Rect(WIDTH // 2 + 500, HEIGHT // 2 - 380, 100, 50)
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
    shop_text = shop_font.render("0 MYR", True, BLACK)
    shop_rect = shop_text.get_rect(center=(WIDTH - 80, HEIGHT - 610))
    screen.blit(shop_text, shop_rect)
    
    helmet_font = pygame.font.Font(None, 40)
    helmet_text = helmet_font.render ("HELMETS", True, BLACK)
    helmet_rect = helmet_text.get_rect(center=(WIDTH // 2, HEIGHT - 600))

    helmet101_font = pygame.font.Font(None, 31)
    helmet101_text = helmet101_font.render ("- DX200 -", True, BLACK)
    helmet101_rect = helmet101_text.get_rect(center=(240  , HEIGHT - 445))

    helmet102_font = pygame.font.Font(None, 28)
    helmet102_text = helmet102_font.render ("- 10% DMG -= -", True, BLACK)
    helmet102_rect = helmet102_text.get_rect(center=(259  , HEIGHT - 417))

    helmet103_font = pygame.font.Font(None, 31)
    helmet103_text = helmet103_font.render ("- FREE -", True, BLACK)
    helmet103_rect = helmet103_text.get_rect(center=(233  , HEIGHT - 387))


    helmet201_font = pygame.font.Font(None, 31)
    helmet201_text = helmet201_font.render ("- GX500 -", True, BLACK)
    helmet201_rect = helmet201_text.get_rect(center=(550  , HEIGHT - 450))

    helmet202_font = pygame.font.Font(None, 28)
    helmet202_text = helmet202_font.render ("- 50% DMG -= -", True, BLACK)
    helmet202_rect = helmet202_text.get_rect(center=(570  , HEIGHT - 422))

    helmet203_font = pygame.font.Font(None, 31)
    helmet203_text = helmet203_font.render ("- 200MYR -", True, BLACK)
    helmet203_rect = helmet203_text.get_rect(center=(557  , HEIGHT - 392))

    helmet301_font = pygame.font.Font(None, 31)
    helmet301_text = helmet301_font.render ("- GXR7707 -", True, BLACK)
    helmet301_rect = helmet301_text.get_rect(center=(858  , HEIGHT - 445))

    helmet302_font = pygame.font.Font(None, 28)
    helmet302_text = helmet302_font.render ("- 90% DMG -= -", True, BLACK)
    helmet302_rect = helmet302_text.get_rect(center=(870  , HEIGHT - 417))

    helmet303_font = pygame.font.Font(None, 31)
    helmet303_text = helmet303_font.render ("- 500MYR -", True, BLACK)
    helmet303_rect = helmet303_text.get_rect(center=(857  , HEIGHT - 387))

    buy1 = pygame.Rect(190, HEIGHT - 372, 100, 30)
    pygame.draw.rect(screen, GREY, buy1)
    buy2 = pygame.Rect(500, HEIGHT - 372, 100, 30)
    pygame.draw.rect(screen, YELLOW, buy2)
    buy3 = pygame.Rect(800, HEIGHT - 372, 100, 30)
    pygame.draw.rect(screen, YELLOW, buy3)

    buy1_text = title_font.render("USING", True, BLACK)
    buy1_text_rect = buy1_text.get_rect(center=buy1.center)
    screen.blit(buy1_text, buy1_text_rect,)

    buy2_text = title_font.render("BUY", True, BLACK)
    buy2_text_rect = buy2_text.get_rect(center=buy2.center)
    screen.blit(buy2_text, buy2_text_rect,)

    buy3_text = title_font.render("BUY", True, BLACK)
    buy3_text_rect = buy3_text.get_rect(center=buy3.center)
    screen.blit(buy3_text, buy3_text_rect,)



    screen.blit(helmet_text,helmet_rect)
    screen.blit(helmet101_text,helmet101_rect)
    screen.blit(helmet102_text,helmet102_rect)
    screen.blit(helmet103_text,helmet103_rect)
    screen.blit(helmet201_text,helmet201_rect)
    screen.blit(helmet202_text,helmet202_rect)
    screen.blit(helmet203_text,helmet203_rect)
    screen.blit(helmet301_text,helmet301_rect)
    screen.blit(helmet302_text,helmet302_rect)
    screen.blit(helmet303_text,helmet303_rect)
    
    
    suit_font = pygame.font.Font(None, 42)
    suit_text = suit_font.render ("SUITS", True, BLACK)
    suit_rect = suit_text.get_rect(center=(WIDTH // 2, HEIGHT - 288))

    suit101_font = pygame.font.Font(None, 31)
    suit101_text = suit101_font.render ("- MD1485 -", True, BLACK)
    suit101_rect = suit101_text.get_rect(center=(240  , HEIGHT - 140))

    suit102_font = pygame.font.Font(None, 28)
    suit102_text = suit102_font.render ("- 10% DMG -= -", True, BLACK)
    suit102_rect = suit102_text.get_rect(center=(259  , HEIGHT - 115))

    suit103_font = pygame.font.Font(None, 31)
    suit103_text = suit103_font.render ("- FREE -", True, BLACK)
    suit103_rect = suit103_text.get_rect(center=(233  , HEIGHT - 85))


    suit201_font = pygame.font.Font(None, 31)
    suit201_text = suit201_font.render ("- PX13 -", True, BLACK)
    suit201_rect = suit201_text.get_rect(center=(550  , HEIGHT - 140))

    suit202_font = pygame.font.Font(None, 28)
    suit202_text = suit202_font.render ("- 40% DMG -= -", True, BLACK)
    suit202_rect = suit202_text.get_rect(center=(570  , HEIGHT - 115))

    suit203_font = pygame.font.Font(None, 31)
    suit203_text = suit203_font.render ("- 300MYR -", True, BLACK)
    suit203_rect = suit203_text.get_rect(center=(557  , HEIGHT - 85))

    suit301_font = pygame.font.Font(None, 31)
    suit301_text = suit301_font.render ("- CR2020 -", True, BLACK)
    suit301_rect = suit301_text.get_rect(center=(850  , HEIGHT - 140))

    suit302_font = pygame.font.Font(None, 28)
    suit302_text = suit302_font.render ("- 80% DMG -= -", True, BLACK)
    suit302_rect = suit302_text.get_rect(center=(870  , HEIGHT - 115))

    suit303_font = pygame.font.Font(None, 31)
    suit303_text = suit303_font.render ("- 600MYR -", True, BLACK)
    suit303_rect = suit303_text.get_rect(center=(857  , HEIGHT - 85))


    buy4 = pygame.Rect(190, HEIGHT - 70, 100, 30)
    pygame.draw.rect(screen, GREY, buy4)
    buy5 = pygame.Rect(500, HEIGHT - 70, 100, 30)
    pygame.draw.rect(screen, YELLOW, buy5)
    buy6 = pygame.Rect(810, HEIGHT - 70, 100, 30)
    pygame.draw.rect(screen, YELLOW, buy6)

    buy4_text = title_font.render("USING", True, BLACK)
    buy4_text_rect = buy4_text.get_rect(center=buy4.center)
    screen.blit(buy4_text, buy4_text_rect,)

    buy5_text = title_font.render("BUY", True, BLACK)
    buy5_text_rect = buy5_text.get_rect(center=buy5.center)
    screen.blit(buy5_text, buy5_text_rect,)

    buy6_text = title_font.render("BUY", True, BLACK)
    buy6_text_rect = buy6_text.get_rect(center=buy6.center)
    screen.blit(buy6_text, buy6_text_rect,)

    
    screen.blit(suit_text,suit_rect)
    screen.blit(suit101_text,suit101_rect)
    screen.blit(suit102_text,suit102_rect)
    screen.blit(suit103_text,suit103_rect)
    screen.blit(suit201_text,suit201_rect)
    screen.blit(suit202_text,suit202_rect)
    screen.blit(suit203_text,suit203_rect)
    screen.blit(suit301_text,suit301_rect)
    screen.blit(suit302_text,suit302_rect)
    screen.blit(suit303_text,suit303_rect)
    


    back_button = pygame.Rect(20, HEIGHT // 2 + 280, 100, 30)
    pygame.draw.rect(screen, AQUA, back_button)
    
    back_text = title_font.render("BACK", True, BLACK)
    back_text_rect = back_text.get_rect(center=back_button.center)
    screen.blit(back_text, back_text_rect)

    def load_and_resize_image(image_path, size):
        try:
            image = pygame.image.load(image_path)
            return pygame.transform.scale(image, size)
        except pygame.error as e:
            print(f"Unable to load or resize image at {image_path}. Error: {e}")
            return None
    desired_size = (80, 80)
    image2 = load_and_resize_image('Inventory/helmet2.png', desired_size)

    helmet_size = image2.get_size()

    image1 = load_and_resize_image('Inventory/helmet1.png', helmet_size)
    image3 = load_and_resize_image('Inventory/helmet3.png', helmet_size)
    desired_size = (100, 100)
    image02 = load_and_resize_image('Inventory/suit2.png', desired_size)
    image01 = load_and_resize_image('Inventory/suit1.png', desired_size)
    image03 = load_and_resize_image('Inventory/suit3.png', desired_size)
    

    if image1:
        screen.blit(image1, (200, 100))  
    if image2:
        screen.blit(image2, (510, 100)) 
    if image3:
        screen.blit(image3, (800, 100)) 
    if image01:
        screen.blit(image01, (200, 390))  
    if image02:
        screen.blit(image02, (510, 390)) 
    if image03:
        screen.blit(image03, (800, 390))

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

class World:
    def __init__(self, data):
        self.obstacle_list = []
        self.process_data(data)

    def process_data(self, data):
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:  # Check if tile is valid
                    img = img_list[tile]  # Get the tile image from img_list
                    img_rect = img.get_rect()
                    img_rect.x = x * tile_size
                    img_rect.y = y * tile_size
                    self.obstacle_list.append((img, img_rect))

    def draw(self):
        for tile in self.obstacle_list:
            screen.blit(tile[0], tile[1])  # tile[0] is the image, tile[1] is the rect

world_data = []
for row in range(rows):
	r = [-1] * cols
	world_data.append(r)
#load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for x, row in enumerate(reader):
		for y, tile in enumerate(row):
			world_data[x][y] = int(tile)
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