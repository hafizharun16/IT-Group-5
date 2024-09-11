import pygame
from pygame.locals import *
import pickle

pygame.init()

screen_width = 1100
screen_height = 650

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Captain Invader')

BLACK = (0, 0, 0)
white = (255, 255, 255)
green = (144, 201, 120)
AQUA = (51, 255, 255)

#define game variables
tile_size = 50
title_font = pygame.font.Font('font/tittle.ttf', 30)

pygame.mixer.music.load('music/spaceman.mp3')
pygame.mixer.music.play(-1)
icon_play = pygame.image.load('pic/musicOn.png')
icon_play = pygame.transform.scale(icon_play, (50, 50)) 
icon_pause = pygame.image.load('pic/musicOff.png')
icon_pause = pygame.transform.scale(icon_pause, (50, 50)) 
icon_rect = pygame.Rect(screen_width - 70, 20, 50, 50) 
music_playing = True
current_icon = icon_play

def draw_icon(icon_image, rect):
    screen.blit(icon_image, rect)

#load images
BG = pygame.image.load('pic/gameimg.jpg')

def draw_grid():
	for line in range(0, 22):
		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
		pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))



class World():
	def __init__(self, data):
		self.tile_list = []

		#load images
		dirt_img = pygame.image.load('pic/dirt.png')
		stone_img = pygame.image.load('pic/stone.png')

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
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0], 
[0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[2, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0], 
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

world = World(world_data)

run = True
while run:

	screen.blit(BG, (0, 0))

	world.draw()

	mouse_pos = pygame.mouse.get_pos()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if icon_rect.collidepoint(mouse_pos):
				if music_playing:
					pygame.mixer.music.pause()
					current_icon = icon_pause
				else:
					pygame.mixer.music.unpause()
					current_icon = icon_play
				music_playing = not music_playing
    
	draw_icon(current_icon, icon_rect)

	pygame.display.update()

pygame.quit()