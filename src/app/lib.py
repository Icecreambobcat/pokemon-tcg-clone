from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
import pygame as pg
from pygame import Font, Surface, image, sprite, time
from pathlib import Path
import re

from app.conf import Config


class GameState(ABC):
    @abstractmethod
    def loop(self) -> bool:
        """
        Contains a "while" loop to enter the gamestate
        This returns a binary value, indicating flow branches
        """
        pass

    @abstractmethod
    def render(self) -> None:
        """
        This method is implemented for the sake of posterity; animations are much easier this way
        """
        pass

    @property
    @abstractmethod
    def clock(self) -> time.Clock:
        """
        The game clock should be passed into each gamestate
        """
        pass

    @property
    @abstractmethod
    def fs_daemon(self) -> FS_Daemon:
        """
        The filesystem daemon should be passed into each gamestate
        """
        pass

    @property
    @abstractmethod
    def config(self) -> Config:
        """
        The config should be passed into each gamestate
        """
        pass

    @property
    @abstractmethod
    def screen(self) -> Surface:
        """
        The screen should be passed into each gamestate
        """
        pass


class Object(ABC, sprite.Sprite):
    """
    But... why would you do this when it's a turn based game???
    """

    @property
    @abstractmethod
    def position(self) -> Tuple[int, int]:
        pass

    @property
    @abstractmethod
    def tex(self) -> Surface:
        pass


class Entity(ABC):
    """
    Encapsulates both potential enemies and players
    """

    class Card(ABC):
        """
        Different cards (abilities) are subclassed from here
        Behaviour of different types should be defined purely within subclasses
        """

        @property
        @abstractmethod
        def name(self) -> str:
            pass

        @property
        @abstractmethod
        def description(self) -> str:
            pass

        @property
        @abstractmethod
        def type(self) -> str:
            pass

    @property
    @abstractmethod
    def health(self) -> int:
        pass

    @property
    @abstractmethod
    def cards(self) -> Dict[str, Card]:
        pass


class FS_Daemon:
    """
    Handler for asset access
    """

    root: Path

    def __init__(self) -> None:
        self.root = Path("../..")

    @property
    def fonts(self) -> Dict[str, List[Font]]:
        """
        Regex for all ttf files and load them in a range of sizes
        """
        out = {}
        files = Path(self.root, "assets", "fonts").iterdir()
        for file in files:
            name = re.search(r"(.+)\.ttf$", file.name)
            if name:
                out[name.group(1)] = list(
                    map(lambda x: Font(file, 24 * x), range(1, 5))
                )

        return out

    @property
    def images(self) -> Dict[str, Surface]:
        """
        Similarly regex for all image files with valid extensions
        May add support for implicitly hinting size by regexing the name
        """
        out = {}
        files = Path(self.root, "assets", "images").iterdir()
        for file in files:
            name = re.search(r"(.+)\.(jpg|png|jpeg)$", file.name)
            if name:
                out[name.group(1)] = image.load(file)

        return out
