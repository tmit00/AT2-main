'''from character import Character

class Rogue(Character):
    def __init__(self, name):
        super().__init__(name, "Rogue", armour = 7)
        # Additional attributes and methods specific to the Rogue class'''

from character import Character

class Rogue(Character):
    def __init__(self, name, max_hp):
        super().__init__(name, "Rogue", armor=7)
        self.max_energy = 100
        self.current_energy = self.max_energy
        self.energy_regeneration = 20
        self.agility = 18
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.skills = {
            "Quick Strike": {"method": self.quick_strike, "energy_cost": 10},
            "Backstab": {"method": self.backstab, "energy_cost": 25},
            "Poisoned Blade": {"method": self.poisoned_blade, "energy_cost": 15},
            "Evasion": {"method": self.evasion, "energy_cost": 20},
            "Shadow Step": {"method": self.shadow_step, "energy_cost": 30},
        }

    def choose_skill(self, target):
        print(f"Choose a skill (Current energy: {self.current_energy}):")
        skill_list = list(self.skills.items())
        for i, (skill, info) in enumerate(skill_list):
            print(f"{i + 1}. {skill} (Energy cost: {info['energy_cost']})")
        chosen_skill = int(input("Enter the number of the skill: "))
        if 1 <= chosen_skill <= len(skill_list):
            skill, skill_info = skill_list[chosen_skill - 1]
            if self.current_energy >= skill_info["energy_cost"]:
                self.current_energy -= skill_info["energy_cost"]
                skill_method = skill_info["method"]
                skill_method(target)
            else:
                print("Not enough energy for this skill.")
        else:
            print("Invalid skill.")

    def regenerate_energy(self):
        self.current_energy = min(self.max_energy, self.current_energy + self.energy_regeneration)

    def quick_strike(self, target):
        damage = self.agility  # Example: Quick Strike deals damage equal to rogue's agility
        print(f"{self.name} performs a Quick Strike on {target.name} for {damage} damage!")
        target.take_damage(damage)

    def backstab(self, target):
        damage = self.agility * 2  # Example: Backstab deals double the rogue's agility as damage
        print(f"{self.name} performs a Backstab on {target.name} for {damage} damage!")
        target.take_damage(damage)

    def poisoned_blade(self, target):
        damage = self.agility * 1.5  # Example: Poisoned Blade deals 1.5 times the rogue's agility as damage
        print(f"{self.name} performs a Poisoned Blade on {target.name} for {damage} damage!")
        target.take_damage(damage)

    def evasion(self):
        self.armor_class += 7  # Example: Evasion increases armor class by 7
        print(f"{self.name} uses Evasion, increasing armor class!")

    def shadow_step(self, target):
        damage = self.agility * 2.5  # Example: Shadow Step deals 2.5 times the rogue's agility as damage
        print(f"{self.name} uses Shadow Step to attack {target.name} for {damage} damage!")
        target.take_damage(damage)