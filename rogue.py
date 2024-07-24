# ROGUE.PY

from character import Character

class Rogue(Character):
    def __init__(self, window, name, max_hp):
        super().__init__(window, name, "Rogue", armor=7, max_hp=max_hp, hit_points=max_hp)
        self.attacks = {
            "Thrust": {"method": self.thrust, "stamina_cost": 10},
            "Upslash": {"method": self.upslash, "stamina_cost": 20},
            "Defensive Stance": {"method": self.defensive_stance, "stamina_cost": 0}  # No stamina cost
        }
        self.defensive = False
        self.character_hit = 5
        self.dexterity = self.character_hit

    def thrust(self, target):
        damage = self.dexterity
        # print(f"{self.name} performs a thrust on {target.name} for {damage} damage!")
        target.take_damage(damage)

    def upslash(self, target):
        damage = self.dexterity * 2
        # print(f"{self.name} performs an upslash on {target.name} for {damage} damage!")
        target.take_damage(damage)

    def defensive_stance(self, target):
        # print(f"{self.name} assumes a defensive stance, blocking all incoming damage this turn!")
        self.blocking = True  # Custom attribute to handle blocking logic

    def take_damage(self, amount):
        if self.defensive:
            self.defensive = False  # Reset defensive stance after blocking
        else:
            super().take_damage(amount)