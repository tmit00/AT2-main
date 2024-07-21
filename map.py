## MAP
 
import random
 
import pygame
from assets import GAME_ASSETS
from enemy import Enemy
from character import Character


class Map:
    def __init__(self, window):
        """
        Initialize the Map class.
 
        Args:
            window (pygame.Surface): The game window surface.
        """
        self.window = window
        self.map_image = pygame.image.load(GAME_ASSETS["background"]).convert_alpha()
        self.map_image = pygame.transform.scale(self.map_image, (self.window.get_width(), 400))
        self.panel_image = pygame.image.load(GAME_ASSETS["panel"]).convert_alpha()
        self.panel_image = pygame.transform.scale(self.panel_image, (self.window.get_width(), 200))
        self.animation_list = []
        self.player_images = {
            'Warrior': [pygame.image.load(GAME_ASSETS[f'warrior_idle_{i}']).convert_alpha() for i in range(1,7)],
            'Mage': [pygame.image.load(GAME_ASSETS[f'idle_wizard_{i}']).convert_alpha() for i in range(1, 7)],
            'Rogue': [pygame.image.load(GAME_ASSETS[f"rogue_idle_{i}"]).convert_alpha() for i in range(1, 6)]
        }
        self.player_type = None
        self.player_position = [0,0]
        self.mage_player_position = [90, 88]
        self.rogue_player_position = [90, 45]
        self.warrior_player_position = [90, 45]
        self.enemies = [
            Enemy([GAME_ASSETS[f"skeleton_idle_{i}"] for i in range(1, 8)], [self.window.get_width() - 90, 80], self.window)
        ]
        self.in_combat = False  # Ensure this attribute is defined in the constructor
        self.current_enemy = None
        self.blue_orb = None
        self.game_over = False
        self.paused = False
        self.pause_menu = {
            "Resume": pygame.image.load(GAME_ASSETS['button_resume']).convert_alpha(),
            "Quit": pygame.image.load(GAME_ASSETS['button_quit']).convert_alpha()
        }
        self.pause_menu_rects = self.create_pause_menu_rects()
        self.animation_index = 0
        self.animation_counter = 0
        self.animation_speed = 80
 
    def load_player(self, character_type):
        """
        Load the player character.
 
        Args:
            character_type (str): The type of character to load.
        """
        self.player_type = character_type
        self.player_images[character_type] = [pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                                              for img, scale in zip(self.player_images[character_type], [1.75] * len(self.player_images['Mage']) if character_type == "Mage" else
                                                                     [3] * len(self.player_images['Warrior']) if character_type == "Warrior" else
                                                                     [3] * len(self.player_images['Rogue']) if character_type == "Rogue" else [1])]
   
 
    def check_for_combat(self):
        """
        Check if the player is in combat with any enemy.
 
        Returns:
            bool: True if the player is in combat, False otherwise.
        """
        for enemy in self.enemies:
            if pygame.math.Vector2(enemy.position).distance_to(self.player_position) < 50:
                self.in_combat = True
                self.current_enemy = enemy
                return True
        return False
 
    def handle_combat(self):
        """
        Handle combat between the player and the current enemy.
        """
        if self.in_combat and self.current_enemy:
            player_damage = random.randint(5, 10)
            enemy_defeated = self.current_enemy.take_damage(player_damage)
            print(f"Player attacks! Deals {player_damage} damage to the enemy.")
            if enemy_defeated:
                print("Enemy defeated!")
                self.enemies.remove(self.current_enemy)
                self.in_combat = False
                self.current_enemy = None
                if not self.enemies:
                    self.spawn_blue_orb()
            else:
                enemy_damage = random.randint(5, 10)
                print(f"Enemy attacks back! Deals {enemy_damage} damage to the player.")
                # Assume player has a method to take damage
                # self.player.take_damage(enemy_damage)
 
    def spawn_blue_orb(self):
        """
        Spawn the blue orb in the center of the map.
        """
        self.blue_orb = pygame.image.load(GAME_ASSETS["blue_orb"]).convert_alpha()
        self.blue_orb = pygame.transform.scale(self.blue_orb, (50, 50))
        self.orb_position = [self.window.get_width() / 2 - 25, self.window.get_height() / 2 - 25]
 
    def check_orb_collision(self):
        """
        Check if the player has collided with the blue orb.
 
        Returns:
            bool: True if the player has collided with the blue orb, False otherwise.
        """
        if self.blue_orb and pygame.math.Vector2(self.orb_position).distance_to(self.player_position) < 25:
            self.game_over = True
            print("YOU WIN")  # This can be modified to a more visual display if needed.
            return True
        return False
 
    def handle_pause(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.pause_menu_rects["Resume"].collidepoint(event.pos):
                    self.paused = False
                elif self.pause_menu_rects["Quit"].collidepoint(event.pos):
                    return "quit"
        return None
           
 
    def handle_events(self):
        """
        Handle user input events.
       
        Returns:
            str: 'quit' if the game is over and should be exited, None otherwise.
        """
        if self.paused:
            if self.handle_pause() == "quit":
                return "quit"
            return None
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
       
        if self.game_over:
            return 'quit'  # Stop processing events if game is over
 
        if not self.in_combat:
            if self.check_for_combat():
                return
        self.handle_combat()
 
        if self.blue_orb and self.check_orb_collision():
            return 'quit'
 
    def draw(self, selected_character):
        """
        Draw the game objects on the window.
        """
        self.window.fill((0, 0, 0))
        self.window.blit(self.map_image, (0, 0))
        self.window.blit(self.panel_image, (0, 400))
       
        if selected_character == "Mage":
            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.animation_counter = 0
                self.animation_index = (self.animation_index + 1) % len(self.player_images["Mage"])
            self.window.blit(self.player_images["Mage"][self.animation_index], (self.mage_player_position[0], self.mage_player_position[1]))
        elif selected_character == "Warrior":
            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.animation_counter = 0
                self.animation_index = (self.animation_index + 1) % len(self.player_images["Warrior"])
            self.window.blit(self.player_images["Warrior"][self.animation_index], (self.warrior_player_position[0], self.warrior_player_position[1]))
        elif selected_character == "Rogue":
            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.animation_counter = 0
                self.animation_index = (self.animation_index + 1) % len(self.player_images["Rogue"])
            self.window.blit(self.player_images["Rogue"][self.animation_index], (self.rogue_player_position[0], self.rogue_player_position[1]))
       
       
        for enemy in self.enemies:
            enemy.draw()
        if self.blue_orb:
            self.window.blit(self.blue_orb, self.orb_position)
        if self.paused:
            self.draw_pause_menu()
        pygame.display.flip()
 
    def draw_pause_menu(self):
        for key, button in self.pause_menu.items():
            self.window.blit(button, self.pause_menu_rects[key].topleft)
        pygame.display.flip()
 
    def create_pause_menu_rects(self):
        pause_menu_rects = {}
        x = self.window.get_width() / 2
        y = self.window.get_height() / 2
        for key, button in self.pause_menu.items():
            pause_menu_rects[key] = button.get_rect(center=(x,y))
            y += 50
        return pause_menu_rects