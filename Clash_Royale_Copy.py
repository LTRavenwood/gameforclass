# Python RPG

# Import statements-----------------------------------------------------------------------------------------------------
import cmd
import os
import sys
import time
import random
import textwrap


# Setting up the Character---------------------------------------------------------------------------------------------


def input_blocker(acceptable_responses: [str]) -> str:
    """Returns input('>') until player picks an acceptable response"""
    while True:
        output = input('>')
        if output in acceptable_responses:
            break
    return output


class Card:
    """All the parameters of a single unit"""
    def __init__(self,
                 name: str,
                 max_hp: int,
                 hp: int,
                 attack: int,
                 speed: float,
                 team: int,
                 splash: bool):
        self.name = name
        self.max_hp = max_hp
        self.hp = hp
        self.attack = attack
        self.speed = speed
        self.team = team
        self.splash = splash
        self.level = 1
        self.card_num = 0
        self.max_card_num = 2

    def is_alive(self) -> bool:
        """returns true if the unit is alive"""
        return self.hp > 0

    def is_ally(self, other_unit) -> bool:
        """returns true if two units are on the same team"""
        return other_unit.team == self.team

    def deal_damage(self, other_unit):
        if other_unit.is_alive():
            other_unit.hp -= self.attack
            print(f'{self.name} attacked, {other_unit.name}!')
        return other_unit

    def get_all_enemy_indices(self, units: List['Card']) -> List[int]:
        return [
            index for index, unit in enumerate(units)
            if unit.is_alive and not unit.is_ally(self)
        ]
    def act(self, units: List):
        all_enemy_locations = self.get_all_enemy_indices(units=self.units)


arch = Card(name='Archer', max_hp=240, hp=240, attack=70, speed=12, splash=False, team=1)
wizz = Card(name='Wizard', max_hp=400, hp=400, attack=170, speed=14, splash=True, team=1)

arch.deal_damage(wizz)
wizz.deal_damage(arch)