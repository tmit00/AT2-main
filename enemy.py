# ENEMY.PY

import pygame
import random
from healthbar import HealthBar

class Enemy:
    def __init__(self, image_paths, attack_image_paths, position, window):
        """
        Initialize the Enemy class.

        Args:
            image_paths (list): List of file paths for idle images.
            attack_image_paths (list): List of file paths for attack images.
            position (list): Initial position of the enemy [x, y].
            window (pygame.Surface): The game window surface.
        """
        # Load and scale the idle images
        self.images = [pygame.image.load(image_path).convert_alpha() for image_path in image_paths]
        self.images = [pygame.transform.scale(img, (int(img.get_width() * 2), int(img.get_height() * 2))) for img in self.images]
        self.images = [pygame.transform.flip(img, True, False) for img in self.images]

        # Load and scale the attack images
        self.attack_images = [pygame.image.load(image_path).convert_alpha() for image_path in attack_image_paths]
        self.attack_images = [pygame.transform.scale(img, (int(img.get_width() * 2), int(img.get_height() * 2))) for img in self.attack_images]
        self.attack_images = [pygame.transform.flip(img, True, False) for img in self.attack_images]

        # Set the initial position of the enemy
        self.position = position

        # Set the window where the enemy will be drawn
        self.window = window

        # Set the initial health of the enemy
        self.max_health = 100
        self.health = self.max_health

        # Initialize the health bar
        self.health_bar = HealthBar(window, window.get_width() - 320, window.get_height() - 150, "Enemy HP: ", width=100)

        # Initialize animation variables
        self.animation_index = 0
        self.animation_counter = 0
        self.animation_speed = 10
        self.current_images = self.images  # Start with idle images

    def take_damage(self, damage):
        """
        Reduce the enemy's health by the specified damage amount.

        Args:
            damage (int): Amount of damage to inflict.

        Returns:
            bool: True if the enemy's health is <= 0, indicating it is defeated.
        """
        self.health -= damage
        return self.health <= 0

    def start_attack_animation(self):
        """Switch to attack animation."""
        self.current_images = self.attack_images
        self.animation_index = 0
        self.animation_counter = 0

    def reset_idle_animation(self):
        """Switch back to idle animation."""
        self.current_images = self.images
        self.animation_index = 0
        self.animation_counter = 0

    def draw(self):
        """
        Draw the enemy on the screen.
        """
        # Adjust the position to ensure the image does not overflow the window boundaries
        adjusted_position = [
            max(0, min(self.window.get_width() - self.images[0].get_width(), self.position[0])),
            max(0, min(self.window.get_height() - self.images[0].get_height(), self.position[1]))
        ]

        # Handle enemy animation
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.animation_index = (self.animation_index + 1) % len(self.current_images)

        # Draw the current frame of the enemy image
        self.window.blit(self.current_images[self.animation_index], adjusted_position)
        self.health_bar.draw(self.health, self.max_health, type="Health")
