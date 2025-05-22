from __future__ import annotations, with_statement
from typing import Dict, List, Tuple
import asyncio
from random import choice, randint, uniform, choices
import pygame as pg
from pygame import Surface, display, draw, sprite, time, transform

from app.app import App
from app.conf import Config
from app.lib import Entity, FS_Daemon, GameState, SpriteObject


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
        # NOTE: these two are separated to differentiate quitting the app and quitting to the menu
        self._quit: bool = False
        self._restart: bool = False

        if self.config.config["debug"]:
            print("Loaded private game vars")
            print(time.get_ticks())

        # sect: images
        self.bg = transform.scale(
            self.fs_daemon.images["gamebg"],
            (int(self.config.config["width"]), int(self.config.config["height"])),
        )

        self.alpha = Surface(
            (int(self.config.config["width"]), int(self.config.config["height"]))
        )
        self.alpha.fill((0, 0, 0))
        self.alpha.set_alpha(120)

        # sect: fonts
        self.font4 = self.fs_daemon.fonts["JetBrainsMonoNerdFont-regular"][3]
        self.font3 = self.fs_daemon.fonts["JetBrainsMonoNerdFont-regular"][2]
        self.font2 = self.fs_daemon.fonts["JetBrainsMonoNerdFont-regular"][1]
        self.font1 = self.fs_daemon.fonts["JetBrainsMonoNerdFont-regular"][0]

        if self.config.config["debug"]:
            print("Loaded fonts and bg (game)")
            print(time.get_ticks())

        self.texts: Dict[str, Tuple[Surface, Tuple[int, int]]] = {}

        # sect: init player & enemy

        self.player = self.Player(
            transform.scale(self.fs_daemon.images["playertex"], (300, 300))
        )

        self.player.cards = [
            self.Player.Card(
                "Social anxiety crashout!!!!!",
                "Deal 400 damage to the enemy and 50 damage to yourself, and heal for 100 hp. Can critically strike for double damage and massive healing.",
                "finisher",
                15,
                400,
                0.5,
                50,
                True,
            ),
            self.player.Card(
                "Sorry for existing!!!",
                "Deal 200 damage and heal for 50 hp. Can critically strike for 50% increased effectiveness.",
                "amplify",
                10,
                200,
                0.3,
                50,
                False,
            ),
            self.player.Card(
                "Stage fright",
                "Deals 120 damage. The next card you play capable of critically striking is guaranteed to do so. This effect does not stack. Cannot critically strike.",
                "guaranteecrit",
                8,
                120,
                0,
                0,
                True,
            ),
            self.player.Card(
                "Don't talk to me!",
                "Restores 150 hp. Can critically strike for an additional 300 hp healing.",
                "restore",
                6,
                0,
                0.2,
                150,
                False,
            ),
            self.player.Card(
                "Cardboard guitar",
                "Deals 120 damage. Can critically strike for double damage.",
                "damage",
                4,
                120,
                0.3,
                0,
                False,
            ),
            self.player.Card(
                "G string",
                "Draw another card instantly.",
                "drawcard",
                1,
                0,
                0,
                0,
                True,
            ),
        ]

        self.player.currentdeck = []

        self.enemy = self.Enemy(
            transform.scale(self.fs_daemon.images["enemytex"], (150, 150)),
            1000,
            "Devious Pikachu",
        )
        # for now...
        self.player.sprite.position = (
            int(
                int(self.config.config["width"]) * 0.275
                - self.player.sprite.tex.get_width() / 2
            ),
            int(
                int(self.config.config["height"]) * 0.7
                - self.player.sprite.tex.get_height() / 2
            ),
        )
        self.enemy.sprite.position = (
            int(
                int(self.config.config["width"]) * 0.7
                - self.enemy.sprite.tex.get_width() / 2
            ),
            int(
                int(self.config.config["height"]) * 0.265
                - self.enemy.sprite.tex.get_height() / 2
            ),
        )

        self.enemy.attacks = [
            self.enemy.EnemyAttack(
                "Pika punch",
                6,
                80,
            ),
            self.enemy.EnemyAttack(
                "Pika strike",
                10,
                100,
            ),
            self.enemy.EnemyAttack(
                "Sued by Nintendo",
                20,
                400,
            ),
            self.enemy.EnemyAttack(
                "Pika slash",
                12,
                150,
            ),
        ]

        Helpers.text_add_helper(
            self.texts,
            (int(self.config.config["width"]), int(self.config.config["height"])),
            (
                (
                    self.font3.render(f"{self.enemy.name}", True, (255, 255, 255)),
                    "enemyname",
                    (70, 13),
                ),
                (
                    self.font3.render("GUITAR GIRL (BOCCHI)", True, (255, 255, 255)),
                    "playername",
                    (31, 42),
                ),
                (
                    self.font2.render("Available cards:", True, (0, 0, 0)),
                    "playerturnlist",
                    (75, 58),
                ),
                (
                    self.font2.render("Available mana", True, (255, 255, 255)),
                    "mananame",
                    (15, 85),
                ),
                (
                    self.font2.render("Enemy mana", True, (255, 255, 255)),
                    "enemymananame",
                    (70, 40),
                ),
                (
                    self.font4.render(
                        "Press 'R' to restart\nPress ESC to quit", True, (255, 255, 255)
                    ),
                    "gameover",
                    (50, 50),
                ),
            ),
        )

        if self.config.config["debug"]:
            print("Loaded text & positions (game)")
            print(time.get_ticks())

        # sect: other control functions
        self.status: str
        self.elements: Dict[str, SpriteObject] = {}

        self.switchevent = pg.event.custom_type()
        self.enemyattackevent = pg.event.custom_type()

        if self.config.config["debug"]:
            print("Initialising game object")
            print(time.get_ticks())
            print(self.__dict__)

    def loop(self) -> bool:
        self.initialise_gamestate()

        if self.config.config["debug"]:
            print("Entering loop")
            print(time.get_ticks())
            print(self.__dict__)

        gamestate = True
        while gamestate:
            self.render()
            self.process_behaviour()
            self.clock.tick(int(self.config.config["fps"]))
            if self._quit:
                break
            elif self._restart:
                break
        else:
            return True
        if self._quit:
            App.quit("Quit from game loop")
        return False

    def render(self) -> None:
        # NOTE: This much should all be obvious. The overlay needs more work
        self.screen.fill((0, 0, 0))

        def commons() -> None:
            self.screen.blits(
                (
                    (self.bg, (0, 0)),
                    (self.alpha, (0, 0)),
                    (self.player.sprite.tex, self.player.sprite.position),
                    (self.enemy.sprite.tex, self.enemy.sprite.position),
                )
            )

            draw.rect(
                self.screen,
                (0, 0, 0),
                (
                    int(self.config.config["width"]) * 0.6,
                    int(self.config.config["height"]) * 0.05,
                    int(self.config.config["width"]) * 0.2,
                    int(self.config.config["height"]) * 0.05,
                ),
                border_radius=5,
            )
            draw.rect(
                self.screen,
                (255, 0, 0),
                (
                    int(self.config.config["width"]) * 0.62,
                    int(self.config.config["height"]) * 0.06,
                    int(self.config.config["width"]) * 0.16,
                    int(self.config.config["height"]) * 0.03,
                ),
                border_radius=4,
            )
            draw.rect(
                self.screen,
                (255, 255, 255),
                (
                    int(self.config.config["width"]) * 0.62,
                    int(self.config.config["height"]) * 0.06,
                    int(self.config.config["width"]) * 0.16 * self.enemy.health / 1000,
                    int(self.config.config["height"]) * 0.03,
                ),
                border_radius=4,
            )

            draw.rect(
                self.screen,
                (0, 0, 0),
                (
                    int(self.config.config["width"]) * 0.19,
                    int(self.config.config["height"]) * 0.33,
                    int(self.config.config["width"]) * 0.22,
                    int(self.config.config["height"]) * 0.05,
                ),
                border_radius=5,
            )
            draw.rect(
                self.screen,
                (255, 0, 0),
                (
                    int(self.config.config["width"]) * 0.2,
                    int(self.config.config["height"]) * 0.34,
                    int(self.config.config["width"]) * 0.2,
                    int(self.config.config["height"]) * 0.03,
                ),
                border_radius=4,
            )
            draw.rect(
                self.screen,
                (255, 255, 255),
                (
                    int(self.config.config["width"]) * 0.2,
                    int(self.config.config["height"]) * 0.34,
                    int(self.config.config["width"]) * 0.2 * self.player.health / 1000,
                    int(self.config.config["height"]) * 0.03,
                ),
                border_radius=4,
            )

            for i in range(self.player.mana):
                draw.rect(
                    self.screen,
                    (45, 0, 255),
                    (
                        int(self.config.config["width"]) * 0.1
                        + i * int(self.config.config["width"]) * 0.02,
                        int(self.config.config["height"]) * 0.9,
                        int(self.config.config["width"]) * 0.015,
                        int(self.config.config["height"]) * 0.05,
                    ),
                    border_radius=4,
                )

            for i in range(self.enemy.mana):
                draw.rect(
                    self.screen,
                    (255, 0, 45),
                    (
                        int(self.config.config["width"]) * 0.55
                        + i * int(self.config.config["width"]) * 0.02,
                        int(self.config.config["height"]) * 0.45,
                        int(self.config.config["width"]) * 0.015,
                        int(self.config.config["height"]) * 0.05,
                    ),
                    border_radius=4,
                )

            for text, surf in self.texts.items():
                if "name" in text:
                    self.screen.blit(surf[0], surf[1])

        def show_card_popup():
            unique_cards = {
                card.name: card for card in self.player.currentdeck
            }.values()
            popup_width = int(self.config.config["width"]) * 0.3
            popup_height = len(unique_cards) * 50 + 20
            popup_x = (int(self.config.config["width"]) - popup_width) // 2 - int(
                self.config.config["width"]
            ) * 0.3
            popup_y = (
                (int(self.config.config["height"]) - popup_height) // 2
                - int(self.config.config["height"]) * 0.32
                - popup_height * 0.2
            )

            draw.rect(
                self.screen,
                (50, 50, 50),
                (popup_x, popup_y, popup_width, popup_height),
                border_radius=10,
            )
            y_offset = popup_y + 10
            for card in unique_cards:
                description_surface = self.font1.render(
                    f"{card.name}\n{card.description}",
                    True,
                    (255, 255, 255),
                    wraplength=int(int(self.config.config["width"]) * 0.29),
                )
                self.screen.blit(description_surface, (popup_x + 10, y_offset))
                y_offset += 50
            for element in self.elements:
                self.screen.blit(
                    self.elements[element].tex, self.elements[element].position
                )

        match self.status:
            case "playerturn":
                commons()
                draw.rect(
                    self.screen,
                    (240, 240, 160),
                    (
                        int(self.config.config["width"]) * 0.55,
                        int(self.config.config["height"]) * 0.55,
                        int(self.config.config["width"]) * 0.4,
                        int(self.config.config["height"]) * 0.4,
                    ),
                    border_radius=5,
                )
                for text, surf in self.texts.items():
                    if "playerturn" in text:
                        self.screen.blit(surf[0], surf[1])

                i = 0
                table = {
                    0: "h",
                    1: "j",
                    2: "k",
                    3: "l",
                }
                for card in self.player.currentdeck:
                    self.screen.blit(
                        self.font2.render(
                            f"({table[i]}) {card.name} ({card.cost} cost)",
                            True,
                            (0, 0, 0),
                            wraplength=int(int(self.config.config["width"]) * 0.3),
                        ),
                        (
                            int(self.config.config["width"]) * 0.58,
                            int(self.config.config["height"]) * 0.6 + i * 50,
                        ),
                    )
                    i += 1

                show_card_popup()

            case "enemyturn":
                commons()
                # animate
                for event in pg.event.get(self.enemyattackevent):
                    text = self.font2.render(
                        f"{self.enemy.name} attacks with {event.dict["attack"]}",
                        True,
                        (200, 150, 200),
                        wraplength=int(int(self.config.config["width"]) * 0.5),
                    )

                    self.screen.blit(
                        text,
                        (
                            int(self.config.config["width"]) * 0.55
                            - text.get_width() // 2,
                            int(self.config.config["height"]) * 0.6
                            - text.get_height() // 2,
                        ),
                    )

            case "gameover":
                self.screen.fill((0, 0, 0))
                for text, surf in self.texts.items():
                    if "gameover" in text:
                        self.screen.blit(surf[0], surf[1])
        display.flip()

        if self.config.config["debug"]:
            print("Rendering game")
            print(time.get_ticks())

    def process_behaviour(self) -> None:
        if self.player.health == 0:
            self.status = "gameover"
            pg.event.post(pg.event.Event(self.switchevent))

        if self.enemy.health == 0:
            self.status = "gameover"
            pg.event.post(pg.event.Event(self.switchevent))

        def handle_special(num: int) -> None:
            match num:
                case 1:
                    self.player.currentdeck.append(choice(self.player.cards))
                case 2:
                    self.player.gcrit = True
                case 3:
                    pass

        def enemy_turn() -> None:
            while True:
                attack = choice(self.enemy.attacks)
                if attack.cost > self.enemy.mana:
                    break
                self.enemy.mana = self.enemy.mana - attack.cost
                self.player.health = self.player.health - attack.damage
                pg.event.post(
                    pg.event.Event(
                        self.enemyattackevent,
                        attack=attack.name,
                        cost=attack.cost,
                        damage=attack.damage,
                    )
                )
                self.render()
                pg.time.wait(1000)
                if self.config.config["debug"]:
                    print(attack.name, attack.cost, attack.damage)
                    print(time.get_ticks())
            self.status = "playerturn"
            pg.event.post(pg.event.Event(self.switchevent))
            pg.time.wait(1000)

        for event in pg.event.get():
            if self.config.config["debug"]:
                print(event)
                print(time.get_ticks())

            if event.type == pg.QUIT:
                self._quit = True

            elif event.type == self.switchevent:
                match self.status:
                    case "playerturn":
                        self.player.mana = self.player.mana + randint(2, 5)
                        self.player.currentdeck = choices(self.player.cards, k=4)
                    case "enemyturn":
                        self.enemy.mana = self.enemy.mana + randint(2, 5)
                        enemy_turn()
                    case "gameover":
                        self.screen.fill((0, 0, 0))

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self._quit = True
                if self.status == "playerturn":
                    if event.key == pg.K_h:
                        if len(self.player.currentdeck) > 0:
                            play = self.player.currentdeck[0].use(
                                self.player.mana, self.player.gcrit
                            )
                            if play["success"]:
                                if self.player.gcrit:
                                    self.player.gcrit = False
                                self.enemy.health = (
                                    self.enemy.health - play["enemyhpmod"]
                                )
                                self.player.mana = (
                                    self.player.mana - play["selfmanamod"]
                                )
                                self.player.health = (
                                    self.player.health + play["selfhpmod"]
                                )
                                self.player.currentdeck.remove(
                                    self.player.currentdeck[0]
                                )
                                handle_special(play["specialeffect"])
                            else:
                                # flash the mana animation
                                # Annnnnnnd i didn't have time to build this
                                pass

                    elif event.key == pg.K_j:
                        if len(self.player.currentdeck) > 1:
                            play = self.player.currentdeck[1].use(
                                self.player.mana, self.player.gcrit
                            )
                            if play["success"]:
                                if self.player.gcrit:
                                    self.player.gcrit = False
                                self.enemy.health = (
                                    self.enemy.health - play["enemyhpmod"]
                                )
                                self.player.mana = (
                                    self.player.mana - play["selfmanamod"]
                                )
                                self.player.health = (
                                    self.player.health + play["selfhpmod"]
                                )
                                self.player.currentdeck.remove(
                                    self.player.currentdeck[1]
                                )
                                handle_special(play["specialeffect"])
                            else:
                                # flash the mana animation
                                pass

                    elif event.key == pg.K_k:
                        if len(self.player.currentdeck) > 2:
                            play = self.player.currentdeck[2].use(
                                self.player.mana, self.player.gcrit
                            )
                            if play["success"]:
                                if self.player.gcrit:
                                    self.player.gcrit = False
                                self.enemy.health = (
                                    self.enemy.health - play["enemyhpmod"]
                                )
                                self.player.mana = (
                                    self.player.mana - play["selfmanamod"]
                                )
                                self.player.health = (
                                    self.player.health + play["selfhpmod"]
                                )
                                self.player.currentdeck.remove(
                                    self.player.currentdeck[2]
                                )
                                handle_special(play["specialeffect"])
                            else:
                                # flash the mana animation
                                pass

                    elif event.key == pg.K_l:
                        if len(self.player.currentdeck) > 3:
                            play = self.player.currentdeck[3].use(
                                self.player.mana, self.player.gcrit
                            )
                            if play["success"]:
                                if self.player.gcrit:
                                    self.player.gcrit = False
                                self.enemy.health = (
                                    self.enemy.health - play["enemyhpmod"]
                                )
                                self.player.mana = (
                                    self.player.mana - play["selfmanamod"]
                                )
                                self.player.health = (
                                    self.player.health + play["selfhpmod"]
                                )
                                self.player.currentdeck.remove(
                                    self.player.currentdeck[3]
                                )
                                handle_special(play["specialeffect"])
                            else:
                                # flash the mana animation
                                pass

                    elif event.key == pg.K_SPACE:
                        self.status = "enemyturn"
                        pg.event.post(pg.event.Event(self.switchevent))

                elif self.status == "gameover":
                    if event.key == pg.K_r:
                        self._restart = True

    def initialise_gamestate(self) -> None:
        self._restart = False
        self.status = "playerturn"
        pg.event.post(pg.event.Event(self.switchevent))
        self.player.health = self.player.maxhp
        self.player.mana = self.player.maxmana
        self.enemy.health = self.enemy.maxhp
        self.enemy.mana = self.enemy.maxmana

        self.player.sprite.position = (
            int(
                int(self.config.config["width"]) * 0.275
                - self.player.sprite.tex.get_width() / 2
            ),
            int(
                int(self.config.config["height"]) * 0.7
                - self.player.sprite.tex.get_height() / 2
            ),
        )
        self.enemy.sprite.position = (
            int(
                int(self.config.config["width"]) * 0.7
                - self.enemy.sprite.tex.get_width() / 2
            ),
            int(
                int(self.config.config["height"]) * 0.265
                - self.enemy.sprite.tex.get_height() / 2
            ),
        )

        if self.config.config["debug"]:
            print("Initialising gamestate")
            print(time.get_ticks())
            print(self.__dict__)

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

    # NOTE: Here, renderered sprites are nested into the overall class handling behaviour
    # Logic can now be handled elsewhere as all abstractions are completed here
    class Player(Entity.Player):
        _hp: int
        _sp: PlayerSprite
        _cards: List[Entity.Player.Card]
        _mana: int

        gcrit: bool = False
        currentdeck: List[Entity.Player.Card]

        class PlayerSprite(SpriteObject):
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
            def __init__(
                self,
                name: str,
                desc: str,
                type: str,
                cost: int,
                damage: int,
                crate: float,
                heal: int,
                special: bool,
            ) -> None:
                self._name = name
                self._desc = desc
                self._type = type
                self._cost = cost
                self.damage = damage
                self.crate = crate
                self.heal = heal
                self.special = special

            @property
            def name(self) -> str:
                return self._name

            @property
            def description(self) -> str:
                return self._desc

            @property
            def type(self) -> str:
                return self._type

            @property
            def cost(self) -> int:
                return self._cost

            def use(self, mana: int, gcrit: bool) -> Dict[str, int | bool]:
                heal: int = 0
                damage: int = 0
                special: int = 0

                if self.cost > mana:
                    return {"success": False}

                if self.special:
                    match self.type:
                        case "drawcard":
                            special = 1

                        case "guaranteecrit":
                            heal = self.heal
                            special = 2

                        case "finisher":
                            special = 3
                            if uniform(0, 1) < self.crate or gcrit:
                                heal = self.heal * 5
                                damage = self.damage * 2
                            else:
                                heal = self.heal
                                damage = self.damage

                    return {
                        "success": True,
                        "specialeffect": special,
                        "selfmanamod": self.cost,
                        "selfhpmod": heal,
                        "enemyhpmod": damage,
                    }

                match self.type:
                    case "damage":
                        if uniform(0, 1) < self.crate or gcrit:
                            damage = self.damage * 2
                            heal = int(self.heal * 1.5)
                        else:
                            damage = self.damage
                            heal = self.heal

                    case "amplify":
                        if uniform(0, 1) < self.crate or gcrit:
                            damage = int(self.damage * 1.5)
                            heal = self.heal * 2
                        else:
                            damage = self.damage
                            heal = self.heal

                    case "restore":
                        if uniform(0, 1) < self.crate or gcrit:
                            heal = self.heal * 3
                        else:
                            heal = self.heal

                return {
                    "success": True,
                    "specialeffect": special,
                    "selfhpmod": heal,
                    "enemyhpmod": damage,
                    "selfmanamod": self.cost,
                }

        def __init__(self, tex: Surface) -> None:
            self._sp = self.PlayerSprite(tex)
            self._hp = 1000
            self.maxhp = self._hp
            self._mana = 20
            self.maxmana = self._mana
            # Lets just arbitrarily put 1000... will see how this goes
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

        @cards.setter
        def cards(self, cards: List[Entity.Player.Card]) -> None:
            self._cards = cards

        @property
        def mana(self) -> int:
            return self._mana

        @mana.setter
        def mana(self, mana: int) -> None:
            match mana:
                case num if num < 0:
                    self._mana = 0
                case num if num > self.maxmana:
                    self._mana = self.maxmana
                case _:
                    self._mana = mana

    class Enemy(Entity.Enemy):
        _hp: int
        _sp: EnemySprite
        _attacks: List[Entity.Enemy.Attack]
        _mana: int

        class EnemySprite(SpriteObject):
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
            def __init__(self, name: str, cost: int, dmg: int) -> None:
                self._name = name
                self._dmg = dmg
                self._cost = cost

            @property
            def name(self) -> str:
                return self._name

            @property
            def cost(self) -> int:
                return self._cost

            @property
            def damage(self) -> int:
                return self._dmg

        def __init__(self, tex: Surface, hp: int, name: str) -> None:
            self._sp = self.EnemySprite(tex)
            self._hp = hp
            self._name = name
            self._mana = 20
            self.maxmana = self._mana
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
        def mana(self) -> int:
            return self._mana

        @mana.setter
        def mana(self, mana: int) -> None:
            match mana:
                case num if num < 0:
                    self._mana = 0
                case num if num > self.maxmana:
                    self._mana = self.maxmana
                case _:
                    self._mana = mana

        @property
        def sprite(self) -> EnemySprite:
            return self._sp

        @property
        def attacks(self) -> List[Entity.Enemy.Attack]:
            return self._attacks

        @attacks.setter
        def attacks(self, attacks: List[Entity.Enemy.Attack]) -> None:
            self._attacks = attacks

    class Overlay(SpriteObject):
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
