import random
import time
from typing import List, Tuple
from queue import PriorityQueue
from dataclasses import dataclass, field


# Start with the player's class
class Character:
    """All the methods the game player can use"""
    def __init__(self,

            name: str,
            hp: float,
            attack: float,
            defense: float,
            speed: float,
            team: int):


    def is_alive(self) -> bool:
        return self.hp > 0

    def is_enemy(self, other_player) -> bool:
        """Returns true if the player is an enemy"""
        return other_player.team != self.team


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


    def deal_damage(self, other_player: 'Character') -> 'Character':
        """Deals damage to another Charater Object

        :param other_player: TODO: Fill in
        :return: TODO: Fill in
        """
        if other_player.is_alive:
            other_player.hp -= self.attack
        # Alex: Moved this out of the if statement
        # because this method wouldn't have returned a value if the other player
        # was dead.
        return other_player

    def get_all_enemy_indices(self,
                              players: List['Character']) -> List[int]:
        """Returns a list of enemies to choose a target from

        Specifically, returns the indices in players that are characters
        which are both enemies and alive

        :param players: TODO: Fill in
        :return: TODO: Fill in
        """
        return [
            index for index, player in players
            if player.is_alive and player.is_enemy
        ]

    def attack(self,
               players: List['Character']) -> List['Character']:
        """Attack method for a player

        TODO: Fill in what the default method does

        Alex: I don't think you really need this. Think about what deal_damage already does
        and the fact that you want to allow a player to select a target if you ever want to add
        multiple opponents.

        :param players: TODO: Fill in
        :return: TODO: Fill in
        """





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


if __name__ == '__main__':
    print('What is your name?')
    name = None
    while name is None:
        name = input('>')
    player1 = Ally(name, 20, 10, 8, 7)
    anime_male = Enemy('Anime Male', 20, 8, 9, 4)

    battle = Battle(players=[player1, anime_male])
    battle.run()