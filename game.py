# GAME.PY

import pygame
from menu import MainMenu
from character_select import CharacterSelect
from character import Character
from settings import Settings
from map import Map
from done import Done
from assets import load_assets, GAME_ASSETS

class Game:
    def __init__(self):
        pygame.init()
        load_assets()  # load the game image assets
        self.window = pygame.display.set_mode((1050, 600))
        self.clock = pygame.time.Clock()
        self.menu = MainMenu(self.window)  # Create an instance of the MainMenu class
        self.character_select = CharacterSelect(self.window)  # Create an instance of the CharacterSelect class
        self.settings = Settings(self.window)
        self.game_map = Map(self.window)  # Create an instance of the Map class
        self.state = 'menu'  # Set the initial state to 'menu'
        self.current_character = None  # To store the chosen character

    def run(self):
        while True:
            if self.state == 'menu':  # If the state is 'menu'
                result = self.menu.run()  # Run the menu and get the result
                if result == 'Start Game':  # If the result is 'Start Game'
                    self.state = 'character_select'  # Change the state to 'character_select'
                elif result == 'Settings':  # If the result is 'Settings'
                    self.state = 'settings'  # Change the state to 'settings'
                elif result == 'Exit':  # If the result is 'Exit'
                    pygame.quit()  # Quit pygame
                    return  # Exit the run method

            elif self.state == 'character_select':  # If the state is 'character_select'
                selected_character = self.character_select.run()  # Run the character select screen and get the selected character
                if selected_character == 'back':  # If the selected character is 'back'
                    self.state = 'menu'  # Change the state to 'menu'
                elif selected_character:  # If a character is selected
                    self.current_character = selected_character  # Set the current character to the selected character
                    self.game_map.load_player(selected_character)  # Load the selected character into the game map
                    self.state = 'game_map'  # Change the state to 'game_map'

            elif self.state == 'game_map':  # If the state is 'game_map'
                result = self.game_map.handle_events()  # Handle events in the game map
                if result == 'quit':
                    pygame.quit()
                    return
                self.game_map.update()  # Update game logic
                if self.game_map.game_over:  # Check if the game is over
                    print("Game Over")
                    self.state = 'done'
                    self.done_screen = Done(self.window, self.game_map.high_score)  # Return to home screen if player dies
                self.game_map.draw(self.current_character)  # Draw the game map

            elif self.state == "settings":
                settings = self.settings.run()
                if settings == "back":
                    self.state = "menu"

            elif self.state == "done":
                done_result = self.done_screen.run()  # Run the done screen
                if done_result == 'quit':
                    pygame.quit()
                    return

            for event in pygame.event.get():  # Iterate over the events in the event queue
                if event.type == pygame.QUIT:  # If the event type is QUIT
                    pygame.quit()  # Quit pygame
                    return  # Exit the run method

            self.clock.tick(60)  # Ensure the game runs at 60 frames per second

if __name__ == "__main__":
    game = Game()  # Create an instance of the Game class
    game.run()  # Run the game
