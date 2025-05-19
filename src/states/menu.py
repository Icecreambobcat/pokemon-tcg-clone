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
        # private
        self._clock = clock
        self._fsd = fsd
        self._conf = config
        self._scr = screen

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

        # Because I'm lazy im gonna load fonts like this
        self.texts: Dict[str, Tuple[Surface, Tuple[int, int]]] = {}

        # TODO: Potentially revise the texts implementation to getters & setters
        self.text_add_helper(
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
            )
        )

    def text_add_helper(
        self,
        sequences: Tuple[Tuple[Surface, str, Tuple[int, int]], ...],
    ) -> None:
        """
        Input a sequence of (<font_surface>, "name", (x, y)) tuples.
        x and y are offset the center of the text rect by screen size percent from (0, 0)
        """

        # NOTE: These are only called once and not updated dynamically
        for i in sequences:
            pos = (
                int(
                    i[2][0] / 100 * int(self.config.config["width"])
                    - i[0].get_width() / 2
                ),
                int(
                    i[2][1] / 100 * int(self.config.config["height"])
                    - i[0].get_height() / 2
                ),
            )
            self.texts[i[1]] = (i[0], pos)

    def loop(self) -> bool:
        gamestate = True
        _quit = False
        while gamestate:
            self.render()
            display.flip()

            # NOTE: Is there a better implementation for flow control?
            for event in pg.event.get():
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
