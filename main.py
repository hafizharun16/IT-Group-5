import pygame

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 675

screen = pygame.display.set_mode((WINDOW_WIDTH , WINDOW_HEIGHT))
pygame.display.set_caption("Captain Invader")

#images
main_img = pygame.image.load("mainimg.jpg")

#main menu
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))



run = True
while run:

    screen.blit(main_img, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

    pygame.display.update()
