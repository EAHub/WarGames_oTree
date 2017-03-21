# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

from otree.db import models
import otree.models
import otree.constants
from otree import widgets
from otree.common import Currency as c, currency_range
# </standard imports>

doc = """
This bargaining game involves 2 players. Each demands for a portion of some
available amount. If the sum of demands is no larger than the available
amount, both players get demanded portions. Otherwise, both get nothing.
"""

source_code ="https://github.com/oTree-org/oTree/tree/master/bargaining"


class Constants(otree.constants.BaseConstants):
    name_in_url = 'WarGames_Test'
    num_rounds = 1
    # Everyone in one group, but randomly split into teams below
    players_per_group = None
    # Starting War Chests, both at value 100
    team_1_chest_start = c(100)
    team_2_chest_start = c(100)


class Subsession(otree.models.BaseSubsession):
    def before_session_starts(self):
        team_and_role = random.sample([1,0,0,11,10,10], 6)
        index = 0
        for player in self.get_players():
            if (team_and_role[index] == 1):
                player.team = 1
                player.role = 1
                index += 1
            elif (team_and_role[index] < 10):
                player.team = 1
                player.role = 2
                index += 1
            elif (team_and_role[index] == 11):
                player.team = 2
                player.role = 1
                index += 1
            else:
                player.team = 2
                player.role = 2
                index += 1

class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>
    
    def total_requested_1(self):
        sum_1 = 0
        players = self.get_players()
        for p in players:
            if (p.role == 1):
                sum_1 = sum_1 + p.offer_1
        return sum_1
    
    def agreement_status_1(self):
        sum_1 = 0
        players = self.get_players()
        for p in players:
            if (p.role == 1):
                sum_1 = sum_1 + p.offer_1
        if sum_1 > 100:
                return 'There is No Agreement'
        else:
                return 'An Agreement Was Achieved'
    
    def set_payoffs(self):
        players = self.get_players()
        total_requested_amount = sum([p.request_amount for p in players])
        if total_requested_amount <= Constants.amount_shared:
            for p in players:
                p.payoff = p.request_amount + Constants.bonus
        else:
            for p in players:
                p.payoff = Constants.bonus


class Player(otree.models.BasePlayer):
    
    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>
    
    # randomly assigned above in subsession
    team = models.PositiveIntegerField()
    
    # a team name to display to the user
    def team_name(self):
        if self.team == 1:
            return 'Alpha'
        else:
            return 'Beta'

    # randomly assigned above in subsession
    role = models.PositiveIntegerField()

    # a role name to display to the user
    def role_name(self):
        if self.role == 1:
            return 'Leader'
        else:
            return 'Advisor'

    # Bargain 1 advice and final offer
    advice_1 = models.PositiveIntegerField(choices=[10, 20, 30, 40, 50,
                                                    60, 70, 80, 90, 100],
                                             initial=None, blank = True)
                                             
    offer_1 = models.PositiveIntegerField(choices=[10, 20, 30, 40, 50,
                                                   60, 70, 80, 90, 100],
                                             initial=None, blank = True)

    offer_1_retry_1 = models.PositiveIntegerField(choices=[10, 20, 30, 40, 50,
                                                   60, 70, 80, 90, 100],
                                             initial=None, blank = True)

# Change in war chests
# team_1_chest_change_1 = 0
# team_2_chest_change_1 = 0

# def team_1_chest_2(self):
#        return team_1_chest_start + team_1_chest_change_1

#    def team_2_chest_2(self):
#        return team_2_chest_start + team_2_chest_change_1


