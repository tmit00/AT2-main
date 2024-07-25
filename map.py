# MAP.PY

import random
import pygame
from assets import GAME_ASSETS
from enemy import Enemy
from character import Character
from warrior import Warrior
from mage import Mage
from rogue import Rogue
from done import Done

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
        self.player_images = {
            'Warrior': [pygame.image.load(GAME_ASSETS[f'warrior_idle_{i}']).convert_alpha() for i in range(1, 7)],
            'Mage': [pygame.image.load(GAME_ASSETS[f'idle_wizard_{i}']).convert_alpha() for i in range(1, 7)],
            'Rogue': [pygame.image.load(GAME_ASSETS[f"rogue_idle_{i}"]).convert_alpha() for i in range(1, 6)]
        }
        self.player_attack_animations = {
            'Warrior': {
                'attack_1': [pygame.image.load(GAME_ASSETS[f'warrior_attack_1_{i}']).convert_alpha() for i in range(1, 5)],
                'attack_2': [pygame.image.load(GAME_ASSETS[f'warrior_attack_2_{i}']).convert_alpha() for i in range(1, 5)],
                'attack_3': [pygame.image.load(GAME_ASSETS[f'warrior_attack_3_{i}']).convert_alpha() for i in range(1, 5)]
            },
            'Mage': {
                'attack_1': [pygame.image.load(GAME_ASSETS[f'wizard_attack_1_{i}']).convert_alpha() for i in range(1, 5)],
                'attack_2': [pygame.image.load(GAME_ASSETS[f'wizard_attack_2_{i}']).convert_alpha() for i in range(1, 9)],
                'attack_3': [pygame.image.load(GAME_ASSETS[f'wizard_attack_3_{i}']).convert_alpha() for i in range(1, 9)]
            },
            'Rogue': {
                'attack_1': [pygame.image.load(GAME_ASSETS[f'rogue_attack_1_{i}']).convert_alpha() for i in range(1, 5)],
                'attack_2': [pygame.image.load(GAME_ASSETS[f'rogue_attack_2_{i}']).convert_alpha() for i in range(1, 5)],
                'attack_3': [pygame.image.load(GAME_ASSETS[f'rogue_attack_3_{i}']).convert_alpha() for i in range(1, 3)]
            }
        }
        self.enemy_attack_animation = [pygame.image.load(GAME_ASSETS[f'skeleton_attack_{i}']).convert_alpha() for i in range(1, 8)]
        self.enemy_attack_animation = [pygame.transform.scale(img, (int(img.get_width() * 2), int(img.get_height() * 2))) for img in self.enemy_attack_animation]
        self.enemy_attack_animation = [pygame.transform.flip(img, True, False) for img in self.enemy_attack_animation]
        self.player_type = None
        self.mage_player_position = [85, 88]
        self.rogue_player_position = [140, 45]
        self.warrior_player_position = [130, 45]
        self.enemies = [
            Enemy([GAME_ASSETS[f"skeleton_idle_{i}"] for i in range(1, 8)],
                  [GAME_ASSETS[f"skeleton_attack_{i}"] for i in range(1, 8)],
                  [self.window.get_width() - 400, 80], self.window)
        ]
        self.current_enemy = self.enemies[0]
        self.in_combat = True  # Ensure this attribute is defined in the constructor
        self.turn = "player"
        self.game_over = False
        self.animation_index = 0
        self.animation_counter = 0
        self.animation_speed = 10
        self.action_taken = False
        self.attack_animation = None
        self.attack_animation_counter = 0
        self.attack_animation_index = 0
        self.attack_delay = 30  # Frames to wait between attacks
        self.level = 1
        self.enemy_attack_base_damage = 5
        self.high_score = self.load_high_score()

    def load_high_score(self):
        """Load the high score from a file."""
        try:
            with open("high_score.txt", "r") as file:
                return int(file.read().strip())
        except (FileNotFoundError, ValueError):
            return 0
        
    def save_high_score(self):
        """Save the high score to a file."""
        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))

    def load_player(self, character_type):
        """
        Load the player character.

        Args:
            character_type (str): The type of character to load.
        """
        self.player_type = character_type
        scale = 1.75 if character_type == "Mage" else 3 if character_type in ["Warrior", "Rogue"] else 1
        self.player_images[character_type] = [pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                                              for img in self.player_images[character_type]]
        self.player_attack_animations[character_type] = {
            'attack_1': [pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale))) for img in self.player_attack_animations[character_type]['attack_1']],
            'attack_2': [pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale))) for img in self.player_attack_animations[character_type]['attack_2']],
            'attack_3': [pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale))) for img in self.player_attack_animations[character_type]['attack_3']]
        }
        
        if character_type == "Warrior":
            self.player = Warrior(self.window, "Player", max_hp=100)
        elif character_type == "Mage":
            self.player = Mage(self.window, "Player", max_hp=100)
        elif character_type == "Rogue":
            self.player = Rogue(self.window, "Player", max_hp=100)

    def get_player_position(self):
        if self.player_type == "Mage":
            return self.mage_player_position
        elif self.player_type == "Warrior":
            return self.warrior_player_position
        elif self.player_type == "Rogue":
            return self.rogue_player_position

    def handle_combat(self, player_attack=None, stamina_cost=0):
        """
        Handle combat between the player and the current enemy.
        """
        if self.in_combat and self.current_enemy:
            if self.turn == "player":
                if player_attack is not None:
                    if self.player.current_stamina >= stamina_cost:
                        self.player.defensive = False
                        attack_animation = f'attack_{player_attack // 5}'
                        self.attack_animation = self.player_attack_animations[self.player_type][f'attack_{player_attack // 5}']
                        self.attack_animation_counter = 0
                        self.attack_animation_index = 0
                        self.action_taken = True
                        if self.player_type == "Warrior":
                            self.damage = self.player.strength * (player_attack // 5)
                        elif self.player_type == "Mage":
                            self.damage = self.player.intelligence * (player_attack // 5)
                        elif self.player_type == "Rogue" and attack_animation != 'attack_3':
                            self.damage = self.player.dexterity * (player_attack // 5)
                        else:
                            self.damage = 0
                            self.player.defensive = True  # Defensive stance for Rogue

            elif self.turn == "enemy":
                self.current_enemy.start_attack_animation()
                self.attack_animation = self.enemy_attack_animation
                self.attack_animation_counter = 0
                self.attack_animation_index = 0
                self.action_taken = True

    def handle_events(self):
        """
        Handle user input events.

        Returns:
            str: 'quit' if the game is over and should be exited, None otherwise.
        """
        if self.game_over:
            return 'menu'  # Stop processing events if game is over

        keys = pygame.key.get_pressed()
        if not self.action_taken and self.turn == "player" and self.in_combat:
            if keys[pygame.K_j]:
                self.handle_combat(player_attack=5)  # Attack 1 deals 5 damage
            if self.level >= 2:
                if keys[pygame.K_k]:
                    self.handle_combat(player_attack=10)  # Attack 2 deals 10 damage
            if self.level >= 3:
                if keys[pygame.K_l]:
                    self.handle_combat(player_attack=15)  # Attack 3 deals 15 damage

        if self.turn == "enemy" and self.in_combat and not self.action_taken:
            self.handle_combat()

    def update(self):
        """
        Update game logic.
        """
        if self.attack_animation:
            self.attack_animation_counter += 1
            if self.attack_animation_counter >= self.attack_delay // len(self.attack_animation):
                self.attack_animation_counter = 0
                self.attack_animation_index += 1
                if self.attack_animation_index >= len(self.attack_animation):
                    if self.turn == "player":
                        enemy_defeated = self.current_enemy.take_damage(self.damage)
                        print(f"Player attacks! Deals {self.damage} damage to the enemy.")
                        if enemy_defeated:
                            print("Enemy defeated!")
                            self.enemies.remove(self.current_enemy)
                            self.in_combat = False
                            self.current_enemy = None
                            self.level += 1  # Increase level
                            self.enemy_attack_base_damage += 5
                            print(f"Player wins! Moving to level {self.level}")
                            self.next_level()  # Move to next level
                        else:
                            self.turn = "enemy"  # Switch turn to enemy
                    elif self.turn == "enemy":
                        enemy_damage = random.randint(self.enemy_attack_base_damage, self.enemy_attack_base_damage + 10)
                        if self.player.defensive == False:
                            self.player.take_damage(enemy_damage)
                        print(f"Enemy attacks back! Deals {enemy_damage} damage to the player.")
                        if not self.player.is_alive():
                            print("Player has been defeated!")
                            if self.level > self.high_score:
                                self.high_score = self.level
                                self.save_high_score()
                            self.game_over = True
                            return "menu"
                        else:
                            self.turn = "player"  # Switch turn back to player
                    self.current_enemy.reset_idle_animation()  # Reset enemy animation to idle
                    self.attack_animation = None  # Reset attack animation
                    self.action_taken = False  # Reset action taken flag

    def draw(self, selected_character):
        """
        Draw the game objects on the window.
        """
        self.window.fill((0, 0, 0))
        self.window.blit(self.map_image, (0, 0))
        self.window.blit(self.panel_image, (0, 400))

        player_position = self.get_player_position()

        if self.attack_animation and self.turn == "player":
            self.window.blit(self.attack_animation[self.attack_animation_index], player_position)
        else:
            if selected_character == "Mage":
                self.animation_counter += 1
                if self.animation_counter >= self.animation_speed:
                    self.animation_counter = 0
                    self.animation_index = (self.animation_index + 1) % len(self.player_images["Mage"])
                self.window.blit(self.player_images["Mage"][self.animation_index], player_position)
            elif selected_character == "Warrior":
                self.animation_counter += 1
                if self.animation_counter >= self.animation_speed:
                    self.animation_counter = 0
                    self.animation_index = (self.animation_index + 1) % len(self.player_images["Warrior"])
                self.window.blit(self.player_images["Warrior"][self.animation_index], player_position)
            elif selected_character == "Rogue":
                self.animation_counter += 1
                if self.animation_counter >= self.animation_speed:
                    self.animation_counter = 0
                    self.animation_index = (self.animation_index + 1) % len(self.player_images["Rogue"])
                self.window.blit(self.player_images["Rogue"][self.animation_index], player_position)

        if self.attack_animation and self.turn == "enemy" and self.game_over == False:
            self.window.blit(self.attack_animation[self.attack_animation_index], self.current_enemy.position)
        else:
            for enemy in self.enemies:
                enemy.draw()

        self.player.draw()

        if selected_character == "Mage":
            self.render_text("J ~ Jab", 20, (255, 255, 255), (20, self.window.get_height() - 125))
            if self.level >= 2:
                self.render_text("K ~ Power Slam", 20, (255, 255, 255), (20, self.window.get_height() - 105))
            if self.level >= 3:
                self.render_text("L ~ Energy Burst", 20, (255, 255, 255), (20, self.window.get_height() - 85))
        elif selected_character == "Rogue":
            self.render_text("J ~ Thrust", 20, (255, 255, 255), (20, self.window.get_height() - 125))
            if self.level >= 2:
                self.render_text("K ~ Upslash", 20, (255, 255, 255), (20, self.window.get_height() - 105))
            if self.level >= 3:
                self.render_text("L ~ Defensive Stance", 20, (255, 255, 255), (20, self.window.get_height() - 85))
        elif selected_character == "Warrior":
            self.render_text("J ~ Kick", 20, (255, 255, 255), (20, self.window.get_height() - 125))
            if self.level >= 2:
                self.render_text("K ~ Sweep", 20, (255, 255, 255), (20, self.window.get_height() - 105))
            if self.level >= 3:
                self.render_text("L ~ Slash", 20, (255, 255, 255), (20, self.window.get_height() - 85))

        pygame.display.flip()

    def render_text(self, text, font_size, color, position):
        """
        Render text on the screen.

        Args:
            text (str): The text to render.
            font_size (int): The size of the font.
            color (tuple): The color of the text (R, G, B).
            position (tuple): The position to render the text (x, y).
        """
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        self.window.blit(text_surface, position)    

    def next_level(self):
        """Progress to the next level."""
        # Load new enemy or update game state for the next level
        self.player.hit_points = 100
        enemy_idle_images = []
        enemy_attack_images = []
        if self.level == 2:
            self.player.character_hit += 5
            self.player.armor += 5
            print("Player Progression Update:\n- NEW ATTACK UNLOCKED!\n- Damage increased by 5 for all attacks\n- Armour increased by 5")
            enemy_idle_images = [GAME_ASSETS[f"plant_idle_{i}"] for i in range(1, 6)]
            enemy_attack_images = [GAME_ASSETS[f"plant_attack_{i}"] for i in range(1, 7)]
        elif self.level == 3:
            self.player.character_hit += 5
            self.player.armor += 5
            print("Player Progression Update:\n- NEW ATTACK UNLOCKED!\n- Damage increased by 5 for all attacks\n- Armour increased by 5")
            enemy_idle_images = [GAME_ASSETS[f"fire_idle_{i}"] for i in range(1, 7)]
            enemy_attack_images = [GAME_ASSETS[f"fire_attack_{i}"] for i in range(1, 12)]
        elif self.level == 4:
            self.player.character_hit += 5
            self.player.armor += 5
            print("Player Progression Update:\n- Damage increased by 5 for all attacks\n- Armour increased by 5")
            enemy_idle_images = [GAME_ASSETS[f"barbarian_idle_{i}"] for i in range(1, 6)]
            enemy_attack_images = [GAME_ASSETS[f"barbarian_attack_{i}"] for i in range(1, 6)]
        elif self.level == 5:
            self.player.character_hit += 5
            self.player.armor += 5
            print("Player Progression Update:\n- Damage increased by 5 for all attacks\n- Armour increased by 5")
            enemy_idle_images = [GAME_ASSETS[f"goblin_mage_idle_{i}"] for i in range(1, 6)]
            enemy_attack_images = [GAME_ASSETS[f"goblin_mage_attack_{i}"] for i in range(1, 7)]
        elif self.level == 6:
            self.player.character_hit += 2
            print("Player Progression Update:\n- Damage increased by 2 for all attacks")
            enemy_idle_images = [GAME_ASSETS[f"princess_idle_{i}"] for i in range(1, 9)]
            enemy_attack_images = [GAME_ASSETS[f"princess_attack_{i}"] for i in range(1, 11)]
        elif self.level == 7:
            self.player.character_hit += 2
            print("Player Progression Update:\n- Damage increased by 2 for all attacks")
            enemy_idle_images = [GAME_ASSETS[f"raven_idle_{i}"] for i in range(1, 7)]
            enemy_attack_images = [GAME_ASSETS[f"raven_attack_{i}"] for i in range(1, 7)]
        elif self.level == 8:
            self.player.character_hit += 2
            print("Player Progression Update:\n- Damage increased by 2 for all attacks")
            enemy_idle_images = [GAME_ASSETS[f"skeleton_warrior_idle_{i}"] for i in range(1, 8)]
            enemy_attack_images = [GAME_ASSETS[f"skeleton_warrior_attack_{i}"] for i in range(1, 5)]
        elif self.level == 9:
            self.player.character_hit += 2
            print("Player Progression Update:\n- Damage increased by 2 for all attacks")
            enemy_idle_images = [GAME_ASSETS[f"goblin_warrior_idle_{i}"] for i in range(1, 6)]
            enemy_attack_images = [GAME_ASSETS[f"goblin_warrior_attack_{i}"] for i in range(1, 5)]
        elif self.level == 10:
            self.player.character_hit += 2
            print("Player Progression Update:\n- Damage increased by 2 for all attacks")
            enemy_idle_images = [GAME_ASSETS[f"samurai_idle_{i}"] for i in range(1, 7)]
            enemy_attack_images = [GAME_ASSETS[f"samurai_attack_{i}"] for i in range(1, 7)]
        else:
            enemy_idle_images = [GAME_ASSETS[f"skeleton_idle_{i}"] for i in range(1, 8)]
            enemy_attack_images = [GAME_ASSETS[f"skeleton_attack_{i}"] for i in range(1, 8)]
        
        y_position = 80
        if any(substring in str(enemy_idle_images[0]) for substring in ['barbarian', 'goblin']):
            y_position += 65

        self.enemies = [
            Enemy(enemy_idle_images, enemy_attack_images, [self.window.get_width() - 400, y_position], self.window)
        ]

        self.enemy_attack_animation = [pygame.image.load(image).convert_alpha() for image in enemy_attack_images]
        self.enemy_attack_animation = [pygame.transform.scale(img, (int(img.get_width() * 2), int(img.get_height() * 2))) for img in self.enemy_attack_animation]
        self.enemy_attack_animation = [pygame.transform.flip(img, True, False) for img in self.enemy_attack_animation]
        self.current_enemy = self.enemies[0]
        self.in_combat = True
        self.turn = "player"
        self.game_over = False