from typing import Dict
import pygame as pg

# import argparse
# implement argparse later

from pygame import (
    Color,
    display,
    event,
    font,
    image,
    key,
    mouse,
    mixer,
    Rect,
    sprite,
    Surface,
    time,
)

from app.conf import Config
from app.lib import GameState
from states.menu import Menu
from states.game import Game


class App:
    screen: Surface
    clock: time.Clock
    fonts: Dict[str, font.Font]
    state: str
    states: Dict[str, GameState]
    config: Config

    def __init__(self) -> None:
        pg.init()
        # blah other init stuff


def main() -> None:
    # init the app & do argparse cringe
    pass


if __name__ == "__main__":
    main()
