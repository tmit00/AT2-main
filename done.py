# done.py

import pygame
from assets import GAME_ASSETS

class Done:
    def __init__(self, window, high_score):
        self.window = window
        self.font = pygame.font.Font(None, 36)  # Specify the font size and style
        self.background_image = pygame.image.load(GAME_ASSETS['main_menu_background_blur']).convert_alpha()  # Load the background image
        self.scaled_background = pygame.transform.scale(self.background_image, (self.window.get_width(), self.window.get_height()))

        self.high_score = high_score  # Store high score

        # Load quit button image
        self.quit_button_image = pygame.image.load(GAME_ASSETS['button_quit']).convert_alpha()
        self.quit_button_rect = self.quit_button_image.get_rect(center=(self.window.get_width() // 2, self.window.get_height() - 100))

    def run(self):
        running = True
        while running:
            self.window.blit(self.scaled_background, (0, 0))

            # Display the highscore text
            highscore_text = self.font.render(f"Highscore: {self.high_score}", True, (255, 255, 255))
            text_rect = highscore_text.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2 - 50))
            self.window.blit(highscore_text, text_rect)

            # Draw quit button
            self.window.blit(self.quit_button_image, self.quit_button_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return 'quit'  # Return 'quit' if the window is closed
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if self.quit_button_rect.collidepoint(event.pos):
                            return 'quit'  # Return 'quit' if quit button is clicked

        return 'quit'  # Default return value if the loop ends
