from __future__ import annotations
from typing import Dict, Tuple
import pygame as pg
from pygame import Surface, display, time, transform

from app.conf import Config
from app.lib import FS_Daemon, GameState


class Menu(GameState):
    def __init__(
        self, clock: time.Clock, fsd: FS_Daemon, config: Config, screen: Surface
    ) -> None:
        from app.lib import Helpers

        # private
        self._clock = clock
        self._fsd = fsd
        self._conf = config
        self._scr = screen

        if self.config.config["debug"]:
            print("Loaded private menu vars")

        # sect: images
        self.bg = transform.scale(
            self.fs_daemon.images["menubg"],
            (int(self.config.config["width"]), int(self.config.config["height"])),
        )

        # sect: fonts
        self.font4 = self.fs_daemon.fonts["JetBrainsMonoNerdFont-regular"][3]
        self.font3 = self.fs_daemon.fonts["JetBrainsMonoNerdFont-regular"][2]
        self.font2 = self.fs_daemon.fonts["JetBrainsMonoNerdFont-regular"][1]
        self.font1 = self.fs_daemon.fonts["JetBrainsMonoNerdFont-regular"][0]

        if self.config.config["debug"]:
            print("Loaded fonts and bg (menu)")

        # Because I'm lazy im gonna load fonts like this
        self.texts: Dict[str, Tuple[Surface, Tuple[int, int]]] = {}

        Helpers.text_add_helper(
            self.texts,
            (int(self.config.config["width"]), int(self.config.config["height"])),
            (
                (
                    self.font2.render(
                        "Press ESC to quit, press SPACE to continue",
                        True,
                        (255, 255, 255),
                    ),
                    "space",
                    (50, 50),
                ),
                (
                    self.font4.render(
                        "Surely this is some kind of game", True, (255, 255, 255)
                    ),
                    "flavour",
                    (50, 30),
                ),
            ),
        )

        if self.config.config["debug"]:
            print("Loaded text & positions (menu)")
            print("Initialising menu")
            print(self.__dict__)

    def loop(self) -> bool:
        if self.config.config["debug"]:
            print("Entering loop")
        gamestate = True
        _quit = False
        while gamestate:
            self.render()

            # NOTE: Is there a better implementation for flow control?
            for event in pg.event.get():
                if self.config.config["debug"]:
                    print(event)
                if event.type == pg.QUIT:
                    _quit = True
                    gamestate = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        _quit = True
                        gamestate = False
                    elif event.key == pg.K_SPACE:
                        gamestate = False

            self.clock.tick(int(self.config.config["fps"]))

        if _quit:
            return False
        return True

    def render(self) -> None:
        # TODO: Either edit the image & darken it or add an alpha darken layer

        self.screen.fill((0, 0, 0))
        self.screen.blits(
            (
                (self.bg, (0, 0)),
                (self.texts["flavour"][0], self.texts["flavour"][1]),
                (self.texts["space"][0], self.texts["space"][1]),
            )
        )
        display.flip()

        if self.config.config["debug"]:
            print("Rendering menu")

    @property
    def clock(self) -> time.Clock:
        return self._clock

    @property
    def fs_daemon(self) -> FS_Daemon:
        return self._fsd

    @property
    def config(self) -> Config:
        return self._conf

    @property
    def screen(self) -> Surface:
        return self._scr
