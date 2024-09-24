import pygame
import csv
import sys
import random
import math
from invent import Inventory, load_and_scale_image, IMAGE_SCALE

pygame.init()

WIDTH = 1200
HEIGHT = 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")
clock = pygame.time.Clock()
Shop_bg = pygame.image.load('pic/shop.jpg')

inventory = Inventory()  # Create an instance
inventory.load_from_file("inventory.txt")
inventory.load_from_file("inventory.txt")

BLACK = (0, 0, 0)
AQUA = (51, 255, 255)
GOLD = (255, 215, 0)
GREEN = (144, 201, 120)

title_font = pygame.font.Font('font/tittle.ttf', 30)
game_font = pygame.font.Font('font/WarriotItalic.otf', 30)

rows = 15
cols = 35
current_tile = 0
tile_size = HEIGHT // rows
tile_type = 7
level = 2
screen_scroll = False

MAIN_MENU = 0
BLACK_SCREEN = 1
PLAYING = 2
CONTROLS = 3
SHOP = 4
CREDITS = 5
current_state = MAIN_MENU

img_list = []
for x in range(tile_type):
    img = pygame.image.load(f'pic/Tile/{x}.png')
    img = pygame.transform.scale(img, (tile_size, tile_size))
    img_list.append(img)

class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)
        print(f"Added {item} to inventory.")

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            for item in self.items:
                f.write(f"{item}\n")

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                self.items = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            print("Inventory file not found, starting with an empty inventory.")

def update_player_images(inventory):
    global standing_image, walking_images, ducking_image  # Ensure we can modify these
    for item in inventory.items:
        if item == "helmet_2":
            standing_image = load_and_scale_image('Store/H2S1/normal.png', IMAGE_SCALE)
            walking_images = [
                load_and_scale_image('Store/H2S1/H2S1A.png', IMAGE_SCALE),
                load_and_scale_image('Store/H2S1/H2S1B.png', IMAGE_SCALE),
                load_and_scale_image('Store/H2S1/H2S1C.png', IMAGE_SCALE),
                load_and_scale_image('Store/H2S1/H2S1D.png', IMAGE_SCALE)
            ]
            ducking_image = load_and_scale_image('Store/H2S1/H2S1D.png', IMAGE_SCALE)
        elif item == "helmet_3":
            standing_image = load_and_scale_image('Store/H3S1/normal.png', IMAGE_SCALE)
            walking_images = [
                load_and_scale_image('Store/H3S1/H3S1A.png', IMAGE_SCALE),
                load_and_scale_image('Store/H3S1/H3S1B.png', IMAGE_SCALE),
                load_and_scale_image('Store/H3S1/H3S1C.png', IMAGE_SCALE),
                load_and_scale_image('Store/H3S1/H3S1D.png', IMAGE_SCALE)
            ]
            ducking_image = load_and_scale_image('Store/H3S1/H3S1A.png', IMAGE_SCALE)
        elif item == "suit_2":
            standing_image = load_and_scale_image('Store/H1S2/normal.png', IMAGE_SCALE)
            walking_images = [
                load_and_scale_image('Store/H1S2/H1S2A.png', IMAGE_SCALE),
                load_and_scale_image('Store/H1S2/H1S2B.png', IMAGE_SCALE),
                load_and_scale_image('Store/H1S2/H1S2C.png', IMAGE_SCALE),
                load_and_scale_image('Store/H1S2/H1S2D.png', IMAGE_SCALE)
            ]
            ducking_image = load_and_scale_image('Store/H1S2/H1S2A.png', IMAGE_SCALE)
        elif item == "suit_3":
            standing_image = load_and_scale_image('Store/H2S1/H2S1A.png', IMAGE_SCALE)
            walking_images = [
                load_and_scale_image('Store/H2S1/H2S1A.png', IMAGE_SCALE),
                load_and_scale_image('Store/H2S1/H2S1A.png', IMAGE_SCALE),
                load_and_scale_image('Store/H2S1/H2S1A.png', IMAGE_SCALE),
                load_and_scale_image('Store/H2S1/H2S1A.png', IMAGE_SCALE)
            ]
            ducking_image = load_and_scale_image('Store/H2S1/H2S1A.png', IMAGE_SCALE)

# Call this function after loading the inventory in Level 2
update_player_images(inventory) 

def start_game_2():
    global current_state
    
    WIDTH = 1200
    HEIGHT = 750
    FPS = 60
    MOVE_SPEED = 3
    WALKING_SPEED = 80
    IMAGE_SCALE = 0.15
    JUMP_HEIGHT = -10
    GRAVITY = 0.5
    BULLET_SPEED = 30
    BULLET_SCALE = 0.03
    ENEMY_SCALE = 0.2
    ENEMY_SPEED = 1  # Speed of the enemy
    ENEMY_MOVE_AREA_LEFT = 800
    ENEMY_MOVE_AREA_RIGHT = 900

    gate = pygame.image.load("pic/gate1.png")
    gate1 = pygame.transform.scale(gate, (70, 100))
    gate_x, gate_y = WIDTH - 80, 1  
    gate_rect = pygame.Rect(gate_x +50 , gate_y, 70, 100)

    BG = pygame.image.load('pic/gamebg.jpeg')
    BG = pygame.transform.scale(BG, (WIDTH,HEIGHT))

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    # Load and resize images
    def load_and_scale_image(filename, scale_factor):
        image = pygame.image.load(filename)
        width, height = image.get_size()
        new_size = (int(width * scale_factor), int(height * scale_factor))
        return pygame.transform.scale(image, new_size)

    def flip_images(images):
        """Flip images horizontally."""
        return [pygame.transform.flip(img, True, False) for img in images]


    # Load and scale the arm image
    arm_image = load_and_scale_image('Store/H1S1/arm3.png', IMAGE_SCALE)
    flipped_arm_image = pygame.transform.flip(arm_image, True, False)

    # Load bullet image
    bullet_image = load_and_scale_image('Store/bullet3.png', BULLET_SCALE)

    # Load enemy image
    enemy_image = load_and_scale_image('Store/enemy.png', ENEMY_SCALE)

    # Flip images for left movement
    flipped_standing_image = pygame.transform.flip(standing_image, True, False)
    flipped_walking_images = flip_images(walking_images)
    flipped_ducking_image = pygame.transform.flip(ducking_image, True, False)

    # Get image rect
    rect = standing_image.get_rect()
    rect.topleft = (0, HEIGHT - rect.height)

    # Animation control
    current_image = standing_image
    
    walking_index = 0
    walking_timer = pygame.time.get_ticks()
    is_walking = False
    moving_right = True
    is_jumping = True
    is_ducking = False
    jump_speed = 0
    ground_y = HEIGHT -25

    # Enemy class
    class Enemy(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = enemy_image
            self.rect = self.image.get_rect(center=(x, y))
            self.original_x = x
            self.direction = random.choice(["left", "right"])
            self.move_range = 3 * self.image.get_width()  # 3 tiles movement range
            self.left_boundary = self.original_x - self.move_range / 2
            self.right_boundary = self.original_x + self.move_range / 2

        def update(self):
            if self.direction == "right":
                self.rect.x += ENEMY_SPEED
                if self.rect.right >= self.right_boundary:
                    self.direction = "left"
            elif self.direction == "left":
                self.rect.x -= ENEMY_SPEED
                if self.rect.left <= self.left_boundary:
                    self.direction = "right"

    # Bullet class
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y, direction, angle):
            super().__init__()
            self.image = bullet_image
            self.rect = self.image.get_rect(center=(x, y))
            self.direction = direction
            self.angle = angle

        def update(self):
            vel_x = BULLET_SPEED * math.cos(self.angle)
            vel_y = BULLET_SPEED * math.sin(self.angle)

            if self.direction == "right":
                self.rect.x += vel_x
                self.rect.y += vel_y
            else:
                self.rect.x -= vel_x
                self.rect.y -= vel_y

            if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
                self.kill()

    # Create a group to hold all enemies
    enemies = pygame.sprite.Group()

    # Define specific enemy positions
    enemy_positions = [
        (WIDTH // 2 + 30, 90), 
        (WIDTH-160, HEIGHT // 3 +20),
        (WIDTH//2-205, HEIGHT // 2),
        (WIDTH//4+10, HEIGHT // 2 + 150),
        (WIDTH//2-90, HEIGHT - 120)
    ]

    # Add enemies to the group with specific positions
    for pos in enemy_positions:
        enemy = Enemy(*pos)
        enemies.add(enemy)

    # Sprite group for bullets
    bullets = pygame.sprite.Group()

    # Set up the clock
    clock = pygame.time.Clock()
    crosshair_image = pygame.image.load("Store/H1S1/aim.png").convert_alpha()
    crosshair_image = pygame.transform.scale(crosshair_image, (20, 20))

    pygame.mouse.set_visible(False)

    #define game variables
    tile_size = HEIGHT // rows
    title_font = pygame.font.Font('font/tittle.ttf', 30)

    #pygame.mixer.music.load('music/spaceman.mp3')
    #pygame.mixer.music.play(-1)
    icon_play = pygame.image.load('pic/musicOn.png')
    icon_play = pygame.transform.scale(icon_play, (50, 50)) 
    icon_pause = pygame.image.load('pic/musicOff.png')
    icon_pause = pygame.transform.scale(icon_pause, (50, 50)) 
    icon_rect = pygame.Rect(WIDTH - 70, HEIGHT -80, 50, 50) 
    music_playing = True
    current_icon = icon_play

    def draw_icon(icon_image, rect):
        screen.blit(icon_image, rect)

    def draw_grid():
        for line in range(0, 22):
            pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (WIDTH, line * tile_size))
            pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, HEIGHT))

    def update_player_movement():
        global is_jumping, jump_speed

    def check_tile_solidification():
        if not is_jumping:
            for tile in world.tile_list:
                img, rect = tile
                if rect.colliderect(rect.x, rect.y + 1, rect.width, rect.height):
                    tile_type = world.get_tile_type(rect.x // tile_size, rect.y // tile_size)
                    if tile_type in [1, 2]:
                        # Mark the tile as solid
                        world.make_tile_solid(rect.x, rect.y)
                        # Adjust player position if necessary
                        if rect.bottom <= rect.y:
                            rect.bottom = rect.y
                            rect.y = rect.bottom

    class World:
        def __init__(self, data):
            self.tile_list = []
            self.tile_data = []
            self.solid_tiles = set()
            self.load_tile_data(data)


        def load_tile_data(self, data):
            for y, row in enumerate(data):
                for x, tile in enumerate(row):
                    if 0 <= tile < len(img_list):
                        img = img_list[tile]
                        img_rect = img.get_rect()
                        img_rect.x = x * tile_size
                        img_rect.y = y * tile_size
                        tile_data = (img, img_rect)
                        self.tile_list.append(tile_data)

        def draw(self, screen_scroll):
            for tile in self.tile_list:
                tile[1][0] += screen_scroll
                screen.blit(tile[0], tile[1])

        def get_tile_type(self, x, y):
            if 0 <= y < len(self.tile_data) and 0 <= x < len(self.tile_data[0]):
                return self.tile_data[y][x]
            else:
                return None

        def is_solid(self, x, y):
            return (x, y) in self.solid_tiles

        def make_tile_solid(self, x, y):
            self.solid_tiles.add((x, y))

    world_data = []
    for row in range(rows):
        r = [-1] * cols
        world_data.append(r)

    with open(f'level{level}_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)
    world = World(world_data)

    run = True
    while run:
        screen.blit(BG, (0, 0))
        screen.blit(gate1, (gate_x, gate_y))
        world.draw(screen_scroll)

        draw_text("HEALTH: ", game_font, GREEN, 10, 20)
        draw_text("MYR:", game_font, GOLD, 10, 50)

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                current_state = False
                exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if icon_rect.collidepoint(mouse_pos):
                    if music_playing:
                        pygame.mixer.music.pause()
                        current_icon = icon_pause
                    else:
                        pygame.mixer.music.unpause()
                        current_icon = icon_play
                    music_playing = not music_playing
                else:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    arm_end_x = rect.centerx + ((arm_image.get_width() // 2 -30  if moving_right else -arm_image.get_width() // 2+25))  
                    arm_end_y = (rect.centery - 15) 

                    dx = mouse_x - arm_end_x
                    dy = mouse_y - arm_end_y
                    angle = math.atan2(dy, dx)

                    bullet_direction = "right" if moving_right else "left"

                    # Adjust bullet direction for left movement
                    if bullet_direction == "left":
                        angle += math.pi  # Add 180 degrees to the angle

                    bullet = Bullet(arm_end_x, arm_end_y, bullet_direction, angle)
                    bullets.add(bullet)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    is_walking = True
                    moving_right = True
                    current_image = standing_image
                elif event.key == pygame.K_a:
                    is_walking = True
                    moving_right = False
                    current_image = flipped_standing_image
                elif event.key == pygame.K_w:
                    if not is_jumping:
                        is_jumping = True
                        current_image = standing_image if moving_right else flipped_standing_image
                        jump_speed = JUMP_HEIGHT
                elif event.key == pygame.K_s:
                    is_ducking = True
                    is_walking = False
                    current_image = ducking_image if moving_right else flipped_ducking_image
                    rect.height = ducking_image.get_height()
                    rect.y = ground_y - rect.height

                if event.key == pygame.K_s:  # Open shop on 's'
                    pygame.mouse.set_visible(True)
                if event.key == pygame.K_l:  # Load items on 'l'
                    pass
            
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_d, pygame.K_a):
                    is_walking = False
                    if is_ducking:
                        current_image = ducking_image if moving_right else flipped_ducking_image
                    else:
                        current_image = standing_image if moving_right else flipped_standing_image
                elif event.key == pygame.K_s:
                    is_ducking = False
                    current_image = standing_image if moving_right else flipped_standing_image
                    rect.height = standing_image.get_height()
                    rect.y = ground_y - rect.height

        if is_walking:
            now = pygame.time.get_ticks()
            if now - walking_timer > WALKING_SPEED:
                walking_timer = now
                walking_index = (walking_index + 1) % len(walking_images)
                current_image = walking_images[walking_index] if moving_right else flipped_walking_images[walking_index]

            if moving_right:
                rect.x += MOVE_SPEED
                if rect.right > WIDTH:
                    rect.right = WIDTH
            else:
                rect.x -= MOVE_SPEED
                if rect.left < 0:
                    rect.left = 0

        if is_jumping:
            rect.y += jump_speed
            jump_speed += GRAVITY

            if rect.bottom >= ground_y:
                rect.bottom = ground_y
                is_jumping = False
                jump_speed = 0
                check_tile_solidification()

            for tile in world.tile_list:
                img, tile_rect = tile
                if rect.colliderect(tile_rect) and rect.y < tile_rect.y:
                    rect.bottom = tile_rect.top
                    is_jumping = False
                    jump_speed = 0
                    check_tile_solidification() 
        
        
        if rect.colliderect(gate_rect):
            pygame.mouse.set_visible(True)
             
        update_player_movement()
        enemies.update()
        bullets.update()

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Adjust arm based on direction
        arm_center_x = rect.centerx
        arm_center_y = rect.centery
        dx = mouse_x - arm_center_x
        dy = mouse_y - arm_center_y

        if moving_right:
            angle = math.degrees(math.atan2(dy, dx))
            arm_image_to_draw = arm_image
            arm_x = rect.centerx + (arm_image.get_width() // 2) - 35  # Adjust for right
            arm_y = rect.centery - (arm_image.get_height() // 2) - 10
        else:
            angle = math.degrees(math.atan2(-dy, -dx))
            arm_image_to_draw = flipped_arm_image
            arm_x = rect.centerx - (arm_image.get_width() // 2) + 30  # Adjust for left
            arm_y = rect.centery - (arm_image.get_height() // 2) - 10

        # Rotate arm image
        rotated_arm_image = pygame.transform.rotate(arm_image_to_draw, -angle)
        arm_rect = rotated_arm_image.get_rect(center=(arm_x, arm_y))

        #screen.fill(BLUE)

        mouse_pos = pygame.mouse.get_pos()
        crosshair_rect = crosshair_image.get_rect(center=mouse_pos)
        screen.blit(crosshair_image, crosshair_rect.topleft)

        screen.blit(current_image, rect)
        screen.blit(rotated_arm_image, arm_rect.topleft)

        for bullet in bullets:
            screen.blit(bullet.image, bullet.rect)
            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect):
                    print("Hit!")
                    bullet.kill()
                    enemy.kill()
                    break

        for enemy in enemies:
            screen.blit(enemy.image, enemy.rect)

        draw_icon(current_icon, icon_rect)

        pygame.display.update()
        clock.tick(60)
    current_state = MAIN_MENU
