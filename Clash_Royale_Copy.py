

class Towers:
    def __init__(self,
                 name: str,
                 hp: int,
                 damage: int,
                 team: int):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.team = team

    def is_alive(self) -> bool:
        """returns true if the crown tower is not destroyed"""
        return self.hp > 0

    def is_ally(self, other_object):
        """returns true if another object, eg. the opposite crown tower or a card is yours"""
        return other_object.team == self.team

    def deal_damage(self, other_object):
        """deals Damage to the other player's cards"""
        if other_object.is_alive():
            other_object.hp -= self.damage
            return other_object

