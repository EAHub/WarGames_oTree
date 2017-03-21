# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants


def vars_for_all_templates(self):
    return {'team_1_chest_start': Constants.team_1_chest_start,
            'team_2_chest_start': Constants.team_2_chest_start}


class Consent(Page):
    pass

class Assignments(Page):
    pass

class Chest_1(Page):
    pass

class Advice_1(Page):
    form_model = models.Player
    form_fields = ['advice_1']

class Wait(WaitPage):
    def after_all_players_arrive(self):
        pass

class Offer_1(Page):
    form_model = models.Player
    form_fields = ['offer_1']

class Compare_1(Page):
    pass


class Offer_1_Retry_1(Page):
    def is_displayed(self):
        return self.group.total_requested_1 > 100
    form_model = models.Player
    form_fields = ['offer_1_retry_1']

class Offer_1_Agreed(Page):
    def is_displayed(self):
        return self.group.total_requested_1 <= 100

class Offer_1_War(Page):
    def is_displayed(self):
        return self.group.total_requested_1 > 100


# Here we outline the order of viewing
page_sequence=[
        Consent,
        Assignments,
        Chest_1,
        Advice_1,
        Wait,
        Offer_1,
        Wait,
        Compare_1,
        Offer_1_Retry_1,
        Offer_1_Agreed,
        Offer_1_War
        
    ]
