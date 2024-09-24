def start_game_2():

    #level_1 = level 1
    
    global current_state
    







    WIDTH = 1110
    HEIGHT = 660
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

    
    BLUEE = (0, 150, 225)
    BLACK = (0, 0, 0)
    white = (255, 255, 255)
    green = (144, 201, 120)
    AQUA = (51, 255, 255)

    gate = pygame.image.load("pic/gate1.png")
    gate1 = pygame.transform.scale(gate, (70, 100))
    gate_x, gate_y = WIDTH - 80, 1  
    gate_rect = pygame.Rect(gate_x +50 , gate_y, 70, 100)

    # Load and resize images
    def load_and_scale_image(filename, scale_factor):
        image = pygame.image.load(filename)
        width, height = image.get_size()
        new_size = (int(width * scale_factor), int(height * scale_factor))
        return pygame.transform.scale(image, new_size)

    def flip_images(images):
        """Flip images horizontally."""
        return [pygame.transform.flip(img, True, False) for img in images]

    # Load images
    standing_image = load_and_scale_image('Store/H1S1/H1S1A.png', IMAGE_SCALE)
    walking_images = [
        load_and_scale_image('Store/H1S1/H1S1A.png', IMAGE_SCALE),
        load_and_scale_image('Store/H1S1/H1S1A.png', IMAGE_SCALE),
        load_and_scale_image('Store/H1S1/H1S1B.png', IMAGE_SCALE),
        load_and_scale_image('Store/H1S1/H1S1C.png', IMAGE_SCALE),
        load_and_scale_image('Store/H1S1/H1S1D.png', IMAGE_SCALE)
    ]
    # Load ducking image
    ducking_image = load_and_scale_image('Store/H1S1/H1S1A.png', IMAGE_SCALE)

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
    tile_size = 30
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

    #load images
    BG = pygame.image.load('back2.png')
    BG = pygame.transform.scale(BG, (WIDTH,HEIGHT))


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





    class World():
        def __init__(self, data):
            self.tile_list = []
            self.solid_tiles = set()
            self.tile_data = data  # Store the tile data for retrieval
            
            # Load images
            dirt_img = pygame.image.load('dirt.png')
            stone_img = pygame.image.load('Stone.png')

            row_count = 0
            for row in data:
                col_count = 0
                for tile in row:
                    if tile == 1:
                        img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    elif tile == 2:
                        img = pygame.transform.scale(stone_img, (tile_size, tile_size))
                    else:
                        img = None
                    
                    if img:
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

        def get_tile_type(self, x, y):
            if 0 <= y < len(self.tile_data) and 0 <= x < len(self.tile_data[0]):
                return self.tile_data[y][x]
            return 0  # Default to empty tile if out of bounds

        def is_solid(self, x, y):
            for img, rect in self.tile_list:
                if rect.collidepoint(x, y):
                    return (rect.x, rect.y) in self.solid_tiles
            return False

        def make_tile_solid(self, x, y):
            for img, rect in self.tile_list:
                if rect.collidepoint(x, y):
                    self.solid_tiles.add((rect.x, rect.y))

        

        

    world_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 1, 1, 1, 1, 1], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]

    world = World(world_data)

    
    while current_state == PLAYING:
        screen.blit(BG, (0, 0))
        screen.blit(gate1, (gate_x, gate_y))

        world.draw()
        title_font = pygame.font.Font('font/tittle.ttf', 20)
        mouse_pos = pygame.mouse.get_pos()
        back_button = pygame.Rect( 20, 20, 70, 30)
        pygame.draw.rect(screen, AQUA, back_button)
        back_text = title_font.render("BACK", True, BLACK)
        back_text_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                current_state = False
                exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(pygame.mouse.get_pos()):
                    current_state = MAIN_MENU
                    pygame.mouse.set_visible(True)
                    pass
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
                if event.key == pygame.K_RIGHT:
                    is_walking = True
                    moving_right = True
                    current_image = standing_image
                elif event.key == pygame.K_LEFT:
                    is_walking = True
                    moving_right = False
                    current_image = flipped_standing_image
                elif event.key == pygame.K_UP:
                    if not is_jumping:
                        is_jumping = True
                        current_image = standing_image if moving_right else flipped_standing_image
                        jump_speed = JUMP_HEIGHT
                elif event.key == pygame.K_DOWN:
                    is_ducking = True
                    is_walking = False
                    current_image = ducking_image if moving_right else flipped_ducking_image
                    rect.height = ducking_image.get_height()
                    rect.y = ground_y - rect.height

                if event.key == pygame.K_s:  # Open shop on 's'
                    pygame.mouse.set_visible(True)
                    open_shop()
                if event.key == pygame.K_l:  # Load items on 'l'
                    load_items_in_level()
            
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_RIGHT, pygame.K_LEFT):
                    is_walking = False
                    if is_ducking:
                        current_image = ducking_image if moving_right else flipped_ducking_image
                    else:
                        current_image = standing_image if moving_right else flipped_standing_image
                elif event.key == pygame.K_DOWN:
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
            current_state = open_shop()
             



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


def open_shop():
    screen.blit(Shop_bg, (0, 0))
    foreground = pygame.image.load('light.jpg').convert_alpha()
    foreground_width, foreground_height = 920, 570  
    foreground = pygame.transform.scale(foreground, (foreground_width, foreground_height))
    foreground.set_alpha(100)
    screen.blit(foreground, (100, 20))

    YELLOW = (255, 255, 0)
    BLUE =(61, 233, 95)
    border_alpha = 100
    border_color = (*BLACK, border_alpha)
    rect_width, rect_height = 160, 190
    border_thickness = 5
    
    #title_font = pygame.font.Font('font/tittle.ttf', 30)

    # Draw shop balance
    shop_font = pygame.font.Font(None, 40)
    shop_text = shop_font.render("150 MYR", True, BLACK)
    shop_rect = shop_text.get_rect(center=(WIDTH - 140, HEIGHT - 610))
    screen.blit(shop_text, shop_rect)

    # Draw headers
    helmet_font = pygame.font.Font('font/tittle.ttf', 30)
    helmet_text = helmet_font.render("HELMETS", True, BLACK)
    helmet_rect = helmet_text.get_rect(center=(WIDTH // 2 +20, HEIGHT - 610))
    screen.blit(helmet_text, helmet_rect)

    suit_font = pygame.font.Font('font/tittle.ttf', 31)
    suit_text = suit_font.render("SUITS", True, BLACK)
    suit_rect = suit_text.get_rect(center=(WIDTH // 2+10, HEIGHT - 320))
    screen.blit(suit_text, suit_rect)

    # Define items
    helmets = [
        {'name': '- DX200 -', 'description': '- 10% DMG -', 'price': '- FREE -', 'image': 'Inventory/helmet1.png', 'pos': (180, 80)},
        {'name': '- GX500 -', 'description': '- 50% DMG -', 'price': '- 200MYR -', 'image': 'Inventory/helmet2.png', 'pos': (500, 80)},
        {'name': '- GXR7707 -', 'description': '- 90% DMG -', 'price': '- 500MYR -', 'image': 'Inventory/helmet3.png', 'pos': (800, 80)}
    ]

    suits = [
        {'name': '- MD1485 -', 'description': '- 10% DMG -= -', 'price': '- FREE -', 'image': 'Inventory/suit1.png', 'pos': (170, 355)},
        {'name': '- PX13 -', 'description': '- 40% DMG -= -', 'price': '- 300MYR -', 'image': 'Inventory/suit2.png', 'pos': (490, 355)},
        {'name': '- CR2020 -', 'description': '- 80% DMG -= -', 'price': '- 600MYR -', 'image': 'Inventory/suit3.png', 'pos': (790, 355)}
    ]

    # Load and resize images
    def load_and_resize_image(image_path, size):
        try:
            image = pygame.image.load(image_path)
            return pygame.transform.scale(image, size)
        except pygame.error as e:
            print(f"Unable to load or resize image at {image_path}. Error: {e}")
            return None

    desired_size = (100, 100)
    desired_size2 = (70, 100)   
    helmet_images = [load_and_resize_image(item['image'], desired_size) for item in helmets]
    suit_images = [load_and_resize_image(item['image'], desired_size2) for item in suits]

    # Draw items
    def draw_items(items, images, y_offset):
        for i, item in enumerate(items):
            name_text = pygame.font.Font(None, 31).render(item['name'], True, BLACK)
            description_text = pygame.font.Font(None, 28).render(item['description'], True, BLACK)
            price_text = pygame.font.Font(None, 31).render(item['price'], True, BLACK)

            # Item position
            x, y = item['pos']
            screen.blit(images[i], (x, y))
            screen.blit(name_text, (x + 10, y + 110))
            screen.blit(description_text, (x + 10, y + 130))
            screen.blit(price_text, (x + 10, y + 150))

    draw_items(helmets, helmet_images, 80)
    draw_items(suits, suit_images, 370)

    # Define buttons
    buttons = {
        'USING': pygame.Rect(190, HEIGHT - 380, 110, 30),
        'BUY1': pygame.Rect(520, HEIGHT - 380, 100, 30),
        'BUY2': pygame.Rect(820, HEIGHT - 380, 100, 30),
        'USING2': pygame.Rect(190, HEIGHT - 100, 120, 30),
        'BUY3': pygame.Rect(510, HEIGHT - 100, 100, 30),
        'BUY4': pygame.Rect(810, HEIGHT - 100, 100, 30),
        'BACK': pygame.Rect(20, HEIGHT // 2 + 280, 100, 30)
    }

    def draw_button(button_rect, text, hover):
        button_color = BLUE if hover else AQUA
        pygame.draw.rect(screen, button_color, button_rect)
        text_surface = title_font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

    def draw_border(surface, color, rect_width, rect_height, border_thickness, position):
        border_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
        pygame.draw.rect(border_surface, color, (0, 0, rect_width, rect_height), border_thickness)
        surface.blit(border_surface, position)

    border_positions = [(163, 70), (485, 70), (790, 70), (163, 350), (485, 350), (790, 350)]
    for position in border_positions:
        draw_border(screen, border_color, rect_width, rect_height, border_thickness, position)

    pygame.display.update()

    while True:
        

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button_text, button_rect in buttons.items():
                    if button_rect.collidepoint(mouse_pos):
                        if button_text == 'USING':
                            player_inventory['helmet'] = 'helmet1'
                            print("Helmet 1 equipped")
                        elif button_text == 'BUY1':
                            player_inventory['helmet'] = 'helmet2'
                            print("Helmet 2 purchased")
                        elif button_text == 'BUY2':
                            player_inventory['helmet'] = 'helmet3'
                            print("Helmet 2 purchased")
                        elif button_text == 'USING2':
                            player_inventory['suit'] = 'suit1'
                            print("Suit 1 equipped")
                        elif button_text == 'BUY3':
                            player_inventory['suit'] = 'suit2'
                            print("Suit 2 purchased")
                        elif button_text == 'BUY4':
                            player_inventory['suit'] = 'suit3'
                            print("Suit 2 purchased")
                        elif button_text == 'BACK':
                            return

        for button_text, button_rect in buttons.items():
            hover = button_rect.collidepoint(mouse_pos)
            draw_button(button_rect, button_text, hover)

        pygame.display.update()
        clock.tick(60)