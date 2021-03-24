"""
Database class that creates and stores every card in a deck
"""

from Cards import *
import random


class Deck:

    def __init__(self):
        self.level1 = []
        self.level2 = []
        self.level3 = []
        self.hidden = []

    def draw(self, level):
        if level == 1:
            card = random.choice(self.level1)
        elif level == 2:
            card = random.choice(self.level2)
        else:
            card = random.choice(self.level3)
        return card

    def loadCards(self):
        self.level1 = loadOne()
        self.level2 = loadTwo()
        self.level3 = loadThree()
        self.hidden = loadHidden()


donation = SmallDonation("donation", "img/cards/1.png")
small_steal = SmallSteal("small steal", "img/cards/2.png")
high_five = HighFive("high five", "img/cards/3.png")
take_5 = TakeFive("take 5", "img/cards/4.png")
jackpot = Jackpot("jackpot", "img/cards/5.png")
wdmeg = WhereDidMyElementsGo("wdmeg", "img/cards/6.png")
bomb = Bomb("bomb", "img/cards/7.png")
bad_luck = BadLuck("bad luck", "img/cards/8.png")
hoover = Hoover("hoover", "img/cards/9.png")
one_more = OneMore("one more", "img/cards/10.png")
reverse = Reverse("reverse", "img/cards/11.png")
defense = Defense("defense", "img/cards/12.png")
special_gift = SpecialGift("special gift", "img/cards/13.png")
more_special = MoreSpecial("more special", "img/cards/14.png")
wow = Wow("wow", "img/cards/15.png")
swapper = Swapper("swapper", "img/cards/16.png")

block = Block("block", "img/cards/17.png", 1, 0.25)
empty_v1 = Empty("empty", "img/cards/18.png", 1, 0.25)
take_v1 = Take("take", "img/cards/19.png", 1, 0.25)
remove = Remove("remove", "img/cards/20.png", 1, 0.25)

camouflage = Camouflage("camouflage", "img/cards/21.png", 2, 0.20)
booster_v2 = Booster("booster", "img/cards/22.png", 2, 0.15)
empty_v2 = Empty("empty", "img/cards/18(2).png", 2, 0.10)
steal = Steal("steal", "img/cards/23.png", 2, 0.20)
take_v2 = Take("take", "img/cards/25.png", 2, 0.35)

booster_v3 = Booster("booster", "img/cards/22(2).png", 3, 0.30)
rob_the_bank = RobTheBank("rtb", "img/cards/27.png", 3, 0.20)
clean = Clean("clean", "img/cards/28.png", 3, 0.25)
i_need_you_score = ScoreSwap("score", "img/cards/29.png", 3, 0.15)
how_did_that_happen = PlayersSwap("swap", "img/cards/30.png", 3, 0.10)



def loadHidden():
    cards = [donation, small_steal, high_five, take_5, jackpot, wdmeg, bomb, bad_luck,
             hoover, one_more, reverse, defense, special_gift, more_special, wow, swapper]
    return cards


def loadOne():
    cards = [block, empty_v1, take_v1, remove]
    return cards


def estimate(card):
    cards = []
    for i in range(int(card.prob*20)):
        cards += [card]
    return cards


def loadTwo():
    cards = []
    for card in [camouflage, booster_v2, empty_v2, steal, take_v2]:
        cards += estimate(card)
    return cards


def loadThree():
    cards = []
    for card in [booster_v3, rob_the_bank, how_did_that_happen, i_need_you_score, clean]:
        cards += estimate(card)
    return cards
