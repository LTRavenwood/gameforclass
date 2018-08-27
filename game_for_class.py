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
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.team = team

    def is_alive(self) -> bool:
        """returns true if the character is alive"""
        return self.hp > 0

    def is_enemy(self, other_player) -> bool:
        """returns true if the player is an enemy"""
        return other_player.team != self.team

    def deal_damage(self, other_player):
        """Deals damage to another Character Object"""
        if other_player.is_alive:
            other_player_block = False
            while Other_player_block == False:
                other_player.hp -= self.attack
            else:
                self.attack -= other_player.defense
                other_player.hp -= self.attack 
        return other_player

    def get_all_enemy_indices(self, players: List['Character']) -> List[int]:
        """Returns a list of enemies to choose a target from
            specifically returns if a target is alive and is an enemy"""
        return [
            index for index, player in self.players
            if player.is_alive and player.is_enemy
            ]
        


    def block(self):
        if self.block():
            other_player_block = True
        else:
            other_player_block = False

    def act(self, players: List['Character']) -> List['Character']:
        """A way of the characters to interact with one another
            ie. an attack"""


        all_enemy_locations = self.get_all_enemy_indices(players)
        if all_enemy_locations:
            targeted_index = all_enemy_locations[0]
            targeted_player = players[targeted_index]
            damaged_player = self.deal_damage(targeted_player)
            players[targeted_index] = damaged_player
            return players
        else:
            return players

            

class Ally(Character):
    def __init__(self,
                 name: str,
                 hp: float,
                 attack: float,
                 defense: float,
                 speed: float):
        super().__init__(
            name=name,
            hp=hp,
            attack=attack,
            defense=defense,
            speed=speed,
            team=1
        )


    def act(self, players: List ['Character']) -> List['Character']:
        """Overides the default method

        Allows a user to select a supported action (attack, block)
        and also determine if a target is attacking

        :param players
        """
        all_enemy_locations = self.get_all_enemy_indices(players)
        if all_enemy_locations:
            print('What will you do?')
            print('"w" to attack or "s" to block')
            move_options = {'w': self.attack(), 's': self.block()}
            player_move = None
            while player_move == None:
                move = input('>')
                player_move = move_options.get(move)
        return player_move
        

class Enemy(Character):
    def __init__(self,
                 name: str,
                 hp: float,
                 attack: float,
                 defense: float,
                 speed: float):
        super().__init__(
            name=name,
            hp=hp,
            attack=attack,
            defense=defense,
            speed=speed,
            team=2
        )


    def act(self, players):
        """Overides the default act method

        randomly selects an action (attack, block) and if attacking,
        randomly selects a valid target.

        :param players
        """

        
        
        all_enemy_locations = self.get_all_enemy_indices(players)
        if all_enemy_locations:
            move_options = ['attack', 'block']
            move = random.choice(move_options)
            if move == 'attack':
                self.attack(other_player)
            if move == 'block':
                self.block(other_player)
                return move




@dataclass(order=True)
class Move:
    priority: float
    player: Character = field(compare=False)

class Battle:
    def __init__(self, players: List[Character]):
        self.players = players
        self.battle_queue = PriorityQueue

    def add_into_queue(self, player: Character, game_time: int) -> None:
        move = Move(priority=game_time + 1/player.speed, player=player)
        self.battle_queue.put(move)

    def get_from_queue(self) -> Tuple[Character, int]:
        move = self.battle_queue.get()
        return move.player, move.priority

    def is_over(self) -> bool:
        return self.battle_queue.empty()

    def run(self):
        print(f'{anime_male.name} appeared!')
        for player in self.players:
            self.add_into_queue(player=player, game_time=0)
        while not self.is_over():
            acting_player, current_game_time = self.get_from_queue()
            if acting_player.is_alive():
                updated_players = acting_player.act(self.players)
                self.players = updated_players
                print(
                    [f'{player.name}\'s HP: {player.hp}'
                     for player in self.players]
                )
                if acting_player.is_alive and acting_player.get_all_enemy_indices(self.players):
                    self.add_into_queue(acting_player, current_game_time)
            else:
                print(f'{acting_player.name} was defeated!')
        print('the battle is over')
        print('survivors:')
        print(f'{[player.name for player in self.players if player.is_alive()]}')


if __name__ == '__main__':
    print('What is your name?')
    name = None
    while name == None:
        name = input('>')
    player1 = Ally(name, 20, 10, 8, 7)
    anime_male = Enemy('Anime Male', 20, 8, 9, 4)

    battle = Battle(players=[player1, anime_male])
    battle.run()












