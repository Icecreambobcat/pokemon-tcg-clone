from abc import ABC, abstractmethod
from typing import Dict, Tuple
from pygame import Surface, sprite


class GameState(ABC):
    @abstractmethod
    def loop(self) -> bool:
        pass

    @abstractmethod
    def render(self) -> None:
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

    class Cards(ABC):
        """
        Varied properties depending on card type
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
    def cards(self) -> Dict[str, Cards]:
        pass
