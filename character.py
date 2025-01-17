# CHARACTER.PY

import pygame
from assets import GAME_ASSETS
from healthbar import HealthBar

class Character:
    MAX_LEVEL = 50  # Maximum level a character can reach
    ATTRIBUTE_POINTS_PER_LEVEL = 3  # Number of attribute points gained per level

    def __init__(self, window, name, character_class, armor, max_hp, hit_points):
        self.window = window
        self.name = name  # Character's name
        self.character_class = character_class  # Character's class
        self.armor = armor  # Character's armor value
        self.max_hp = max_hp
        self.hit_points = hit_points  # Example starting value for character's hit points
        self.alive = True
        self.level = 1  # Character's current level
        self.experience_points = 0  # Character's current experience points
        self.armor_class = 10  # Example starting value for character's armor class
        self.skills = {}  # Example empty dictionary for character's skills
        self.inventory = []  # Example empty list for character's inventory
        self.attribute_points = 0  # Attribute points available to allocate

        self.max_stamina = 100
        self.current_stamina = self.max_stamina
        self.stamina_regeneration = 10

        self.health_bar = HealthBar(window, x=220, y=window.get_height() - 150, label="Player HP: ", width=100)
        self.stamina_bar = HealthBar(window, x=220, y=window.get_height() - 80, label="Player Stamina: ", width=100)
        self.level_bar = HealthBar(window, x=220, y=window.get_height() - 10, label="Player Level: ", width=100)

    def assign_attribute_points(self, attribute, points):
        # Ensure the attribute exists before assigning points
        if attribute in self.__dict__:
            setattr(self, attribute, getattr(self, attribute) + points)  # Add points to the attribute
            self.attribute_points -= points  # Decrease available attribute points
        else:
            print(f"Error: Attribute '{attribute}' does not exist.")

    def gain_experience(self, experience):
        self.experience_points += experience  # Increase character's experience points
        # Calculate experience required for next level
        required_experience = self.calculate_required_experience(self.level + 1)
        # Check if character has enough experience to level up and is below the level cap
        while self.experience_points >= required_experience and self.level < self.MAX_LEVEL:
            self.level += 1  # Level up the character
            self.experience_points -= required_experience  # Decrease character's experience points
            self.hit_points += 10  # Example: Increase hit points by 10 each level up
            self.attribute_points += self.ATTRIBUTE_POINTS_PER_LEVEL  # Allocate attribute points
            print(f"Level up! {self.name} is now level {self.level}.")
            # Calculate experience required for next level
            required_experience = self.calculate_required_experience(self.level + 1)

    def calculate_required_experience(self, level):
        # Example exponential scaling: Each level requires 100 more experience points than the previous level
        return int(100 * (1.5 ** (level - 1)))

    def is_alive(self):
        return self.hit_points > 0

    def take_damage(self, amount):
        # Calculate the actual damage taken, taking into account the character's armor
        actual_damage = max(0, amount - self.armor)
        self.hit_points -= actual_damage
        if self.hit_points <= 0:
            self.alive = False
            print(f"{self.name} takes {actual_damage} damage and has been defeated!")
        else:
            print(f"{self.name} takes {actual_damage} damage. Remaining hit points: {self.hit_points}")

    def regenerate_stamina(self):
        self.current_stamina = min(self.max_stamina, self.current_stamina + self.stamina_regeneration)

    def draw(self):
        self.health_bar.draw(self.hit_points, self.max_hp, type="Health")
        self.stamina_bar.draw(self.current_stamina, self.max_stamina, type="Stamina")
