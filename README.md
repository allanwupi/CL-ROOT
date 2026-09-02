# Command-Line Root

This Python program simulates the board game Root with Clockwork Expansion bots. Bots are based on the [Clockwork: Definitive Edition playtest boards](https://boardgamegeek.com/thread/2068034/better-bot-project-24082026-new-catalliancemolecro), published on 24 August 2026.

## Goals 
- Implement a command-line version of the board game Root, conforming as closely as possible to the [official rulebook](https://rules.ledergames.com/?product=root&locale=en-US&printing=p16) from Leder Games.
    - Run the simulation and watch bot factions play against each other
    - Input Python commands to inspect objects and manually control the factions
    - Eventually support rules for playing as a human faction against the bots
- Learn and practise the object-oriented programming paradigm in Python
- (tentatively, in the far future) Learn more logic programming and rewrite this in Prolog

## Current features
- Autumn map and base deck only
- No system for crafting costs at the moment
  - Only items are craftable
- No persistent effects (including dominance victory condition) have been implemented
- Battle system does not include ambushes
- Mechanical Marquise bot (24-08-2026 version) implementation in progress

### Future improvements
- I need to implement better turn tracking (would like to plot faction VP over time)
- I would like to track pieces' complete history over time
    - This is needed to adhere to a stipulation of the Mechanical Marquise's board that pieces cannot move twice in a turn
- System architecture for faction abilities and modifiers is completely in the air
- Currently the map ASCII art is a long multi-line f-string; it may be worth looking at algorithms for drawing edges in the future
