from __future__ import annotations, with_statement
import pygame as pg
from pygame import Surface, time

from app.conf import Config
from app.lib import FS_Daemon, GameState


class Game(GameState):
    # TODO: Implement the whole thing!!!!!
    def __init__(
        self, clock: time.Clock, fsd: FS_Daemon, config: Config, screen: Surface
    ) -> None:
        self._clock = clock
        self._fsd = fsd
        self._conf = config
        self._scr = screen

    def loop(self) -> bool:
        gamestate = True
        while gamestate:
            self.render()
            self.clock.tick(int(self.config.config["fps"]))
        return False

    def render(self) -> None:
        pass

    def process_behaviour(self):
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
