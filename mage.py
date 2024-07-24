# MAGE.PY

from character import Character

class Mage(Character):
    def __init__(self, window, name, max_hp):
        super().__init__(window, name, "Mage", armor=5, max_hp=max_hp, hit_points=max_hp)
        self.attacks = {
            "Jab": {"method": self.jab, "stamina_cost": 10},
            "Power Slam": {"method": self.power_slam, "stamina_cost": 20},
            "Energy Burst": {"method": self.energy_burst, "stamina_cost": 30}
        }
        self.defensive = False
        self.character_hit = 5
        self.intelligence = self.character_hit

    def jab(self, target):
        damage = self.intelligence
        # print(f"{self.name} performs a jab on {target.name} for {damage} damage!")
        target.take_damage(damage)

    def power_slam(self, target):
        damage = self.intelligence * 2
        # print(f"{self.name} performs a power slam on {target.name} for {damage} damage!")
        target.take_damage(damage)

    def energy_burst(self, target):
        damage = self.intelligence * 3
        # print(f"{self.name} performs an energy burst on {target.name} for {damage} damage!")
        target.take_damage(damage)