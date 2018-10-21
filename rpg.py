"""RGG that is made for fun of class"""

# Import Statements----------------------------------------------------------------------------------------------------
from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import List, Tuple
import random
import time
import sys
import copy


# Input Blocker--------------------------------------------------------------------------------------------------------
def blocking_input(acceptable_responses: [str]) -> str:
    """calls input('>') until an appropriate input is selected
    :param acceptable_responses: the inputs that will get a go-ahead"""
    while True:
        output = input('>')
        if output in acceptable_responses:
            break
    return output


class Tower:
    def __init__(self,
                 name: str,
                 hp: int,
                 max_hp: int,
                 attack: int,
                 speed: float,
                 status_effects: list,
                 level: int):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.attack = attack
        self.speed = speed
        self.status_effects = status_effects
        self.level = level
        self.splash = False
        self.team = 1

    def __copy__(self):
        self.team = 2


# Character class-------------------------------------------------------------------------------------------------------
class Character:
    """All the methods a character in the game can perform"""
    def __init__(self,
                 name: str,
                 hp: float,
                 max_hp: float,
                 attack: float,
                 speed: float,
                 status_effects: list,
                 splash: bool,
                 team: int):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.attack = attack
        self.speed = speed
        self.status_effects = status_effects
        self.splash = splash
        self.team = team
        self.num_of_cards = 0
        self.total_of_cards = 2
        self.level = 1
        self.team = 1
        """:param max_hp: hp of an unharmed player
        :param level: level of the player, 1-100 eventually
        :param exp: value of the current exp a player has
        :param target_exp: value of the exp needed for a player's level to increase"""

    def is_alive(self) -> bool:
        """Returns true if the player if they are alive"""
        return self.hp > 0

    def is_ally(self, other_player) -> bool:
        """returns true if the player is an ally"""
        return other_player.team == self.team

    def deal_damage(self, other_player: 'Character'):
        """The base method for dealing damage to an enemy player
        :param other_player: target of damage"""
        if other_player.is_alive():
            other_player.hp -= self.attack
            print(f'{self.name} attacked {other_player.name}')

        return other_player

    def get_all_enemies(self, players: List['Character']) -> List[int]:
        """returns the location of all enemy players in a list"""
        return [
            index for index, player in enumerate(players)
            if not self.is_ally(player) and player.is_alive()
        ]

    def act(self, players: List):
        all_enemy_locations = self.get_all_enemies(players)
        if self.is_alive():
            if all_enemy_locations:
                targeted_index = all_enemy_locations[0]
                targeted_player = players[targeted_index]
                damaged_player = self.deal_damage(targeted_player)
                players[targeted_index] = damaged_player
                if self.splash is True:
                    for i in range(0, len(all_enemy_locations)):
                        targeted_indexes = all_enemy_locations[i]
                        targeted_players = players[targeted_indexes]
                        damaged_players = self.deal_damage(targeted_players)
                        players[targeted_indexes] = damaged_players

        return players


# How the battle runs--------------------------------------------------------------------------------------------------
@dataclass(order=True)
class Move:
    """Handles the priority Queue"""
    priority: float
    player: Character = field(compare=False)


class Battle:
    """list of characters, and order of moves"""

    def __init__(self, players: List[Character]):
        self.players = players
        self.battle_queue = PriorityQueue()

    def add_into_queue(self, player: Character, game_time: int) -> None:
        """adds a player back based on game time
        faster players go first"""
        move = Move(priority=game_time + 1/player.speed, player=player)
        self.battle_queue.put(move)

    def get_from_queue(self) -> Tuple[Character, int]:
        """removes the player from the queue to add back after cooldown"""
        move = self.battle_queue.get()
        return move.player, move.priority

    def is_over(self) -> bool:
        """true if the battle is over"""
        return self.battle_queue.empty()

    def run(self):
        """Makes the battle loop while it's not over"""
        print(f'{[player.name for player in self.players if player.team == 1]} vs '
              f'{[player.name for player in self.players if player.team == 2]}')
        # Empty print statements are to separate texts in the console
        # To improve readability during the program's running
        for player in self.players:
            self.add_into_queue(player=player, game_time=0)

        while not self.is_over():
            acting_player, current_game_time = self.get_from_queue()
            if acting_player.is_alive():
                if acting_player.team == 1:
                    print(f'{acting_player.name}\'s turn')
                    acting_player.act(self.players)
                if acting_player.is_alive and acting_player.get_all_enemies(self.players):
                    self.add_into_queue(acting_player, current_game_time)
            else:
                print(f'{acting_player.name} is dead')
            print()

        print('Match Over')


# Main Loop------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    king_tower = Tower(name='King Tower', hp=1200, max_hp=1200, attack=55, speed=10, status_effects=[], level=1)
    crown_tower = Tower(name='Crown Tower', hp=950, max_hp=950, attack=55, speed=8, status_effects=[], level=1)
    crown_tower2 = copy.copy(crown_tower)
    arch = Character(name='Archer', max_hp=240, hp=240, attack=70, speed=20, status_effects=[], splash=False, team=1)
    wizz = Character(name='Wizard', max_hp=400, hp=400, attack=170, speed=18, status_effects=[], splash=True, team=1)
    mega_min = Character(name='Mega Minion', max_hp=490, hp=490, attack=152, speed=16, status_effects=[], splash=False,
                         team=1)
    arch2 = copy.deepcopy(arch)
    arch2.name = 'Archer 2'
    arch2.team = 2
    wizz2 = copy.deepcopy(wizz)
    wizz2.name = 'Wizard 2'
    wizz2.team = 2
    mega_min2 = copy.deepcopy(mega_min)
    mega_min2.name = 'Mega Minion 2'
    mega_min2.team = 2
    battle = Battle(players=[arch, wizz, mega_min, arch2, wizz2, mega_min2])
    battle.run()
