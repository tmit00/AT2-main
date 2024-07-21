## SETTINGS
 
 
import pygame
from assets import GAME_ASSETS
 
# settings.py
 
class Settings:
    def __init__(self, window):
        self.window = window
        self.font = pygame.font.Font(None, 36)
        self.options = {
            "Volume": pygame.image.load(GAME_ASSETS['button_audio']).convert_alpha(),
            "Graphics": pygame.image.load(GAME_ASSETS['button_video']).convert_alpha()
        }
        self.option_buttons = self.setup_menu_buttons()
        self.background_image = pygame.image.load(GAME_ASSETS['main_menu_background_blur'])  # Load the background image
        # Scale the background image to match the window size
        self.scaled_background = pygame.transform.scale(self.background_image, (self.window.get_width(), self.window.get_height()))
        self.back_button = pygame.Rect(50, self.window.get_height() - 50 - 30, 100, 30)
 
    def setup_menu_buttons(self):
        buttons = {}
        total_spacing = 10  # spacing between buttons and edges
        num_buttons = len(self.options)
        window_width = self.window.get_width()
        window_height = self.window.get_height()
        lower_third = (2 * window_height) // 3.8
 
        button_heights = []
        for option, image in self.options.items():
            scaled_image = pygame.transform.scale(image, (int(image.get_width()* 0.7), int(image.get_height() * 0.7)))
            button_heights.append(scaled_image.get_height())
 
       
        total_button_height = sum(button_heights) + total_spacing * (num_buttons - 1)
 
        y = lower_third + (window_height - lower_third - total_button_height) // 2
 
        for option, image in self.options.items():
            button_width = int(image.get_width() * 0.7)
            button_height = int(image.get_height() * 0.7)
            scaled_image = pygame.transform.scale(image, (button_width, button_height))
           
            x = (window_width - button_width) // 2
 
            buttons[option] = (scaled_image, pygame.Rect(x, y, button_width, button_height))
            y += button_height + total_spacing
 
        return buttons
 
    def run(self):
        running = True
        while running:
            self.window.blit(self.scaled_background, (0, 0))
            for option, (image, rect) in self.option_buttons.items():
                self.window.blit(image, rect)
 
            pygame.draw.rect(self.window, (200, 200, 200), self.back_button)  # Draw a grey button
            back_text = self.font.render('Back', True, (0, 0, 0))
            text_rect = back_text.get_rect(center=self.back_button.center)
            self.window.blit(back_text, text_rect)
 
            pygame.display.flip()
 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.collidepoint(event.pos):
                        return 'back'
                    for option, (image, rect) in self.option_buttons.items():
                        if rect.collidepoint(event.pos):
                            print(f"Adjusting {option}")
        return None