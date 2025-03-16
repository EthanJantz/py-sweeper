# py-sweeper

I've been wanting to dive further into python lately to get more familiar with OOP principles and this is the project I ended up deciding to work on. This project is a basic implementation of Minesweeper written from scratch in python. Tests for core gameplay functions were written using `pytest`. 

## Setup

Clone this repository:

```git clone https://github.com/EthanJantz/py-sweeper.git```

Set up a virtual environment, acivate it, and install the necessary packages using `pip install -r requirements.txt`. 

Begin playing by running `src/minesweeper.py`. 

## Gameplay

Currently the difficulty is hardcoded as a 10x10 board with 15 mines. When loading the game, the user is prompted to select a cell before the board is generated. The player continues to reveal cells until they reveal a mine or all cells without mines have been revealed. 