from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import List, Tuple
import random
import time


def blocking_input(acceptable_responses: [str]) -> str:
    """calls input('>') until an appropriate input is selected
    :param acceptable_responses: the inputs that will get a go-ahead"""
    while True:
        output = input('>')
        if output in acceptable_responses:
            break
    return output


class Item:
    """This will NOT just be potions,
    there will be statuses to worry about and cure with items"""
    def __init__(self,
                 name: str,
                 hp_restore: int,
                 heal_status: bool):
        self.name = name
        self.hp_restore = hp_restore,
        self.heal_status = heal_status


inventory = []


class Character:
    """All the methods a character in the game can perform"""
    def __init__(self,
                 name: str,
                 hp: float,
                 max_hp: float,
                 attack: float,
                 speed: float,
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

    def deal_damage(self, other_player: 'Character', multiplier: float, burn_chance: int):
        """The base method for dealing damage to an enemy player
        :param other_player: target of damage
        :param multiplier: the multiplier of the damage dealt
        :param burn_chance: target's chance of being burned in the attack"""
        if other_player.is_alive():
            other_player.hp -= (int(self.attack * multiplier))
            other_player.is_burned = other_player.is_burned or (burn_chance > random.randint(1, 100))
            print(f'{self.name} attacked {other_player.name} for {int(self.attack * multiplier)} damage!')
            if other_player.is_burned:
                print(f'{other_player.name} Received a burn!')
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
                damaged_player = self.deal_damage(targeted_player, 1.0, 0)
                players[targeted_index] = damaged_player
        return players


class Ally(Character):
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
        """:param leveling_rate: a multiplier of the level exp every time
                    """

    def act(self, players: List['Character']):
        """the act method specific to team 1 or the allies"""

        all_enemy_locations = self.get_all_enemies(players)
        enemies = {character.name:
                   character for character in players if character.team != 1}
        if self.is_alive:
            if all_enemy_locations:
                if len(all_enemy_locations) == 1:  # if there is only one enemy in the battle:
                    targeted_index = all_enemy_locations[0]
                    targeted_player = players[targeted_index]
                    print('Normal attack: 1')
                    print('Special attack: 2')
                    multiplier_input = blocking_input(['1', '2'])
                    if multiplier_input == '1':
                        self.deal_damage(targeted_player, multiplier=1.0, burn_chance=0)
                    elif multiplier_input == '2':
                        self.deal_damage(targeted_player, multiplier=1.3, burn_chance=10)
                else:  # if there is more than one enemy in the battle:
                    print('Who do you attack?')
                    for player in players:
                        if player.is_alive() and not player.is_ally(self):
                            print(player.name)
                    targeted_enemy = None
                    while targeted_enemy is None:
                        user_input = input('>')
                        targeted_enemy = enemies.get(user_input)
                    print('Normal attack: 1')
                    print('Special attack: 2')
                    multiplier_input = blocking_input(['1', '2'])
                    if multiplier_input == '1':
                        self.deal_damage(other_player=targeted_enemy, multiplier=1.0, burn_chance=0)
                    elif multiplier_input == '2':
                        self.deal_damage(other_player=targeted_enemy, multiplier=1.3, burn_chance=10)

        return players

    def move_input(self):
        """an input at the beginning of the ally turn
        which will ask to either fight, view inventory, or view stats"""
        print('What will you do?')
        print('[f]ight, [i]tem, [s]tats')
        move_input = blocking_input(['f', 'i', 's'])
        if move_input == 'f':
            pass
        elif move_input == 'i':
            self.use_item()
        elif move_input == 's':
            self.get_stats()

    def use_item(self) -> List:
        """How the player can use an item to recover hp"""
        if len(inventory) > 0:
            print(inventory)
            for item in inventory:
                print(f'would you like to use {item}?')
                print('[y]es or [n] no')
                item_input = blocking_input(['y', 'n'])
                if item_input == 'y':
                    if self.hp < self.max_hp:
                        self.hp = min(self.hp + potion.hp_restore, self.max_hp)
                        print(f'{self.name}\'s hp was restored')
                    if self.is_burned is True:
                        if burn_heal.heal_status is True:
                            self.is_burned = False
                            print(f'{self.name}\'s burn was healed')
                        inventory.remove(item)
                    else:  # If the player's hp is already full, they shouldn't be able to use the potion
                        print('It won\'t help')
                elif item_input == 'n':
                    pass
        else:
            print('Your inventory is empty')
        return inventory

    def get_stats(self):
        """prints out the player's important stats"""
        if self.is_alive():
            stats = {
                'name': self.name,
                'hp/max hp': f'{self.hp}/{self.max_hp}',
                'speed': self.speed
            }
            print(stats)
            print()
            return stats


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

    def act(self, players: List['Character']):
        """The act method specific to the enemy characters"""
        all_enemy_locations = self.get_all_enemies(players)
        if all_enemy_locations:
            targeted_index = random.choice(all_enemy_locations)
            targeted_player = players[targeted_index]
            enemy_damage = random.randint(1, 2)
            if enemy_damage == 1:
                self.deal_damage(other_player=targeted_player, multiplier=1.0, burn_chance=0)
            elif enemy_damage == 2:
                self.deal_damage(other_player=targeted_player, multiplier=1.3, burn_chance=10)

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
        """Method to check the player's exp
        add exp when a fight is won
        and level up when the exp reaches it's target value"""
        exp_gain = 200
        for player in self.players:
            if player.is_alive():
                player.exp += exp_gain
                print(f'{player.name} gained {exp_gain} experience points!')
                if player.exp >= player.level_exp:
                    print(f'{player.name} leveled up!')
                    player.level += 1
                    print(f'{player.name} LV: {player.level}')
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
        # Empty print statements are to separate texts in the console
        # To improve readability during the program's running
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
                    acting_player.act(self.players)
                else:
                    print(f'{acting_player.name}\'s turn')
                    acting_player.act(self.players)
                if acting_player.is_burned is True:
                    acting_player.hp -= 1
                    print(f'{acting_player.name} was burned for 1 damage!')
                print()
                for player in self.players:
                    if player.is_alive():
                        print(f'{player.name} LV: {player.level}')
                        print(f'HP: {player.hp}/{player.max_hp}')
                time.sleep(1)
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
    player1 = Ally(name=name, hp=20, max_hp=20, attack=10, speed=2, leveling_rate=1)
    aqua = Ally(name='Aqua', hp=20, max_hp=20, attack=12, speed=3, leveling_rate=2)
    krillin = Enemy(name='Krillin', hp=20, max_hp=20, attack=9, speed=2, leveling_rate=0)
    yamcha = Enemy(name='Yamcha', hp=20, max_hp=20, attack=9, speed=1, leveling_rate=0)
    anime_male = Enemy(name='Anime Male', hp=20, max_hp=20, attack=9, speed=2, leveling_rate=1)
    battle = Battle(players=[player1, aqua, krillin, yamcha])
    potion = Item('potion', hp_restore=7, heal_status=False)
    burn_heal = Item('Burn Heal', hp_restore=0, heal_status=True)
    battle1 = Battle(players=[player1, anime_male])
    battle1.run()
    inventory.append(potion.name)
    inventory.append(burn_heal.name)
    print(f'You found a {potion.name} and a {burn_heal.name}')
    print(f'{aqua.name} joined!')
    battle.run()
    time.sleep(5)
