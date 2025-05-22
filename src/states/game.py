from __future__ import annotations, with_statement
from typing import Dict, List, Tuple
import pygame as pg
from pygame import Surface, display, sprite, time, transform

from app.conf import Config
from app.lib import Entity, FS_Daemon, GameState, Object


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

        # TODO: add some for [match name] in fsd[type]... loop to load everything in 1 go

        # sect: init player
        # TODO: implement missing methods
        # Implement textures
        # implement naming

        # self.player = self.Player()
        # self.enemy = self.Enemy()

    def loop(self) -> bool:
        self.initialise_gamestate()
        gamestate = True
        while gamestate:
            self.render()
            self.process_behaviour()
            self.clock.tick(int(self.config.config["fps"]))
        return False

    def render(self) -> None:
        # NOTE: This much should all be obvious. The overlay needs more work
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        # TODO: Implement logic control here by checking self.status (dict)
        display.flip()

    def process_behaviour(self) -> None:
        # TODO: Handle player input here + call class logic
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

    # TODO: Implement behaviours for these 3 classes
    # add logic
    # NOTE: Here, renderered sprites are nested into the overall class handling behaviour
    class Player(Entity.Player):
        _hp: int
        _sp: PlayerSprite
        _cards: List[Entity.Player.Card]

        class PlayerSprite(Object):
            _pos: Tuple[int, int]
            _tex: Surface

            def __init__(self, tex) -> None:
                self._pos = (0, 0)
                self._tex = tex

            @property
            def position(self) -> Tuple[int, int]:
                return self._pos

            @position.setter
            def position(self, pos: Tuple[int, int]) -> None:
                self._pos = pos

            @property
            def tex(self) -> Surface:
                return self._tex

        class Card(Entity.Player.Card):
            # TODO: implement the card framework and a few basic cards
            pass

        def __init__(self, tex: Surface) -> None:
            self._sp = self.PlayerSprite(tex)
            self._hp = 500
            self.maxhp = self._hp
            # Lets just arbitrarily put 500... will see how this goes
            # Set the max hp to whatever the character is initialised with
            # I'm too lazy to do otherwise

        @property
        def health(self) -> int:
            return self._hp

        # NOTE: Using these setter methods is a catch-all way to be lazy when expanding
        @health.setter
        def health(self, hp: int) -> None:
            match hp:
                case num if num < 0:
                    self.hp = 0
                case num if num > self.maxhp:
                    self.hp = self.maxhp
                case _:
                    self._hp = hp

        @property
        def sprite(self) -> PlayerSprite:
            return self._sp

        @property
        def cards(self) -> List[Entity.Player.Card]:
            return self._cards

        # TODO: Implement behaviour here
        def playerturn(self) -> None:
            pass

    class Enemy(Entity.Enemy):
        _hp: int
        _sp: EnemySprite
        _attacks: List[Entity.Enemy.Attack]

        class EnemySprite(Object):
            _pos: Tuple[int, int]
            _tex: Surface

            def __init__(self, tex) -> None:
                self._pos = (0, 0)
                self._tex = tex

            @property
            def position(self) -> Tuple[int, int]:
                return self._pos

            @position.setter
            def position(self, pos: Tuple[int, int]) -> None:
                self._pos = pos

            @property
            def tex(self) -> Surface:
                return self._tex

        class EnemyAttack(Entity.Enemy.Attack):
            # TODO: add a few basic attacks for enemies too
            pass

        def __init__(self, tex: Surface, hp: int, name: str) -> None:
            self._sp = self.EnemySprite(tex)
            self._hp = hp
            self._name = name
            # self._attacks = []
            self.maxhp = self._hp
            # let's just do this again

        @property
        def name(self) -> str:
            return self._name

        @property
        def health(self) -> int:
            return self._hp

        @health.setter
        def health(self, hp: int) -> None:
            match hp:
                case num if num < 0:
                    self.hp = 0
                case num if num > self.maxhp:
                    self.hp = self.maxhp
                case _:
                    self._hp = hp

        @property
        def sprite(self) -> EnemySprite:
            return self._sp

        @property
        def attacks(self) -> List[Entity.Enemy.Attack]:
            return self._attacks

        # TODO: implement enermyturn handling
        def enemyturn(self) -> None:
            pass

    class Overlay(Object):
        _pos: Tuple[int, int]
        _size: Tuple[int, int]
        _tex: Surface

        def __init__(
            self, position: Tuple[int, int], size: Tuple[int, int], tex: Surface
        ) -> None:
            self._pos = position
            self._size = size
            self._tex = tex

        @property
        def position(self) -> Tuple[int, int]:
            return self._pos

        @position.setter
        def position(self, pos: Tuple[int, int]) -> None:
            self._pos = pos

        @property
        def tex(self) -> Surface:
            return self._tex

        @property
        def size(self) -> Tuple[int, int]:
            return self._size

        @size.setter
        def size(self, size: Tuple[int, int]) -> None:
            self._size = size

