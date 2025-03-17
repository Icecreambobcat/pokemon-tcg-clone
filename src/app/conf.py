from typing import Dict


class Config:
    defaults: Dict[str, str] = {}

    def __init__(self) -> None:
        # merge argparse results w defaults
        pass
