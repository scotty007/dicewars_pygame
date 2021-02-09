# dicewars_pygame #

A DiceWars game GUI (frontend) for
[*dicewars*](https://github.com/scotty007/dicewars),
based on [*pygame*](https://www.pygame.org).

**dicewars_pygame** runs **single player vs. up to 7 AI players** matches.
It should work on all platforms supported by
[*pygame*](https://www.pygame.org/wiki/GettingStarted)
and Python>=3.7.

![start screen](screenshot_01.png 'Start screen')

![match screen](screenshot_02.png 'Match screen')

## Installation & Start ##

The following commands may (or should) be executed in a Python 3 virtual env.

**dicewars_pygame** can be started w/o installation from inside the
top-level source directory:

    $ pip install -r requirements.txt
    $ python -m dicewars_pygame.main

### Installation from PyPI ###

**dicewars_pygame** is available on
[The Python Package Index](https://pypi.org/project/dicewars_pygame/):

    $ pip install dicewars_pygame
    $ dicewars_pygame

### Installation from source ###

    $ pip install .
    # or
    $ python setup.py install
    # then
    $ dicewars_pygame

### Options ###

Attack/supply step intervals during matches can be adjusted via the
``-i``/``--interval`` command line argument. The sound effects volume
can be reduced via ``-v``/``--volume``.

## Licenses ##

**dicewars_pygame** is distributed under the terms of the
[GPLv3+](https://www.gnu.org/licenses/gpl-3.0).

All sound files are created using
[sfxr-sdl2](https://github.com/tjohnman/sfxr-sdl2)
and licensed under the
[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).

The Anton font is licensed by The Anton Project Authors under the
[OFL v1.1](http://scripts.sil.org/OFL).
