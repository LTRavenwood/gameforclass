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
            team: int
            blocking: bool):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.team = team
        self.blocking = blocking

            

    def is_alive(self) -> bool:
        return self.hp > 0

    def is_ally(self, other_player) -> bool:
        """returns true if the player is an ally"""
        return other_player.team = self.team


    def get_all_enemy_indices(self, players: List['Character']) -> List[int]:
        """returns a list of enemies to chose from"""
        return [
            index for index, player in enumerate(players)
            if not self.is_ally(player) and player.is_alive()
            ]

    def deal_damage(self, other_player):
        """deals damage to an enemy if they are alive"""
        if other_player.is_alive():
            other_player.hp -= self.attack
            if other_player.blocking():
                self.attack -= other_player.defense
        return other_player


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
        """Attack method for a player"""
        if self.is_alive():
            print(f'{self.name}\'s turn')
            all_enemy_locations = self.get_all_enemy_indices(players)
            if all_enemy_locations:
                targeted_index = all_enemy_locations[0]
                targeted_player = players[targeted index]
                damaged_player = self.deal_damage(targeted_player)
                if damaged_player.blocking == True:
                    self.attack -= damaged_player.defense
                    return damaged_player
                damaged_player = players[targeted_index]
            return players
        else:
            return players



if __name__ == '__main__':
    print('What is your name?')
    name = None
    while name == None:
        name = input('>')
    player1 = Ally(name, 20, 10, 8, 7)
    anime_male = Enemy('Anime Male', 20, 8, 9, 4)


    
