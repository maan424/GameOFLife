
"""
The universe of the Game of Life is an infinite two-dimensional orthogonal grid of square cells,
each of which is in one of two possible states, alive or dead (populated or unpopulated).
Every cell interacts with its eight neighbours, which are the cells that are horizontally,
vertically, or diagonally adjacent.

At each step in time, the following transitions occur:

****************************************************************************************************
   1. Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
   2. Any live cell with two or three live neighbours lives on to the next generation.
   3. Any live cell with more than three live neighbours dies, as if by overpopulation.
   4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
****************************************************************************************************

The initial pattern constitutes the seed of the system.

The first generation is created by applying the above rules simultaneously to every cell in the
seed—births and deaths occur simultaneously, and the discrete moment at which this happens is
sometimes called a tick. The rules continue to be applied repeatedly to create further generations.

You run this script as a module:
    python -m Project.gol
"""
import sys
import argparse
import random
import itertools
from pathlib import Path
from _Resources import code_base as cb
import time


__version__ = '1.0'
__desc__ = "A simplified implementation of Conway's Game of Life."

RESOURCES = Path(__file__).parent / "../_Resources/"

"""
    Function: 
    "parse_world_size_arg()": Determine dimensions of the outputs world.
    Input: 
    "_arg": An string readable from console.    
    Parameters:
    "second_value","first_value": (width, height),Decide from this function or get as defaulted som 80x40.
    "_sub_all": _arg will be partitions after and before "x" from given string(_arg).
    Return: 
    _world_size_tuple: A Tuple in format "aaxaa" to get both width and height after calling from another functions .      
 """


def parse_world_size_arg(_arg: str) -> tuple:
    """ Parse width and height from command argument. """

    first_value = 80
    second_value = 40
    _sub_all = _arg.partition("x")
    if _sub_all[2].isnumeric() and len(_sub_all[2]) == 2 and _sub_all[1] == "x" and _sub_all[0] != "" and _sub_all[
        2] != "" and int(_sub_all[0]) > 1 and int(_sub_all[2]) > 1:
        first_value = int(_sub_all[0])
        second_value = int(_sub_all[2])
    elif (not _sub_all[2].isnumeric()) and len(_sub_all[2]) == 2 and _sub_all[1] == "x":
        raise ValueError(f"invalid literal for int() with base 10:\"{_sub_all[2]}\"\n Using default world size: 80x40")
    elif (not _sub_all[2].isnumeric()) or _sub_all[1] != "x" or _sub_all[0] == "" or _sub_all[2] == "":
        raise AssertionError(
            "World size should contain width and height, separated by ‘x’. Ex: ‘80x40’\n Using default world size: 80x40")
    elif int(_sub_all[0]) <= 0 or int(_sub_all[2]) <= 0:
        raise ValueError(
            "Both width and height needs to have positive values above zero.\n Using default world size: 80x40")
    _world_size_tuple = (first_value, second_value)
    return _world_size_tuple


"""
    Function: 
    "populate_world()": Determine dimensions of the outputs world.

    Input: 
    "_world_size": An string readable from the console.
    "_seed_pattern": Get from code_base.py   
    Parameters:
    "_list_1","_list_2": All points (x,y) without the RIMs.
    "_count_1x", "_count_2x", "_count_3x", "_count_4x": Simple counter in the loops.
    "population_rim", "population_dead, "population_alive": Counting of every set of cells
    "_pattern_list": Because there is different to use 'gliders', 'pulsar','penta' in this function
                     make a list to check every points initial from code_base.py to get correct position.
    "_make_iter": A list maker for get intended pattern.
    Return: 
    "_population_all": A dictionary contains of DEAD and ALIVE cells and theirs neighbours.
"""


def populate_world(_world_size: tuple, _seed_pattern: str = None) -> dict:
    """ Populate the world with cells and initial states."""
    _population_all = {}
    _world_size_new = (_world_size[1], _world_size[0])
    _population_all["world_size"] = _world_size_new
    _list_1 = list(range(1, _world_size_new[0] - 1))
    _list_2 = list(range(1, _world_size_new[1] - 1))
    population_rim, population_dead, population_alive, _pattern_list, _make_iter = [], [], [], [], []
    _count_1x, _count_2x, _count_3x, _count_4x = 0, 0, 0, 0

    while _count_2x < _world_size_new[1]:
        cb.progress("RIM CELL")
        population_rim.append(tuple((0, _count_2x)))
        _population_all[tuple((0, _count_2x))] = None
        _count_2x += 1
    sys.stdout.write('\n')
    while _count_1x < len(_list_1):
        _make_iter = []
        _make_iter.append(_list_1[_count_1x])
        _iter = itertools.product(_make_iter, _list_2)
        cb.progress("RIM CELL")
        population_rim.append(tuple((_count_1x + 1, 0)))
        _population_all[tuple((_count_1x + 1, 0))] = None
        for _members in _iter:
            if _seed_pattern != 'gliders' and _seed_pattern != 'pulsar' and _seed_pattern != 'penta':
                if int(random.randint(0, 20)) > 16:
                    cb.progress("ALIVE CELL")
                    population_alive.append(_members)
                else:
                    cb.progress("DEAD CELL")
                    population_dead.append(_members)
            else:
                while _count_4x < len(cb.get_pattern(_seed_pattern, _world_size_new)):
                    _temple1 = cb.get_pattern(_seed_pattern, _world_size_new)[_count_4x][0]
                    _temple2 = cb.get_pattern(_seed_pattern, _world_size_new)[_count_4x][1]
                    if _seed_pattern == 'gliders' or _seed_pattern == 'pulsar':
                        _par = (_temple2, _temple1)
                        _pattern_list.append(_par)
                    elif _seed_pattern == 'penta':
                        _par = (_temple1 - int(_world_size_new[0] * .5), _temple2 + int(_world_size_new[0] * .5))
                        _pattern_list.append(_par)
                    _count_4x += 1
                if _members in _pattern_list:
                    cb.progress("ALIVE CELL")
                    population_alive.append(_members)
                else:
                    cb.progress("DEAD CELL")
                    population_dead.append(_members)

        cb.progress("RIM CELL")
        population_rim.append(tuple((_count_1x + 1, _world_size_new[1] - 1)))
        _population_all[tuple((_count_1x + 1, _world_size_new[1] - 1))] = None
        sys.stdout.write('\n')
        _make_iter = []
        _count_1x += 1
    # **********************************************************************************************
    while _count_3x < _world_size_new[1]:
        cb.progress("RIM CELL")
        population_rim.append(tuple(([_world_size_new[0] - 1, _count_3x])))
        _population_all[tuple((_world_size_new[0] - 1, _count_3x))] = None
        _count_3x += 1
    sys.stdout.write('\n')

    # *******************************************************************************************************
    # Count alive cells neighbours
    for _alive in population_alive:
        _population_all[_alive] = {"state": "X",
                                   "neighbours": list(set(calc_neighbour_positions(_alive)) - set(population_rim))}
    # *******************************************************************************************************
    # Count dead cells neighbours

    for _dead in population_dead:
        _population_all[_dead] = {"state": "-",
                                  "neighbours": list(set(calc_neighbour_positions(_dead)) - set(population_rim))}
    count_alive_neighbours(_make_iter, _population_all)
    # *******************************************************************************************************
    return _population_all


"""
    Function: 
    "calc_neighbour_positions": Counting all neighbours in both initial function and run function.
    Input: 
    "_cell_coord": A tuple contains Coordinates of every points to count neighbours.  
    Parameters:
    "_list_neighbour": All neighbours ass a list.
    Return: 
    " _list_neighbour": Return a list of all neighbours.
"""


def calc_neighbour_positions(_cell_coord: tuple) -> list:
    """ Calculate neighbouring cell coordinates in all directions (cardinal + diagonal).
    Returns list of tuples. """
    _list_neighbour = []
    _list_neighbour.append(tuple((_cell_coord[0] - 1, _cell_coord[1] - 1)))
    _list_neighbour.append(tuple((_cell_coord[0], _cell_coord[1] - 1)))
    _list_neighbour.append(tuple((_cell_coord[0] + 1, _cell_coord[1] - 1)))
    _list_neighbour.append(tuple((_cell_coord[0] - 1, _cell_coord[1] + 1)))
    _list_neighbour.append(tuple((_cell_coord[0], _cell_coord[1] + 1)))
    _list_neighbour.append(tuple((_cell_coord[0] + 1, _cell_coord[1] + 1)))
    _list_neighbour.append(tuple((_cell_coord[0] - 1, _cell_coord[1])))
    _list_neighbour.append(tuple((_cell_coord[0] + 1, _cell_coord[1])))
    return _list_neighbour


"""
    Function: 
    "run_simulation()": Determine how many times the world will calling and updated.
    Input: 
    "_nth_generation": An integer of times that the world would be updated.
    "_population": The initialed world. 
    "_world_size":  
    Parameters:
    "_counter_run ": A simple counter to the "while" loop.
    "time.sleep", time between two updates, 200 ms.
    Return: 
    "_population_all": A dictionary contains of DEAD and ALIVE cells and theirs neighbours.
"""


def run_simulation(_nth_generation: int, _population: dict, _world_size: tuple):
    """ Runs simulation for specified amount of generations. """
    _counter_run = 0
    while _counter_run < _nth_generation:
        cb.clear_console()
        update_world(_population, _world_size)
        time.sleep(0.2)
        _counter_run += 1


"""
    Function: 
    "update_world()": Determine the times world will be updated.
    Input: 
    "_world_size": An string readable from the console.
    "_cur_gen": Get from initial function,populate_world().  
    Parameters:
    "_list_1","_list_2": All points (x,y) without the RIMs.
    "_count_1x", "_count_2x", "_count_3x": Simple counter in the loops.
    "population_rim", "population_dead, "population_alive": Counting of every set of cells
    "_pattern_list": Because there is different to use 'gliders', 'pulsar','penta' in this function
                     make a list to check every points initial from code_base.py to get correct position.
    "_make_iter": A list maker for get intended pattern.
    Return: 
    "_population_all": A dictionary contains of DEAD and ALIVE cells and theirs neighbours.
"""


def update_world(_cur_gen: dict, _world_size: tuple) -> dict:
    """ Represents a tick in the simulation. """
    _world_size_new = (_world_size[1], _world_size[0])
    _population_all = _cur_gen
    _population_all["world_size"] = _world_size_new
    population_rim, population_dead, population_alive, _make_iter = [], [], [], []
    _count_1x, _count_2x, _count_3x = 0, 0, 0
    # *************************************************************************************************
    _list_1 = list(range(1, _world_size_new[0] - 1))
    _list_2 = list(range(1, _world_size_new[1] - 1))
    # *************************************************************************************************
    while _count_2x < _world_size_new[1]:
        cb.progress("RIM CELL")
        population_rim.append(tuple((0, _count_2x)))
        _population_all[tuple((0, _count_2x))] = None
        _count_2x += 1
    sys.stdout.write('\n')
    while _count_1x < len(_list_1):
        _make_iter.append(_list_1[_count_1x])
        _iter = itertools.product(_make_iter, _list_2)
        # sys.stdout.write(cb.get_print_value(STATE_RIM))
        cb.progress("RIM CELL")
        population_rim.append(tuple((_count_1x + 1, 0)))
        _population_all[tuple((_count_1x + 1, 0))] = None
        for _new_pos in _iter:
            _counter_Neigh = 0
            _counter_nej = 0
            if _population_all[tuple(_new_pos)]["state"] == "X":
                _counter_Neigh = 0
                _counter_nej = 0
                while _counter_nej < len(_population_all[tuple(_new_pos)]["neighbours"]):
                    x = _population_all[tuple(_new_pos)]["neighbours"][_counter_nej]
                    if _population_all[tuple(x)]["state"] == "X":
                        _counter_Neigh += 1
                    _counter_nej += 1
                if _counter_Neigh == 2 or _counter_Neigh == 3:
                    population_alive.append(_new_pos)
                    cb.progress("ALIVE CELL")
                    _counter_Neigh = 0
                    _counter_nej = 0
                else:
                    population_dead.append(_new_pos)
                    cb.progress("DEAD CELL")
                    _counter_Neigh = 0
                    _counter_nej = 0

            if _population_all[_new_pos]["state"] == "-":
                _counter_nej = 0
                _counter_Neigh = 0
                while _counter_nej < len(_population_all[_new_pos]["neighbours"]):
                    x = _population_all[_new_pos]["neighbours"][_counter_nej]
                    if _population_all[x]["state"] == "X":
                        _counter_Neigh += 1
                    _counter_nej += 1
                if _counter_Neigh == 3:
                    population_alive.append(_new_pos)
                    cb.progress("ALIVE CELL")
                    _counter_Neigh = 0
                    _counter_nej = 0
                else:
                    population_dead.append(_new_pos)
                    cb.progress("DEAD CELL")
                    _counter_Neigh = 0
                    _counter_nej = 0
        cb.progress("RIM CELL")
        population_rim.append(tuple((_count_1x + 1, _world_size_new[1] - 1)))
        _population_all[tuple((_count_1x + 1, _world_size_new[1] - 1))] = None
        sys.stdout.write('\n')
        _make_iter = []
        _count_1x += 1
    # *******************************************************************************************************
    while _count_3x < _world_size_new[1]:
        cb.progress("RIM CELL")
        population_rim.append(tuple(([_world_size_new[0] - 1, _count_3x])))
        _population_all[tuple((_world_size_new[0] - 1, _count_3x))] = None
        _count_3x += 1
    sys.stdout.write('\n')
    # *******************************************************************************************************
    # Count alive cells neighbours

    for _alive in population_alive:
        _population_all[_alive] = {"state": "X",
                                   "neighbours": list(set(calc_neighbour_positions(_alive)) - set(population_rim))}
    # *******************************************************************************************************
    # Count dead cells neighbours

    for _dead in population_dead:
        _population_all[_dead] = {"state": "-",
                                  "neighbours": list(set(calc_neighbour_positions(_dead)) - set(population_rim))}
    count_alive_neighbours(_make_iter, _population_all)
    # *******************************************************************************************************
    return _population_all


"""
    Function: 
    "count_alive_neighbours()": Counting of alive cells after each update.
    Input: 
    "_neighbours": A list of neighbours.
    "_cells": A dictionary shows all DEAD, ALIVE cells and their neighbours. 
    Parameters:
    "__count_alive": A simple counter.
    Return: 
    "_count_alive": A integer shows how many ALIVE cells.
"""


def count_alive_neighbours(_neighbours: list, _cells: dict) -> int:
    """ Determine how many of the neighbouring cells are currently alive. """
    population_all = itertools.product(list(range(1, _cells["world_size"][0] - 1)),
                                       list(range(1, _cells["world_size"][1] - 1)))
    _count_alive = 0
    for _coord in population_all:
        if _cells[_coord]["state"] == "X":
            _count_alive += 1
    return _count_alive


def main():
    """ """
    epilog = "DT179G Project v" + __version__
    parser = argparse.ArgumentParser(description=__desc__, epilog=epilog, add_help=True)
    parser.add_argument('-g', '--generations', dest='generations', type=int, default=50,
                        help='Amount of generations the simulation should run. Defaults to 50.')
    parser.add_argument('-s', '--seed', dest='seed', type=str,
                        help='Starting seed. If omitted, a randomized seed will be used.')
    parser.add_argument('-ws', '--worldsize', dest='worldsize', type=str, default='80x40',
                        help='Size of the world, in terms of width and height. Defaults to 80x40.')
    parser.add_argument('-f', '--file', dest='file', type=str,
                        help='Load starting seed from file.')
    args = parser.parse_args()
    try:
        if not args.file:
            raise AssertionError
        population, world_size = load_seed_from_file(args.file)
    except (AssertionError, FileNotFoundError):
        world_size = parse_world_size_arg(args.worldsize)
        if args.generations != 0:
            population = populate_world(world_size, args.seed)
    if args.generations != 0:
        run_simulation(args.generations, population, world_size)


if __name__ == "__main__":
    main()
