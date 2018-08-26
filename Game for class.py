import random
import time
from typing import List, Tuple
from queue import PriorityQueue
from dataclasses import dataclass, field

# Start with the player's class
class Character:
    """All the methods the game player can use"""
    def __init__(self, name, hp, attack, defense, speed, team):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.team = team

    def is_alive(self) -> bool:
        """returns true if the character is alive"""
        return self.hp >= 1

    def is_enemy(self, other_player) -> bool:
        """returns true if the player is an enemy"""
        return other_player.team != self.team

    def deal_damage(self, other_player):
        """Deals damage when an attack is called"""
        if other_player.is_alive:
            other_player.hp -= self.attack
            return other_player

    def get_all_enemy_indices(self, players: List) -> List[int]:
        """Returns a list of enemies to choose a target from"""
        return [index for index, player in self.players if player.is_alive and player.is_enemy]
        

    def attack(self, players):
        """how the player attacks"""
        all_enemy_locations = self.get_all_enemy_indices(players)
        if all_enemy_locations:
            targeted_index = all_enemy_locations[0]
            targeted_player = players[targeted_index]
            damaged_player = self.deal_damage(targeted_player)
            players[targeted_index] = damaged_player
            return players
        else:
            return players

    def block(self, other_player):
        """stops the other player from doing as much damage"""
        if self.block:
            if other_player.deal_damage(self):
                other_player.attack -= player.defense
                return other_player
            return players
        else:
            return players
            

class You(Character):
    def __init__(self, name, hp, attack, defense, speed, team):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.team = team
        

    def input_name(self):
        self.name = name
        print('What is your name?')
        name = input('>')
        return name

    def act(self, players):
        all_enemy_locations = self.get_all_enemy_indices(players)
        print('What will you do?')
        print('"w" to attack, or "s" to block')
        if all_enemy_locations():
            move_options = {'w': self.attack(other_player), 's': player.block(other_player)}
            player_move = None
            while player_move == None:
                move = input('>')
                player_move = move_options.get(move)
                return player_move

class Enemy(Character):
    def __init__(self, name, hp, attack, defense, speed, team):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.team = team

    def act(self, players):
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
    priority: int
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
                print(f'Enemy HP: {anime_male.hp}')
                print(f'Your HP: {player1.hp}')
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
    player1 = You(name, 20, 10, 8, 7, 1)
    anime_male = Enemy('Anime Male', 20, 8, 9, 4, 2)

    battle = Battle(players=[player1, anime_male])
    battle.run()
        











