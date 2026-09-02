from components.card import Card
from components.items import Item, ItemType
from factions.faction import NullFaction
from board.suit import Suit


_ENVIRONMENT = NullFaction()

BAG: Item = Item(owner=_ENVIRONMENT, itemtype=ItemType.BAG, points=1, suit=Suit.MOUSE)
BOOT: Item = Item(owner=_ENVIRONMENT, itemtype=ItemType.BOOT, points=1, suit=Suit.RABBIT)
CROSSBOW: Item = Item(owner=_ENVIRONMENT, itemtype=ItemType.CROSSBOW, points=1, suit=Suit.FOX)
HAMMER: Item = Item(owner=_ENVIRONMENT, itemtype=ItemType.HAMMER, points=2, suit=Suit.FOX)
SWORD: Item = Item(owner=_ENVIRONMENT, itemtype=ItemType.SWORD, points=2, suit=Suit.FOX)
TEA: Item = Item(owner=_ENVIRONMENT, itemtype=ItemType.TEA, points=2, suit=Suit.MOUSE)
COINS: Item = Item(owner=_ENVIRONMENT, itemtype=ItemType.COINS, points=3, suit=Suit.RABBIT)


BASE_DECK: list[Card] = [
    Card('Stand and Deliver!', Suit.FOX, (Suit.MOUSE, Suit.MOUSE, Suit.MOUSE), persistent=True),
    Card('Stand and Deliver!', Suit.FOX, (Suit.MOUSE, Suit.MOUSE, Suit.MOUSE), persistent=True),
    Card('Sword', Suit.MOUSE, (Suit.FOX, Suit.FOX), SWORD),
    Card('Tax Collector', Suit.FOX, (Suit.RABBIT, Suit.FOX, Suit.MOUSE), persistent=True),
    Card('Tax Collector', Suit.FOX, (Suit.RABBIT, Suit.FOX, Suit.MOUSE), persistent=True),
    Card('Tax Collector', Suit.FOX, (Suit.RABBIT, Suit.FOX, Suit.MOUSE), persistent=True),
    Card('Travel Gear', Suit.FOX, (Suit.RABBIT,), BOOT),
    Card('Travel Gear', Suit.MOUSE, (Suit.RABBIT,), BOOT),
    Card('Woodland Runners', Suit.BIRD, (Suit.RABBIT,), BOOT),
    Card('Ambush!', Suit.BIRD),
    Card('Ambush!', Suit.BIRD),
    Card('Ambush!', Suit.RABBIT),
    Card('Ambush!', Suit.FOX),
    Card('Ambush!', Suit.MOUSE),
    Card('Anvil', Suit.FOX, (Suit.FOX,), HAMMER),
    Card('Armorers', Suit.BIRD, (Suit.FOX,), persistent=False),
    Card('Armorers', Suit.BIRD, (Suit.FOX,), persistent=False),
    Card('Arms Trader', Suit.BIRD, (Suit.FOX, Suit.FOX), SWORD),
    Card('A Visit to Friends', Suit.RABBIT, (Suit.RABBIT,), BOOT),
    Card('Bake Sale', Suit.RABBIT, (Suit.RABBIT, Suit.RABBIT), COINS),
    Card('Better Burrow Bank', Suit.RABBIT, (Suit.RABBIT, Suit.RABBIT), persistent=True),
    Card('Better Burrow Bank', Suit.RABBIT, (Suit.RABBIT, Suit.RABBIT), persistent=True),
    Card('Birdy Bindle', Suit.BIRD, (Suit.MOUSE,), BAG),
    Card('Brutal Tactics', Suit.BIRD, (Suit.FOX, Suit.FOX), persistent=True),
    Card('Brutal Tactics', Suit.BIRD, (Suit.FOX, Suit.FOX), persistent=True),
    Card('Cobbler', Suit.RABBIT, (Suit.RABBIT, Suit.RABBIT), persistent=True),
    Card('Cobbler', Suit.RABBIT, (Suit.RABBIT, Suit.RABBIT), persistent=True),
    Card('Codebreakers', Suit.MOUSE, (Suit.MOUSE,), persistent=True),
    Card('Codebreakers', Suit.MOUSE, (Suit.MOUSE,), persistent=True),
    Card('Command Warren', Suit.RABBIT, (Suit.RABBIT, Suit.RABBIT), persistent=True),
    Card('Command Warren', Suit.RABBIT, (Suit.RABBIT, Suit.RABBIT), persistent=True),
    Card('Crossbow', Suit.BIRD, (Suit.FOX,), CROSSBOW),
    Card('Crossbow', Suit.MOUSE, (Suit.FOX,), CROSSBOW),
    Card('Dominance', Suit.BIRD),
    Card('Dominance', Suit.RABBIT),
    Card('Dominance', Suit.FOX),
    Card('Dominance', Suit.MOUSE),
    Card('Favor of the Foxes', Suit.FOX, (Suit.FOX, Suit.FOX, Suit.FOX), persistent=False),
    Card('Favor of the Mice', Suit.MOUSE, (Suit.MOUSE, Suit.MOUSE, Suit.MOUSE), persistent=False),
    Card('Favor of the Rabbits', Suit.RABBIT, (Suit.RABBIT, Suit.RABBIT, Suit.RABBIT), persistent=False),
    Card('Foxfolk Steel', Suit.FOX, (Suit.FOX, Suit.FOX), SWORD),
    Card('Gently Used Knapsack', Suit.FOX, (Suit.MOUSE,), BAG),
    Card('Investments', Suit.MOUSE, (Suit.RABBIT, Suit.RABBIT), COINS),
    Card('Mouse-in-a-Sack', Suit.MOUSE, (Suit.MOUSE,), BAG),
    Card('Protection Racket', Suit.FOX, (Suit.RABBIT, Suit.RABBIT), COINS),
    Card('Root Tea', Suit.RABBIT, (Suit.MOUSE,), TEA),
    Card('Root Tea', Suit.FOX, (Suit.MOUSE,), TEA),
    Card('Root Tea', Suit.MOUSE, (Suit.MOUSE,), TEA),
    Card('Royal Claim', Suit.BIRD, (Suit.WILD, Suit.WILD, Suit.WILD, Suit.WILD), persistent=True),
    Card('Sappers', Suit.BIRD, (Suit.MOUSE,), persistent=True),
    Card('Sappers', Suit.BIRD, (Suit.MOUSE,), persistent=True),
    Card('Scouting Party', Suit.MOUSE, (Suit.MOUSE, Suit.MOUSE), persistent=True),
    Card('Scouting Party', Suit.MOUSE, (Suit.MOUSE, Suit.MOUSE), persistent=True),
    Card("Smuggler's Trail", Suit.RABBIT, (Suit.MOUSE,), BAG)
]