from __future__ import annotations
from typing import Dict


class Config:
    defaults: Dict[str, str | int | bool] = {
        "width": 1200,
        "height": 800,
        "fps": 120,
        "debug": False,
        "vsync": False,
        "title": "Pokemon TCG Clone",
    }

    config: Dict[str, str | int | bool]

    def __init__(self, custom: Dict[str, str | int | bool] = {}) -> None:
        """
        Initialising the config by passing a config dict (optional) merges it with the defaults
        This overrides any default values
        Nonstandard keys are ignored and removed
        """

        # NOTE: This is a standard table merge
        _tmp = {**Config.defaults, **custom}
        for key in _tmp.keys():
            if key not in set(Config.defaults.keys()):
                _ = _tmp.pop(key)

        self.config = _tmp
