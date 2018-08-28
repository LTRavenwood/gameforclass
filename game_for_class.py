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

    def block(self, other_player: 'Character'):
        """stops the other player from doing as much damage

        Alex: you need to rethink what this method really entails
        your implementation was mixing return types (Sometimes with return a player,
        other times a list of players
        It could also PERMANENTLY alter an enemy's stats, which would be very confusing
        My suggestion: Look into how to properly use self.defense and how to use that value
        in self.deal_damage()

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

    def act(self, players: List['Character']) -> List['Character']:
        """TODO: Fill in

        Alex: You need to implement a default act method

        TODO: Fill in what the default method does



# TODO: Change You to a better (more descriptive) class name
class You(Character):
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

    # def act(self, players):
    #     all_enemy_locations = self.get_all_enemy_indices(players)
    #     print('What will you do?')
    #     print('"w" to attack, or "s" to block')
    #     if all_enemy_locations:
    #         move_options = {'w': self.attack, 's': player.block(other_player)}
    #         player_move = None
    #         while player_move == None:
    #             move = input('>')
    #             player_move = move_options.get(move)
    #             return player_move

    def act(self, players: List[Character]) -> List[Character]:
        """Overrides the default act method,

        Allows a user to select a supported action (attack, block)
        and also determine a target if attacking

        :param players: TODO: fill in
        :return: TODO: fill in
        """
        raise NotImplementedError()


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

    # def act(self, players):
    #
    #     all_enemy_locations = self.get_all_enemy_indices(players)
    #     if all_enemy_locations:
    #         move_options = ['attack', 'block']
    #         move = random.choice(move_options)
    #         if move == 'attack':
    #             self.attack(other_player)
    #         if move == 'block':
    #             self.block(other_player)
    #             return move
    def act(self, players: List[Character]) -> List[Character]:
        """Overrides the default act method,

        Randomly selects an action (attack, block) and if attacking, randomly
        selects a valid target.

        :param players: TODO: fill in
        :return: TODO: fill in
        """
        raise NotImplementedError()


@dataclass(order=True)
class Move:
    priority: float
    player: Character = field(compare=False)


class Battle:
    def __init__(self, players: List[Character]):
        self.players = players
        self.battle_queue = PriorityQueue()

    def add_into_queue(self, player: Character, game_time: int) -> None:
        move = Move(priority=game_time + 1.0/player.speed, player=player)
        self.battle_queue.put(move)

    def get_from_queue(self) -> Tuple[Character, int]:
        move = self.battle_queue.get()
        return move.player, move.priority

    def is_over(self) -> bool:
        return self.battle_queue.empty()

    def run(self):
        for player in self.players:
            self.add_into_queue(player=player, game_time=0)
        while not self.is_over():
            acting_player, current_game_time = self.get_from_queue()
            if acting_player.is_alive():
                updated_players = acting_player.act(self.players)
                self.players = updated_players
                print(


                    [f'{player.name}\'s hp: {player.hp}'

                     for player in self.players]
                )
                if acting_player.is_alive and acting_player.get_all_enemy_indices(self.players):
                    self.add_into_queue(acting_player, current_game_time)
            else:
                print(f'{acting_player.name} was defeated!')
        print('The battle is over')
        print('survivors:')
        print(f'{[player.name for player in self.players if player.is_alive()]}')


if __name__ == '__main__':
    print('What is your name?')
    name = None
    while name is None:
        name = input('>')
    player1 = Ally(name, 20, 10, 8, 7)
    anime_male = Enemy('Anime Male', 20, 8, 9, 4)

    battle = Battle(players=[player1, anime_male])
    battle.run()












