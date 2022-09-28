import configparser
from dataclasses import dataclass
from functools import lru_cache


@dataclass
class Config:
    global_loglevel: int
    host: str
    save_folder: str
    checkpoint_path: str
    full_save_path: str
    tensorflow_loglevel: int
    training_shuffle_buffer_size: int
    training_batch_size: int
    training_prefetch_size: int
    model_vocab_size: int
    layers_setup: str


def load_config(path: str):
    cfg = configparser.ConfigParser()
    cfg.read(path)
    general = cfg["general"]
    return Config(
        global_loglevel = general.get("global_loglevel"),
        host = general.get("host"),
        save_folder = general.get("save_folder"),
        checkpoint_path = general.get("checkpoint_path"),
        full_save_path = general.get("full_save_path"),
        tensorflow_loglevel = general.getint("tensorflow_loglevel"),
        training_shuffle_buffer_size = general.getint("training_shuffle_buffer_size"),
        training_batch_size = general.getint("training_batch_size"),
        training_prefetch_size = general.getint("training_prefetch_size"),
        model_vocab_size = general.getint("model_vocab_size"),
        layers_setup = general.get("layers_setup"))
