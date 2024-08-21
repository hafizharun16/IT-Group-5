import pygame

pygame.init()

WIDTH = 900
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

background_img = pygame.image.load("Pic/background0.jpg")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
AQUA=(51,255,255)

title_font = pygame.font.Font('Font/tittle.ttf', 30)
title_font2 = pygame.font.Font('Font/tittle.ttf', 50)
title_text = title_font2.render('WELCOME TO CAPTAIN INVADER', True, WHITE)
text_rect = title_text.get_rect(center=(WIDTH // 2, 120))

button_width = 150
button_height = 40
buttons = {
    'START': pygame.Rect(((button_width) //2) + 10 , (HEIGHT - button_height + 50) // 2 - 65, button_width, button_height),
    'CONTROL': pygame.Rect(((button_width) //2) + 10 , (HEIGHT - button_height + 50) // 2 + 10, button_width, button_height),
    'OPTION': pygame.Rect(((button_width) //2) + 10 , (HEIGHT - button_height + 50) // 2 + 85, button_width, button_height),
    'SHOP': pygame.Rect((WIDTH-button_width*2), (HEIGHT - button_height + 50) // 2 -65, button_width, button_height),
    'QUIT': pygame.Rect((WIDTH-button_width*2), (HEIGHT - button_height + 50) // 2 + 10, button_width, button_height)
}

pygame.mixer.music.load('music/spaceman.mp3')
pygame.mixer.music.play(-1)
icon_play = pygame.image.load('Pic/musicOn.png')
icon_play = pygame.transform.scale(icon_play, (50, 50)) 
icon_pause = pygame.image.load('Pic/musicOff.png')
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

while running:
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
                        print("Start button clicked!")    
                    elif button_text == 'OPTION':
                        print("Options button clicked!")
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
