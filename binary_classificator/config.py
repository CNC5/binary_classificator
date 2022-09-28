import configparser
from dataclasses import dataclass
from functools import lru_cache


@dataclass
class Config:
    host: str
    loglevel: int

def load_config(path: str):
    cfg = configparser.ConfigParser()
    cfg.read(path)
    general = cfg["general"]
    return Config(host=general.get("host"),
        loglevel=general.getint("loglevel"),
        )
