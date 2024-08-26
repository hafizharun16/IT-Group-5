import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("space cadaver")

# Colors
WHITE = (255, 255, 255)
FPS = 60
clock = pygame.time.Clock()

# Gravity
GRAVITY = 0.8

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))  
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.vel_y = 0
        self.jumping = False

        # Load and resize gun image (PNG)
        self.gun_image = pygame.image.load("gun2.png").convert_alpha()
        self.gun_image = pygame.transform.scale(self.gun_image, (50, 30))  

    def update(self):
        
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        
        if keys[pygame.K_SPACE] and not self.jumping:
            self.vel_y = -15
            self.jumping = True

        
        self.collide()

    def collide(self):
        hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for platform in hit_list:
            if self.vel_y > 0:  # Fall down
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.jumping = False

    def shoot(self, mouse_pos):
        # Calculate the vector length 
        direction = pygame.math.Vector2(mouse_pos) - self.rect.center
        direction = direction.normalize()

        # gun offsen
        gun_offset = pygame.math.Vector2(20, 0).rotate(-math.degrees(math.atan2(-direction.y, direction.x)))
        bullet_x = self.rect.centerx + gun_offset.x
        bullet_y = self.rect.centery + gun_offset.y

        
        bullet = Bullet(bullet_x, bullet_y, direction)
        all_sprites.add(bullet)
        bullets.add(bullet)

    def draw(self, surface):
        
        surface.blit(self.image, self.rect.topleft)

        
        mouse_pos = pygame.mouse.get_pos()
        direction = pygame.math.Vector2(mouse_pos) - self.rect.center
        angle = math.degrees(math.atan2(-direction.y, direction.x))

        
        rotated_gun = pygame.transform.rotate(self.gun_image, angle)
        gun_rect = rotated_gun.get_rect(center=self.rect.center + pygame.math.Vector2(20, 0).rotate(-angle))
        surface.blit(rotated_gun, gun_rect.topleft)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load("platform.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))  # Resize platform image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.image.load("projectile.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 10))  # Resize projectile image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 10
        self.direction = direction

    def update(self):
        
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

class Opponent(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("opponent.png").convert_alpha()  
        self.image = pygame.transform.scale(self.image, (70, 70))  
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def die(self):
        self.kill()  # Remove the opps


all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
bullets = pygame.sprite.Group()
opponents = pygame.sprite.Group()

# player
player = Player()
all_sprites.add(player)

# platforms
platform1 = Platform(100, 500, 200, 20)
platform2 = Platform(400, 400, 200, 20)
platforms.add(platform1, platform2)
all_sprites.add(platform1, platform2)

#  opponents
opponent1 = Opponent(300, 250)
opponent2 = Opponent(500, 150)
opponents.add(opponent1, opponent2)
all_sprites.add(opponent1, opponent2)

#  
crosshair_image = pygame.image.load("crosshair.png").convert_alpha()
crosshair_image = pygame.transform.scale(crosshair_image, (20, 20))  # Resize crosshair

# Main game 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Shooting
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                player.shoot(mouse_pos)

    # Update
    all_sprites.update()

    # Check for collisions between bullets and opponents
    for bullet in bullets:
        hits = pygame.sprite.spritecollide(bullet, opponents, False)
        for hit in hits:
            hit.die()
            bullet.kill()  # Remove the bullet

    # Draw
    screen.fill(WHITE)
    all_sprites.draw(screen)
    player.draw(screen)  # Draw the player with the gun

    # Draw the crosshair at the mouse position
    mouse_pos = pygame.mouse.get_pos()
    crosshair_rect = crosshair_image.get_rect(center=mouse_pos)
    screen.blit(crosshair_image, crosshair_rect.topleft)

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)


