import random
import time
from typing import List, Tuple
from queue import PriorityQueue
from dataclasses import dataclass, field


# Start with the player's class
class Character:
    """All the methods the game player can use"""
    def __init__(self, name: str, hp: float, attack: float, defense: float, speed: float, team: int):

        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.team = team
        """Initializes the Character"""

    def is_alive(self) -> bool:

        """returns true if the player is alive"""
        return self.hp > 0

    def is_ally(self, other_player) -> bool:
        """returns true if the other player is an ally"""
        return other_player.team == self.team

    def get_all_enemy_indices(self, players: List['Character']) -> List[int]:
        """returns a list of enemies to chose from"""
        return [index for index, player in enumerate(players) if not self.is_ally(player) and player.is_alive()]

    def deal_damage(self, other_player):
        """deals damage to an enemy if they are alive"""
        if other_player.is_alive():
            other_player.hp -= self.attack
        return other_player

    def block(self, other_player) -> bool:
        """Blocks for a little bit of damage before returning to normal damage"""
        if self.block():
            return self.block == True
        if self.block == True:
            other_player.attack -= self.defense
        return self.block == False

    def act(self, players: List['Character']) -> List[int]:
        all_enemy_locations = self.get_all_enemy_indices

        if all_enemy_locations:
            targeted_index = all_enemy_locations[0]
            targeted_player = players[targeted_index]
            damaged_player = self.deal_damage(targeted_player)
            players[targeted_index] = damaged_player
            return players
        else:
            return players




        :param players: TODO: Fill in
        :return: TODO: Fill in
        """
        # if self.block:
        #     if other_player.deal_damage(self):
        #         other_player.attack -= player.defense
        #         return other_player
        #     return players
        # else:
        #     return players
        raise NotImplementedError()













