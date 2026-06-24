# Robot Coin Collector Game

A 2D game developed in Python, featuring a robot that explores a tile-based map, collects coins, and avoids or fights monsters using simple mechanics.

## Overview

The player controls a robot navigating a grid-based world. The goal is to collect coins while avoiding monsters that actively chase the player using pathfinding logic.

As the game progresses, both the player and enemies gradually increase in speed, making the game progressively more challenging.

Players can also:

* Use doors to teleport across the map
* Destroy monsters after collecting every 5 coins, adding a risk–reward combat mechanic

The game demonstrates core programming and game development concepts such as:

* OOP
* Game loops and real-time updates
* Tile-based map systems
* Basic AI behavior
* Pathfinding (A* algorithm)
* Collision detection
* Event handling

## Features

### Player Mechanics

* Moveable robot character
* Coin collection system
* Teleportation via doors
* Score tracking (coins collected, monsters killed)

### Enemy

* Monsters spawn periodically
* Chase the player using pathfinding
* Dynamic speed changes based on gameplay conditions
* Player can eliminate monsters under specific conditions

### Map System

* Grid-based world
* Walls that block movement in specific directions

### Pathfinding

* Implementation of A* algorithm
* Monsters recalculate paths at regular intervals
* Movement constrained by map connectivity

## Technologies Used

* Python
* Pygame
