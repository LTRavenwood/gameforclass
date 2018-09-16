from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import List, Tuple
import random
import time


class Item:
    def __init__(self,
                 name: str,
                 hp_restore: int):
        self.name = name
        self.hp_restore = hp_restore


inventory = []


class Character:
    """All the methods a character in the game can perform"""
    def __init__(self,
                 name: str,
                 hp: int,
                 max_hp: int,
                 attack: int,
                 speed: int,
                 leveling_rate: int,
                 exp: int,
                 level_exp: int,
                 team: int,
                 level: int):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.attack = attack
        self.speed = speed
        self.leveling_rate = leveling_rate
        self.exp = exp
        self.level_exp = level_exp
        self.team = team
        self.level = level
        self.is_burned = False
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

    def deal_damage(self, other_player):
        """Deals damage if the other player is alive"""
        if other_player.is_alive():
            other_player.hp -= self.attack
            print(f'{self.name} attacked {other_player.name} for {self.attack} damage!')
        return other_player

    def deal_damage2(self, other_player):
        """Deals a bit more damage and has a chance to burn the target"""
        if other_player.is_alive():
            self.attack *= 2
            other_player.hp -= self.attack
            burn_chance = random.randint(1, 100)
            if burn_chance < 11:
                other_player.is_burned = True
                print(f'{self.name} attacked {other_player.name} for {self.attack} damage!')
        return other_player

    def get_all_enemies(self, players: List) -> List[int]:
        """returns the location of all enemy players in a list"""
        return [
            index for index, player in enumerate(players)
            if not self.is_ally(player) and player.is_alive()
        ]

    def act(self, players: List) -> List:
        """how one player acts upon another, eg. an attack"""
        all_enemy_locations = self.get_all_enemies(players)
        if self.is_alive:
            if all_enemy_locations:
                targeted_index = all_enemy_locations[0]
                targeted_player = players[targeted_index]
                print('What move will you use?')
                damage_input = input('>')
                print(damage_input)
                if damage_input == 1:
                    damaged_player = self.deal_damage(targeted_player)
                    players[targeted_index] = damaged_player
                elif damage_input == 2:
                    damaged_player = self.deal_damage2(targeted_player)
                    players[targeted_index] = damaged_player
                else:
                    print('please enter a move option.')
                    damage_input = input('>')
                    print(damage_input)

        return players


class Ally(Character):
    # subclass of character
    """This is a subclass of characters specific to team 1"""
    def __init__(self,
                 name: str,
                 hp: int,
                 max_hp: int,
                 attack: int,
                 speed: int,
                 leveling_rate: int):
        super().__init__(name,
                         hp,
                         max_hp,
                         attack,
                         speed,
                         leveling_rate,
                         exp=0,
                         level_exp=200,
                         team=1,
                         level=1)

    def act(self, players):
        """the act method specific to team 1"""

        all_enemy_locations = self.get_all_enemies(players)
        enemies = {character.name:
                   character for character in players if character.team != 1}
        if self.is_alive:
            if all_enemy_locations:
                if len(all_enemy_locations) == 1:  # if there is only one enemy in the battle:
                    targeted_index = all_enemy_locations[0]
                    targeted_player = players[targeted_index]
                    print('What move will you use?')
                    damage_input = input('>')
                    print(damage_input)
                    if damage_input == 1:
                        damaged_player = self.deal_damage(targeted_player)
                        players[targeted_index] = damaged_player
                    elif damage_input == 2:
                        damaged_player = self.deal_damage2(targeted_player)
                        players[targeted_index] = damaged_player
                    else:
                        print('What move will you use?')
                        damage_input = input('>')
                        print(damage_input)
                else:  # if there is more than one enemy in the battle:
                    print('Who do you attack?')
                    for player in players:
                        if player.is_alive() and not player.is_ally(self):
                            print(player.name)
                    targeted_enemy = None
                    while targeted_enemy is None:
                        user_input = input('>')
                        targeted_enemy = enemies.get(user_input)
                        print('What move will you use?')
                        damage_input = input('>')
                        print(damage_input)
                        if damage_input == 1:
                            damaged_player = self.deal_damage(targeted_enemy)
                            targeted_enemy = damaged_player
                        elif damage_input == 2:
                            damaged_player = self.deal_damage2(targeted_enemy)
                            targeted_enemy = damaged_player
                        else:
                            damage_input = input('>')
                            print(damage_input)

        return players

    def move_input(self):
        print('What will you do?')
        print('[f]ight, [i]tem, [s]tats')
        move_input = input('>')
        print(move_input)
        move = move_input
        print(move)
        if move == 'f':
            pass
        elif move == 'i':
            self.use_item()
        elif move == 's':
            self.get_stats()
        else:
            print('Please input a move.')
            return move_input

    def use_item(self):
        if potion.name in inventory:
            print(f'would you like to use {potion.name}?')
            print('[y]es or [n] no')
            item_input = input('>')
            print(item_input)
            if item_input == 'y':
                if self.hp < self.max_hp:
                    self.hp = min(self.hp + potion.hp_restore, self.max_hp)
                    inventory.remove(potion)
                else:
                    print('It won\'t help')
            if item_input == 'n':
                pass
            elif item_input != 'y' and item_input != 'n':
                print('please enter y or n')
                return item_input
            else:
                print('Your inventory is empty')

    def get_stats(self):
        """prints out the player's important stats"""
        if self.is_alive():
            stats = {
                'name': self.name,
                'hp/max hp': f'{self.hp}/{self.max_hp}',
                'speed': self.speed
            }
            print(stats)


class Enemy(Character):
    # another subclass of character
    """this is a subclass of characters specific to team 2"""
    def __init__(self,
                 name: str,
                 hp: int,
                 max_hp: int,
                 attack: int,
                 speed: int,
                 leveling_rate: int):
        super().__init__(name,
                         hp,
                         max_hp,
                         attack,
                         speed,
                         leveling_rate,
                         exp=0,
                         level_exp=200,
                         team=2,
                         level=1)

    def act(self, players):
        all_enemy_locations = self.get_all_enemies(players)
        if all_enemy_locations:
            damage_input = random.randint(1, 2)
            targeted_player = random.choice(all_enemy_locations)
            if damage_input == 1:
                damaged_player = self.deal_damage(targeted_player)
                players[targeted_index] = damaged_player
            elif damage_input == 2:
                damaged_player = self.deal_damage2(targeted_player)
                players[targeted_index] = damaged_player

        return players


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

    def victory(self) -> bool:
        """returns true if the allies win"""
        if self.is_over():
            if player1.is_alive() or aqua.is_alive():
                victory = True
                return victory

    def defeat(self) -> bool:
        """Returns true if the enemies win"""
        if self.is_over():
            if player1.get_all_enemies(self.players):
                defeat = True
                return defeat

    def level_up(self):
        exp_gain = 200
        for player in self.players:
            if player.is_alive():
                player.exp += exp_gain
                print(f'{player.name} gained {exp_gain} experience points!')
                if player.exp >= player.level_exp:
                    print(f'{player.name} leveled up!')
                    player.level += 1
                    player.max_hp += 2
                    player.hp = player.max_hp
                    player.attack += 1
                    player.speed += 1
                    player.level_exp *= (player.leveling_rate * 2)
                    player.exp = 0
                    print(f'HP: {player.hp}/{player.max_hp}')
                    print(f'New attack: {player.attack}')
                    print(f'New speed: {player.speed}')

    def run(self):
        """Makes the battle loop while it's not over"""
        print(f'{[player.name for player in self.players if player.team != 1]} appeared!')
        print()
        for player in self.players:
            self.add_into_queue(player=player, game_time=0)

        while not self.is_over():
            acting_player, current_game_time = self.get_from_queue()
            if acting_player.is_alive():
                if acting_player.team == 1:
                    print(f'{acting_player.name}\'s turn')
                    print()
                    acting_player.move_input()
                    print(acting_player.move_input)
                    acting_player.act(self.players)
                else:
                    acting_player.act(self.players)
                if acting_player.is_burned is True:
                    acting_player.hp -= 1
                    print(f'{acting_player.name} was burned for 1 damage!')
                    print()
                for player in self.players:
                    if player.is_alive():
                        print(f'{player.name} LV: {player.level}')
                        print(f'HP: {player.hp}/{player.max_hp}')
                if acting_player.is_alive and acting_player.get_all_enemies(self.players):
                    self.add_into_queue(acting_player, current_game_time)
            else:
                print(f'{acting_player.name} is dead')
            print()

        if self.victory():
            print('You win!')
            self.level_up()
        if self.defeat():
            print('You lose!')


if __name__ == '__main__':
    print('What is your name?')
    name = ''
    while name == '':
        name = input('>')
    player1 = Ally(name=name, hp=5, max_hp=5, attack=3, speed=2, leveling_rate=1)
    aqua = Ally(name='Aqua', hp=7, max_hp=7, attack=4, speed=3, leveling_rate=2)
    krillin = Enemy(name='Krillin', hp=7, max_hp=7, attack=3, speed=2, leveling_rate=0)
    yamcha = Enemy(name='Yamcha', hp=7, max_hp=7, attack=3, speed=1, leveling_rate=0)
    anime_male = Enemy(name='Anime Male', hp=5, max_hp=5,attack=2, speed=2, leveling_rate=1)
    battle = Battle(players=[player1, aqua, krillin, yamcha])
    potion = Item('potion', 5)
    battle1 = Battle(players=[player1, anime_male])
    battle1.run()
    inventory.append(potion)
    print(f'You found a {potion.name}')
    print(f'{aqua.name} joined!')
    battle.run()
    time.sleep(5)
