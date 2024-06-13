'''from character import Character

class Mage(Character):
    def __init__(self, name):
        super().__init__(name, "Mage", armour = 5)
        # Additional attributes and methods specific to the Mage class'''

from character import Character

class Mage(Character):
    def __init__(self, name, max_hp):
        super().__init__(name, "Mage", armor=5)
        self.max_mana = 150
        self.current_mana = self.max_mana
        self.mana_regeneration = 15
        self.intelligence = 20
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.spells = {
            "Fireball": {"method": self.fireball, "mana_cost": 30},
            "Ice Lance": {"method": self.ice_lance, "mana_cost": 20},
            "Arcane Blast": {"method": self.arcane_blast, "mana_cost": 40},
            "Magic Shield": {"method": self.magic_shield, "mana_cost": 25},
            "Mana Regeneration": {"method": self.mana_regeneration_spell, "mana_cost": 10},
        }

    def choose_spell(self, target):
        print(f"Choose a spell (Current mana: {self.current_mana}):")
        spell_list = list(self.spells.items())
        for i, (spell, info) in enumerate(spell_list):
            print(f"{i + 1}. {spell} (Mana cost: {info['mana_cost']})")
        chosen_spell = int(input("Enter the number of the spell: "))
        if 1 <= chosen_spell <= len(spell_list):
            spell, spell_info = spell_list[chosen_spell - 1]
            if self.current_mana >= spell_info["mana_cost"]:
                self.current_mana -= spell_info["mana_cost"]
                spell_method = spell_info["method"]
                spell_method(target)
            else:
                print("Not enough mana for this spell.")
        else:
            print("Invalid spell.")

    def regenerate_mana(self):
        self.current_mana = min(self.max_mana, self.current_mana + self.mana_regeneration)

    def fireball(self, target):
        damage = self.intelligence * 2  # Example: Fireball deals double the mage's intelligence as damage
        print(f"{self.name} casts Fireball on {target.name} for {damage} damage!")
        target.take_damage(damage)

    def ice_lance(self, target):
        damage = self.intelligence * 1.5  # Example: Ice Lance deals 1.5 times the mage's intelligence as damage
        print(f"{self.name} casts Ice Lance on {target.name} for {damage} damage!")
        target.take_damage(damage)

    def arcane_blast(self, target):
        damage = self.intelligence * 2.5  # Example: Arcane Blast deals 2.5 times the mage's intelligence as damage
        print(f"{self.name} casts Arcane Blast on {target.name} for {damage} damage!")
        target.take_damage(damage)

    def magic_shield(self):
        self.armor_class += 10  # Example: Magic Shield increases armor class by 10
        print(f"{self.name} casts Magic Shield, increasing armor class!")

    def mana_regeneration_spell(self):
        self.current_mana = min(self.max_mana, self.current_mana + 50)  # Example: Mana Regeneration spell restores 50 mana
        print(f"{self.name} casts Mana Regeneration, restoring 50 mana!")
