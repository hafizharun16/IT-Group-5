import pygame

pygame.init

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

IMAGE_SCALE = 0.15
BULLET_SCALE = 0.03
ENEMY_SCALE = 0.2  # Define this if you haven't

def load_and_scale_image(filename, scale_factor):
    image = pygame.image.load(filename).convert_alpha()
    width, height = image.get_size()
    new_size = (int(width * scale_factor), int(height * scale_factor))
    return pygame.transform.scale(image, new_size)

