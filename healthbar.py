## HEALTHBAR
 
import pygame
 
class HealthBar:
    def __init__(self, window, x, y, width=100, height=10):
        """
        Initialize the HealthBar class.
 
        Args:
            window (pygame.Surface): The game window surface.
            x (int): The x-coordinate of the health bar.
            y (int): The y-coordinate of the health bar.
            width (int): The width of the health bar. Default is 100.
            height (int): The height of the health bar. Default is 10.
        """
        self.window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
 
    def draw(self, current_hp, max_hp):
        """
        Draw the health bar on the screen.
 
        Args:
            current_hp (int): The current health points of the character.
            max_hp (int): The maximum health points of the character.
        """
        # Calculate health percentage
        health_percentage = current_hp / max_hp
        # Calculate the width of the current health bar based on the health percentage
        current_health_bar_width = self.width * health_percentage
        # Define the health bar rectangles
        health_bar_background = pygame.Rect(self.x, self.y, self.width, self.height)
        current_health_bar = pygame.Rect(self.x, self.y, current_health_bar_width, self.height)
        # Draw the health bar background (in red)
        pygame.draw.rect(self.window, (255, 0, 0), health_bar_background)
        # Draw the current health bar (in green)
        pygame.draw.rect(self.window, (0, 255, 0), current_health_bar)