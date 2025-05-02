from __future__ import annotations
from typing import Any, Dict
import pygame as pg

import argparse, sys

# implement argparse later

from pygame import (
    display,
    Surface,
    time,
)

from app.conf import Config
from app.lib import GameState, FS_Daemon
from states.menu import Menu
from states.game import Game


class App:
    screen: Surface
    clock: time.Clock
    state: str
    fps: int
    states: Dict[str, GameState]
    fs_daemon: FS_Daemon
    config: Config

    def __init__(self, args: Dict[str, str | bool | int] = {}) -> None:
        self.config = Config(args)
        if self.config.config["debug"]:
            print(self.config.config)

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

        # blah other init stuff

    @staticmethod
    def quit(*args: Any) -> None:
        pg.quit()
        for arg in args:
            print(str(arg))
        sys.exit(0)


def main() -> None:
    # init the app & do argparse cringe
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", "-w", type=int, help="Window width")
    parser.add_argument("--height", "-h", type=int, help="Window height")
    parser.add_argument("--fps", "-f", type=int, help="Frames per second")
    parser.add_argument("--debug", "-d", action="store_true", help="Debug mode")
    parser.add_argument("--vsync", "-s", action="store_true", help="Vsync")
    parser.add_argument(
        "--title", "-t", type=str, action="store", help="Change the title (str input)"
    )
    args: Dict[str, str | bool | int] = vars(parser.parse_args())

    app = App(args)
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


if __name__ == "__main__":
    main()
