import pygame

pygame.init

class Inventory:
    def __init__(self):
        self.items = []  
        self.money = 0   

    def add_item(self, item):
        self.items.append(item)  
        print(f"Added {item} to inventory.")

    def save_to_file(self, filename):
        try:
            with open(filename, 'w') as f:
                for item in self.items:
                    f.write(f"{item}\n")  
                f.write(f"Money: {self.money}\n") 
        except Exception as e:
            print(f"Error saving inventory: {e}")

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
                self.items = [line.strip() for line in lines if not line.startswith("Money")]
                
                for line in lines:
                    if line.startswith("Money"):
                        parts = line.strip().split(":")
                        if len(parts) > 1:
                            self.money = int(parts[1].strip())
                        else:
                            print("Money format is incorrect. Defaulting to 0.")
                            self.money = 0  
                        break  

        except FileNotFoundError:
            print("Inventory file not found, starting with an empty inventory.")
        except ValueError:
            print("Error converting money to integer. Defaulting to 0.")
            self.money = 0 
    def update_money(self, amount):
        """Update the player's money after a purchase or reward."""
        self.money += amount  
        print(f"Money updated: {self.money}")

    def display_inventory(self):
        """Display the current inventory and money."""
        print("Inventory:", self.items)
        print("Money:", self.money)


IMAGE_SCALE = 0.15
BULLET_SCALE = 0.03
ENEMY_SCALE = 0.2  # Define this if you haven't

def load_and_scale_image(filename, scale_factor):
    image = pygame.image.load(filename).convert_alpha()
    width, height = image.get_size()
    new_size = (int(width * scale_factor), int(height * scale_factor))
    return pygame.transform.scale(image, new_size)


