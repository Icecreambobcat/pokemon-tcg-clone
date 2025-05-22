from __future__ import annotations
from typing import Any, Dict
import pygame as pg

import sys

# implement argparse later

from pygame import (
    display,
    Surface,
    time,
)

from .conf import Config
from .lib import GameState, FS_Daemon


class App:
    screen: Surface
    clock: time.Clock
    state: str
    fps: int
    states: Dict[str, GameState]
    fs_daemon: FS_Daemon
    config: Config

    def __init__(self, args: Dict[str, str | bool | int] = {}) -> None:
        # NOTE: Conditional imports are less expensive

        from states.menu import Menu
        from states.game import Game

        self.config = Config(args)
        if self.config.config["debug"]:
            print(self.config.config)
            print(time.get_ticks())

        pg.init()
        self.screen = display.set_mode(
            (int(self.config.config["width"]), int(self.config.config["height"])),
            vsync=int(self.config.config["vsync"]),
        )
        display.set_caption(str(self.config.config["title"]))
        self.fps = int(self.config.config["fps"])
        self.clock = time.Clock()
        self.fs_daemon = FS_Daemon()
        self.states = {
            "menu": Menu(self.clock, self.fs_daemon, self.config, self.screen),
            "game": Game(self.clock, self.fs_daemon, self.config, self.screen),
        }
        self.state = "menu"

        if self.config.config["debug"]:
            print("Initialized app")
            print(time.get_ticks())
            print(self.__dict__)
        # blah other init stuff

    @staticmethod
    def quit(*args: Any) -> None:
        pg.quit()
        for arg in args:
            print(str(arg))
        sys.exit(0)


def main(config: Dict[str, str | bool | int] = {}) -> None:
    # NOTE: The argparse implementation probably won't work too well with this architecture;
    # configs will be passed directly by the calling script.

    app = App(config)
    quit: bool = False
    while True:
        match app.state:
            case "menu":
                if app.states["menu"].loop():
                    app.state = "game"
                else:
                    quit = True
            case "game":
                if app.states["game"].loop():
                    app.state = "menu"
                else:
                    continue

        display.flip()
        app.clock.tick(app.fps)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit = True
        if quit:
            break

    app.quit("Quit from main loop")
