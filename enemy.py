## ENEMY
 
import pygame
import random
 
class Enemy:
    def __init__(self, image_paths, position, window):
        # Load the enemy image from the specified image path
        self.images = [pygame.image.load(image_path).convert_alpha() for image_path in image_paths]
       
        # Scale the enemy image to 0.75 times the original size
        self.images = [pygame.transform.scale(img, (int(img.get_width() * 2), int(img.get_height() * 2))) for img in self.images]
        self.images = [pygame.transform.flip(img, True, False) for img in self.images]
 
        # Set the initial position of the enemy
        self.position = position
       
        # Set the window where the enemy will be drawn
        self.window = window
       
        # Set the initial health of the enemy to 100
        self.health = 100
 
        self.animation_index = 0
        self.animation_counter = 0
        self.animation_speed = 80
 
    def take_damage(self, damage):
        # Reduce the enemy's health by the specified damage amount
        self.health -= damage
       
        # Return True if the enemy's health is less than or equal to 0, indicating that it is defeated
        return self.health <= 0
 
    def draw(self):
        # Adjust the position to ensure the image does not overflow the window boundaries
        adjusted_position = [
            max(0, min(self.window.get_width() - self.images[0].get_width(), self.position[0])),
            max(0, min(self.window.get_height() - self.images[0].get_height(), self.position[1]))
        ]
       
        # Handle enemy animation
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.animation_index = (self.animation_index + 1) % len(self.images)
       
        # Draw the current frame of the enemy image
        self.window.blit(self.images[self.animation_index], adjusted_position)