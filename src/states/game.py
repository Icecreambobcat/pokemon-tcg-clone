from __future__ import annotations, with_statement
from typing import Dict, Tuple
import pygame as pg
from pygame import Surface, display, sprite, time, transform

from app.conf import Config
from app.lib import Entity, FS_Daemon, GameState


class Game(GameState):
    # TODO: Implement the whole thing!!!!!
    def __init__(
        self, clock: time.Clock, fsd: FS_Daemon, config: Config, screen: Surface
    ) -> None:
        from app.lib import Helpers

        # private
        self._clock = clock
        self._fsd = fsd
        self._conf = config
        self._scr = screen

        # sect: images
        # TODO: find other assets for "game" gamestate
        self.bg = transform.scale(
            self.fs_daemon.images["gamebg"],
            (int(self.config.config["width"]), int(self.config.config["height"])),
        )

        # sect: fonts
        self.font4 = self.fs_daemon.fonts["JetBrainsMonoNerdFont-regular"][3]
        self.font3 = self.fs_daemon.fonts["JetBrainsMonoNerdFont-regular"][2]
        self.font2 = self.fs_daemon.fonts["JetBrainsMonoNerdFont-regular"][1]
        self.font1 = self.fs_daemon.fonts["JetBrainsMonoNerdFont-regular"][0]

        # Because I'm lazy im gonna load fonts like this
        self.texts: Dict[str, Tuple[Surface, Tuple[int, int]]] = {}

        # TODO: Add required text and positions
        # Text positions should all be predetermined, and rendered only when needed
        Helpers.text_add_helper(
            self.texts,
            (int(self.config.config["width"]), int(self.config.config["height"])),
            (),
        )

        # sect: sprites & group handling
        self.playerssprites = sprite.Group()
        self.enemiessprites = sprite.Group()
        self.overlaysprites = sprite.Group()

        # TODO: add some for [match name] in fsd[type]... loop to load everything in 1 go


        # sect: init player

    def loop(self) -> bool:
        self.initialise_gamestate()
        gamestate = True
        while gamestate:
            self.render()
            self.clock.tick(int(self.config.config["fps"]))
        return False

    def render(self) -> None:
        self.screen.fill((0, 0, 0))
        # TODO: Implement logic control here by checking self.status (dict)
        display.flip()

    def process_behaviour(self) -> None:
        pass

    def initialise_gamestate(self) -> None:
        # TODO: Reset player health & groups
        pass

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

    # TODO: Implement behaviours for these 2 classes
    class Player(Entity):
        pass

    class Enemy(Entity):
        pass
