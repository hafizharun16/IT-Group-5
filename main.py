import pygame

pygame.init()

WIDTH = 1100
HEIGHT = 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")
clock = pygame.time.Clock()
running = True

#variable
screen_black = False

# images
background_img = pygame.image.load("background0.jpg")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
AQUA = (51, 255, 255)

# font
title_font = pygame.font.Font('tittle.ttf', 30)
title_font2 = pygame.font.Font('tittle.ttf', 50)
title_text = title_font2.render('CAPTAIN INVADER', True, WHITE)
text_rect = title_text.get_rect(center=(WIDTH // 2, 120))

# buttons
button_width = 150
button_height = 40
buttons = {
    'START': pygame.Rect(((button_width) //2) + 10 , (HEIGHT - button_height + 50) // 2 - 65, button_width, button_height),
    'CONTROL': pygame.Rect(((button_width) //2) + 10 , (HEIGHT - button_height + 50) // 2 + 10, button_width, button_height),
    'SHOP': pygame.Rect(((button_width) //2) + 10 , (HEIGHT - button_height + 50) // 2 + 85, button_width, button_height),
    'CREDIT': pygame.Rect((WIDTH-button_width*2), (HEIGHT - button_height + 50) // 2 -65, button_width, button_height),
    'QUIT': pygame.Rect((WIDTH-button_width*2), (HEIGHT - button_height + 50) // 2 + 10, button_width, button_height)
}

# music
pygame.mixer.music.load('spaceman.mp3')
pygame.mixer.music.play(-1)
icon_play = pygame.image.load('musicOn.png')
icon_play = pygame.transform.scale(icon_play, (50, 50)) 
icon_pause = pygame.image.load('musicOff.png')
icon_pause = pygame.transform.scale(icon_pause, (50, 50)) 
icon_rect = pygame.Rect(WIDTH - 60, HEIGHT - 60, 50, 50) 
music_playing = True
current_icon = icon_play

def draw_button(button_rect, text, hover):
    button_color = (255, 153, 51) if hover else AQUA
    pygame.draw.rect(screen, button_color, button_rect)
    
    text_surface = title_font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

def draw_icon(icon_image, rect):
    screen.blit(icon_image, rect)

#Button Function
def start_game():
    screen.fill(BLACK)
    play_font = pygame.font.Font(None, 45)
    play_text = play_font.render("This is the PLAY screen.", True, WHITE)
    play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(play_text, play_rect)

    back_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 50, 150, 50)
    pygame.draw.rect(screen, AQUA, back_button)
    
    back_text = title_font.render("BACK", True, BLACK)
    back_text_rect = back_text.get_rect(center=back_button.center)
    screen.blit(back_text, back_text_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(pygame.mouse.get_pos()):
                    return
        clock.tick(60)

def open_control():
    screen.fill(BLACK)
    control_font = pygame.font.Font(None, 45)
    
    #Instruction
    control_text1 = control_font.render("D: Move to the right", True, WHITE)
    control_text2 = control_font.render("A: Move to the left", True, WHITE)
    control_text3 = control_font.render("W: Jump", True, WHITE)
    control_text4 = control_font.render("Mouse: To Aim", True, WHITE)
    control_text5 = control_font.render("Left Click: To Shoot", True, WHITE)
    
    control_texts = [control_text1, control_text2, control_text3, control_text4, control_text5]
    control_positions = [
        (WIDTH // 2, HEIGHT // 2 - 200),
        (WIDTH // 2, HEIGHT // 2 - 150),
        (WIDTH // 2, HEIGHT // 2 - 100),
        (WIDTH // 2, HEIGHT // 2 - 50),
        (WIDTH // 2, HEIGHT // 2)
    ]

    for i, text in enumerate(control_texts):
        text_rect = text.get_rect(center=control_positions[i])
        screen.blit(text, text_rect)

    #Back Button
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
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(pygame.mouse.get_pos()):
                    return  # Return to main menu

        clock.tick(60)

def open_shop():
    print("shop")

def open_credit():
    screen.fill(BLACK)
    credit_font = pygame.font.Font(None, 45)
    
    credit_text1 = credit_font.render("The Main Charcter: Hafiz", True, WHITE)
    credit_text2 = credit_font.render("The Author: Imran", True, WHITE)
    credit_text3 = credit_font.render("The Designer: John Doe", True, WHITE)
    credit_text4 = credit_font.render("The Final Boss: Mr.Willie", True, WHITE)

    credit_texts = [credit_text1, credit_text2, credit_text3, credit_text4]
    credit_positions = [
        (WIDTH // 2, HEIGHT // 2 - 150),
        (WIDTH // 2, HEIGHT // 2 - 100),
        (WIDTH // 2, HEIGHT // 2 - 50),
        (WIDTH // 2, HEIGHT // 2)
    ]
    
    for i, text in enumerate(credit_texts):
        text_rect = text.get_rect(center=credit_positions[i])
        screen.blit(text, text_rect)

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
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(pygame.mouse.get_pos()):
                    return
        clock.tick(60)

#Loop
while running:
    if screen_black:
        screen.fill((BLACK))
    else:
        screen.fill((30, 90, 200))
        screen.blit(background_img, (0, 0))
        screen.blit(title_text, text_rect)
    
    mouse_pos = pygame.mouse.get_pos() 
  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button_text, button_rect in buttons.items():
                if button_rect.collidepoint(mouse_pos):
                    if button_text == 'START':
                        start_game()
                    elif button_text == 'CONTROL':
                        open_control()
                    elif button_text == 'SHOP':
                        open_shop()
                    elif button_text == 'CREDIT':
                        open_credit()
                    elif button_text == 'QUIT':
                        running = False
            if icon_rect.collidepoint(mouse_pos):
                if music_playing:
                    pygame.mixer.music.pause()
                    current_icon = icon_pause
                else:
                    pygame.mixer.music.unpause()
                    current_icon = icon_play
                music_playing = not music_playing

    for button_text, button_rect in buttons.items():
        hover = button_rect.collidepoint(mouse_pos)
        draw_button(button_rect, button_text, hover)
    
    draw_icon(current_icon, icon_rect)
    
    pygame.display.update()
    clock.tick(60)  

pygame.quit()
