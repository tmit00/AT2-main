# WARRIOR.PY

from character import Character

class Warrior(Character):
    def __init__(self, window, name, max_hp):
        super().__init__(window, name, "Warrior", armor=10, max_hp=max_hp, hit_points=max_hp)
        self.attacks = {
            "Kick": {"method": self.kick, "stamina_cost": 10},
            "Sweep": {"method": self.sweep, "stamina_cost": 20},
            "Slash": {"method": self.slash, "stamina_cost": 30}
        }
        self.defensive = False
        self.character_hit = 5
        self.strength = self.character_hit

    def kick(self, target):
        damage = self.strength
        # print(f"{self.name} performs a kick on {target.name} for {damage} damage!")
        target.take_damage(damage)

    def sweep(self, target):
        damage = self.strength * 2
        # print(f"{self.name} performs a sweep on {target.name} for {damage} damage!")
        target.take_damage(damage)

    def slash(self, target):
        damage = self.strength * 3
        # print(f"{self.name} performs a slash on {target.name} for {damage} damage!")
        target.take_damage(damage)



