from typing import List, Tuple
from queue import PriorityQueue
from dataclasses import dataclass, field









class Character:
    def __init__(self,
                 name: str,
                 max_hp: int,
                 hp: int,
                 attack: int,
                 speed: int,
                 team: int,
                 leveling_rate: float):
        self.name = name
        self.max_hp = max_hp
        self.hp = hp
        self.attack = attack
        self.speed = speed
        self.team = team
        self.leveling_rate = leveling_rate
        self.level = 1
        self.exp = 0
        self.target_exp = 200

    def is_alive(self)-> bool:
        """Returns true if the player is alive"""
        return self.hp > 0

    def is_ally(self, other_player) -> bool:
        """returns true if the other player is an ally"""
        return other_player.team == self.team

    def deal_damage(self, other_player, multiplier):
        """Deals damage when an attack is called
        :param multiplier: the multiplier of damage when a specific attack is called"""
        if other_player.is_alive():
            other_player.hp -= self.attack * multiplier
        return other_player

    def get_all_enemy_indices(self, players: List['Character']) -> List[int]:
        """Returns all the enemies in a list for attack targeting"""
        return [
            index for index, player in enumerate(players)
            if player.is_alive and not player.is_ally(self)
        ]

    def act(self, players: List):
        all_enemy_locations = self.get_all_enemy_indices(players)
        if all_enemy_locations:
            targeted_index = all_enemy_locations[0]
            targeted_player = players[targeted_index]
            damaged_player = self.deal_damage(targeted_player, 1.0)
            players[targeted_index] = damaged_player
        return players


@dataclass(order=True)











