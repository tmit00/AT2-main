## MENU
 
import pygame
from assets import GAME_ASSETS
 
class MainMenu:
    def __init__(self, window):
        self.window = window
        self.font = pygame.font.Font(None, 36)  # Specify the font size and style
        self.menu_buttons = {
            "Start Game": pygame.image.load(GAME_ASSETS['start_button']).convert_alpha(),
            "Settings": pygame.image.load(GAME_ASSETS['button_options']).convert_alpha(),
            "Exit": pygame.image.load(GAME_ASSETS['button_quit']).convert_alpha()
        }
        self.menu_buttons2 = self.setup_menu_buttons()
        self.background_image = pygame.image.load(GAME_ASSETS['main_menu_background'])  # Load the background image
        # Scale the background image to match the window size
        self.scaled_background = pygame.transform.scale(self.background_image, (self.window.get_width(), self.window.get_height()))
 
    def setup_menu_buttons(self):
        buttons = {}
        total_spacing = 10  # spacing between buttons and edges
        num_buttons = len(self.menu_buttons)
        window_width = self.window.get_width()
        window_height = self.window.get_height()
        lower_third = (2 * window_height) // 3.8
 
        button_heights = []
        for option, image in self.menu_buttons.items():
            if option == "Start Game":
                scaled_image = pygame.transform.scale(image, (int(image.get_width()* 0.25), int(image.get_height() * 0.25)))
                button_heights.append(scaled_image.get_height())
            else:
                scaled_image = pygame.transform.scale(image, (int(image.get_width()* 0.7), int(image.get_height() * 0.7)))
                button_heights.append(scaled_image.get_height())
 
       
        total_button_height = sum(button_heights) + total_spacing * (num_buttons - 1)
 
        y = lower_third + (window_height - lower_third - total_button_height) // 2
 
        for option, image in self.menu_buttons.items():
            if option == "Start Game":
                button_width = int(image.get_width() * 0.25)
                button_height = int(image.get_height() * 0.25)
                scaled_image = pygame.transform.scale(image, (button_width, button_height))
            else:
                button_width = int(image.get_width() * 0.7)
                button_height = int(image.get_height() * 0.7)
                scaled_image = pygame.transform.scale(image, (button_width, button_height))
           
            x = (window_width - button_width) // 2
 
            buttons[option] = (scaled_image, pygame.Rect(x, y, button_width, button_height))
            y += button_height + total_spacing
 
        return buttons
 
    def run(self):
        """Handles the display and interaction logic for the main menu."""
        running = True
        while running:
            # Blit the scaled background image to fill the entire window
            self.window.blit(self.scaled_background, (0, 0))
            for option, (image, rect) in self.menu_buttons2.items():
                self.window.blit(image, rect)
 
            pygame.display.flip()  # Update the display with the new frame
 
            # Event handling in the menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'  # Return 'quit' if the window is closed
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for option, (image, rect) in self.menu_buttons2.items():
                        if rect.collidepoint(event.pos):
                            return option
 
        return 'quit'  # Default return value if the loop ends