# Python Text RPG Tyler

# Import Statements

import time
from typing import List, Tuple
from queue import PriorityQueue
from dataclasses import dataclass, field
import copy


# Input blocker (Prevents the user from inputting invalid responses)
def blocking_input(acceptable_responses: [str]) -> str:
    """Returns input{'>') until an acceptable response is inputted"""
    while True:
        output = input('>')
        if output in acceptable_responses:
            break
    return output


class Player:
    def __init__(self, name: str, team: int):
        self.name = name
        self.team = team
        self.max_hp = 1200
        self.hp = self.max_hp
        self.attack = 55
        self.speed = 10
        self.status_effects = []
        self.splash = False
        self.level = 1
        self.xp = 0
        self.lv_xp = 200


you = Player('You', 1)
enemy = Player('Enemy', 2)


class Cards:
    def __init__(self,
                 name: str,
                 max_hp: int,
                 hp: int,
                 attack: int,
                 speed: int,
                 status_effects: list,
                 splash: bool,
                 team: int):
        self.name = name
        self.max_hp = max_hp
        self.hp = hp
        self.attack = attack
        self.speed = speed
        self.status_effects = status_effects
        self.splash = splash
        self.team = team
        self.level = 1
        self.card_num = 0
        self.tar_card_num = 2

    def is_alive(self) -> bool:
        """returns true if the card/tower is alive"""
        return self.hp > 0

    def is_ally(self, other_unit) -> bool:
        """returns true if two objects are on the same team"""
        return other_unit.team == self.team

    def deal_damage(self, other_unit):
        """deals damage to another unit or player"""
        if other_unit.is_alive():
            other_unit.hp -= self.attack
            print(f'{self.name} attacked {other_unit.name}')
        return other_unit

    def get_all_enemy_indices(self, units: List['Cards']) -> List[int]:
        """returns a list of indexes of all the enemies"""
        return [
            index for index, unit in enumerate(units)
            if unit.is_alive and not unit.is_ally(self)
        ]

    def act(self, units: List) -> List:
        """The method in which a unit acts."""
        all_enemy_locations = self.get_all_enemy_indices(units=units)
        if all_enemy_locations:
            targeted_index = all_enemy_locations[0]
            targeted_card = units[targeted_index]
            damaged_card = self.deal_damage(targeted_card)
            units[targeted_index] = damaged_card
            if self.splash is True:  # If the unit does splash damage
                for i in range(3):
                    targeted_indexes = all_enemy_locations[i]
                    targeted_cards = units[targeted_indexes]
                    damaged_cards = self.deal_damage(targeted_cards)
                    units[targeted_indexes] = damaged_cards
        return units


@dataclass(order=True)
class Move:
    priority: float
    unit: Cards = field(compare=False)


class Battle:
    """The list of characters and order of their moves"""
    def __init__(self, units: List['Cards']):
        self.units = units
        self.q = PriorityQueue()

    def add_into_queue(self, unit: Cards, game_time: int) -> None:
        move = Move(priority=game_time + 1.0/unit.speed, unit=unit)
        self.q.put(move)

    def get_from_queue(self) -> Tuple[Cards, int]:
        move = self.q.get()
        return move.unit, move.priority

    def is_over(self) -> bool:
        """returns true when the battle is over"""
        return self.q.empty()

    def run(self):
        for unit in self.units:
            self.add_into_queue(unit=unit, game_time=0)
        while not self.is_over():
            acting_unit, current_game_time = self.get_from_queue()
            print()
            if acting_unit.is_alive():
                acting_unit.act(self.units)
            if acting_unit.is_alive and acting_unit.get_all_enemy_indices(self.units):
                self.add_into_queue(acting_unit, current_game_time)
            else:
                print(f'{acting_unit.name} is out of play')
        print('Match Over')


arch = Cards(name='Archer', max_hp=240, hp=240, attack=70, speed=12,
             status_effects=[], splash=False, team=1)
wizz = Cards(name='Wizard', max_hp=400, hp=400, attack=170, speed=14,
             status_effects=[], splash=True, team=1)
mega_min = Cards(name='Mega Minion', max_hp=490, hp=490, attack=152, speed=16,
                 status_effects=[], splash=False, team=1)
arch2 = copy.deepcopy(arch)
arch2.team = 2
wizz2 = copy.deepcopy(wizz)
wizz2.team = 2
mega_min2 = copy.deepcopy(mega_min)
mega_min2.team = 2

battle = Battle(units=[arch, wizz, mega_min, arch2, wizz2, mega_min2])
battle.run()


























































