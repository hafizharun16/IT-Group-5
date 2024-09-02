import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 1000
HEIGHT = 566.93
WHITE = (0, 150, 225)
FPS = 60
MOVE_SPEED = 3
WALKING_SPEED = 80
IMAGE_SCALE = 0.15
JUMP_HEIGHT = -10
GRAVITY = 0.5

# Create the screen object
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Captain Vader')

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
standing_image = load_and_scale_image('H1S1/Normal.png', IMAGE_SCALE)
walking_images = [
    load_and_scale_image('H1S1/Normal.png', IMAGE_SCALE),
    load_and_scale_image('H1S1/H1S1A.png', IMAGE_SCALE),
    load_and_scale_image('H1S1/H1S1B.png', IMAGE_SCALE),
    load_and_scale_image('H1S1/H1S1C.png', IMAGE_SCALE),
    load_and_scale_image('H1S1/H1S1D.png', IMAGE_SCALE)
]

# Load ducking image
ducking_image = load_and_scale_image('H1S1/Dduckka.png', IMAGE_SCALE)

# Flip images for left movement
flipped_standing_image = pygame.transform.flip(standing_image, True, False)
flipped_walking_images = flip_images(walking_images)
flipped_ducking_image = pygame.transform.flip(ducking_image, True, False)

# Get image rect
rect = standing_image.get_rect(center=(WIDTH // 6, HEIGHT // 1.5))

# Animation control
current_image = standing_image
walking_index = 0
walking_timer = pygame.time.get_ticks()
is_walking = False
moving_right = True
is_jumping = True
is_ducking = False
jump_speed = 0
ground_y = HEIGHT // 1.5

# Set up the clock
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                is_walking = True
                moving_right = True
                current_image = standing_image 
            elif event.key == pygame.K_LEFT:
                is_walking = True
                moving_right = False
                current_image = flipped_standing_image #if not is_ducking else flipped_ducking_image
            elif event.key == pygame.K_UP:
                if is_jumping:
                    current_image = standing_image 
                    
                elif not is_jumping:
                    is_jumping = True
                    current_image = standing_image if moving_right else flipped_standing_image
                    jump_speed = JUMP_HEIGHT
            elif event.key == pygame.K_DOWN:
                is_ducking = True
                is_walking = False
                current_image = ducking_image if moving_right else flipped_ducking_image
                rect.height = ducking_image.get_height()  # Adjust the rect height for ducking
                rect.y = ground_y - rect.height  # Move rect down to keep character on the ground

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_RIGHT, pygame.K_LEFT):
                is_walking = False
                if is_ducking:
                    current_image = ducking_image if moving_right else flipped_ducking_image
                    
                else:
                    current_image = standing_image if moving_right else flipped_standing_image

            elif event.key == pygame.K_DOWN:
                is_ducking = False
                current_image = standing_image if moving_right else flipped_standing_image
                rect.height = standing_image.get_height()  # Reset the rect height
                rect.y = ground_y - rect.height   # Move rect back to original position

    # Update animation if walking
    if is_walking:
        now = pygame.time.get_ticks()
        if now - walking_timer > WALKING_SPEED:
            walking_timer = now
            walking_index = (walking_index + 1) % len(walking_images)
            current_image = walking_images[walking_index] if moving_right else flipped_walking_images[walking_index]

        # Move image
        if moving_right:
            rect.x += MOVE_SPEED
            if rect.right > WIDTH:
                rect.right = WIDTH
        else:
            rect.x -= MOVE_SPEED
            if rect.left < 0:
                rect.left = 0

    # Update jumping
    if is_jumping:
        rect.y += jump_speed
        jump_speed += GRAVITY
        
        # Check if the image has landed
        if rect.bottom >= ground_y:
            rect.bottom = ground_y
            is_jumping = False
            jump_speed = 0

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the current image
    screen.blit(current_image, rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
