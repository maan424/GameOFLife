
Entities within this document is supporting the implementations of project assignment.

"""

import os
import sys


STATE_RIM, STATE_DEAD, STATE_ALIVE = '#', '-', 'X'  # base cell states
STATE_ELDER, STATE_PRIME_ELDER = 'E', 'P'           # cell states used for higher grade

"""
    Function:
    "get_print_value()": Used for print out the result as a semi graphical items.
    Som of colors didnt need for basement on "D" Grade.   
    Input: 
    "_val": An string from function ,Progress() to get the intended both, color and state.
    Parameters:
    "STATE_RIM", "STATE_DEAD", "STATE_ALIVE": to keep a color in this case on console printing.
    Return:
    "get_state_color(_val), _val, get_state_color('ENDC')": An string of the current color, state and the end reset
    coloring 
 """
def get_print_value(_val: str) -> str:
    """ Format output value for printing. """
    def get_state_color(state):
        """ Used to color console output. """
        switcher = {
            STATE_RIM: '\033[45m',          # Magenta background color
            STATE_DEAD: '\033[31m',         # Red foreground color
            STATE_ALIVE: '\033[36m',        # Cyan foreground color
            STATE_ELDER: '\033[32m',        # Green foreground color
            STATE_PRIME_ELDER: '\033[34m',  # Blue foreground color
            'ENDC': '\033[0m'               # Reset console color
        }
        return switcher.get(state, None)
    return "{}{}{}".format(get_state_color(_val), _val, get_state_color('ENDC'))


"""
    Function:
    "Progress()": Used for calling function "get print value" to print the intended value.
    Input: 
    "_status": Have three different states to each cell situation as,"RIM CELL", "DEAD CELL", "ALIVE CELL".
    Parameters:"_status"
    Return: None   
 """


def progress(_status: str):
    """ Update progress information in console. """
    if _status == "RIM CELL":
        sys.stdout.write(get_print_value(STATE_RIM))
    elif _status == "DEAD CELL":
        sys.stdout.write(get_print_value(STATE_DEAD))
    elif _status == "ALIVE CELL":
        sys.stdout.write(get_print_value(STATE_ALIVE))


def clear_console():
    """ Clear the console. POSIX refers to OSX/Linux. """
    os.system('clear' if os.name == 'posix' else 'cls')


"""
    Function: 
    "get_pattern()": Used for initialization from gol.py .
    Input: 
    "_pattern": An string with the keys of switcher, as 'gliders', 'pulsar','penta': or None.
    "_world_size": An Tuple som demonstrate the size of outputs, "world".
    Parameters:
    'gliders', 'pulsar','penta': Various patterns from outprintings matters.
    Return: 
    switcher.get(_pattern, None): A switcher of initializations pattern, Requested from project.gol.py.      
 """


def get_pattern(_pattern: str, _world_size: tuple) -> list:
    """ Add predefined pattern to initial seed. """

    def create_gliders() -> list:
        """ Create gliders (simple spaceships) at each corner of the world which will eventually
        collide and spawn other patterns. """

        # world width and height, compensating for rim cells
        _w, _h = _world_size[0] - 1, _world_size[1] - 1

        return [  # creates a glider at each corner of world: NW, NE, SW, SE
            (1, 3), (2, 3), (3, 3), (2, 1), (3, 2),
            (1, _w - 3), (2, _w - 3), (3, _w - 3), (2, _w - 1), (3, _w - 2),
            (_h - 1, 3), (_h - 2, 3), (_h - 3, 3), (_h - 3, 2), (_h - 2, 1),
            (_h - 1, _w - 3), (_h - 2, _w - 3), (_h - 3, _w - 3), (_h - 3, _w - 2), (_h - 2, _w - 1)
        ]

    def create_pulsar() -> list:
        """ Create a pulsar, which is an period 3 oscillator pattern. """
        _vc = int(_world_size[1] * .5)  # vertical center
        _hc = int(_world_size[0] * .5)  # horizontal center

        mapped_vals = {  # map column values to row keys
            1: [2, 3, 4],
            2: [1, 6],
            3: [1, 6],
            4: [1, 6],
            6: [2, 3, 4]
        }

        pulsar = []
        for row, cols in mapped_vals.items():
            for col in cols:
                pulsar.append(tuple((_vc - row, _hc - col)))  # top-left
                pulsar.append(tuple((_vc - row, _hc + col)))  # top-right
                pulsar.append(tuple((_vc + row, _hc - col)))  # bottom-left
                pulsar.append(tuple((_vc + row, _hc + col)))  # bottom-right

        return pulsar

    def create_penta_decathlon() -> list:
        """ Create a Penta-decathlon, which is a 15 period oscillator. """
        _vc = int(_world_size[1] * .5 - 1)  # vertical center
        _hc = int(_world_size[0] * .5)  # horizontal center
        return [
            (_vc - 5, _hc - 1), (_vc - 5, _hc), (_vc - 5, _hc + 1),
            (_vc - 4, _hc), (_vc - 3, _hc),
            (_vc - 2, _hc - 1), (_vc - 2, _hc), (_vc - 2, _hc + 1),

            (_vc, _hc - 1), (_vc, _hc), (_vc, _hc + 1),
            (_vc + 1, _hc - 1), (_vc + 1, _hc), (_vc + 1, _hc + 1),

            (_vc + 3, _hc - 1), (_vc + 3, _hc), (_vc + 3, _hc + 1),
            (_vc + 4, _hc), (_vc + 5, _hc),
            (_vc + 6, _hc - 1), (_vc + 6, _hc), (_vc + 6, _hc + 1)
        ]

    switcher = {
        'gliders': create_gliders(),
        'pulsar': create_pulsar(),
        'penta': create_penta_decathlon()
    }
    return switcher.get(_pattern, None)
