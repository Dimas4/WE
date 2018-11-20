import pathlib
import os

import yaml


def get_config():
    path = pathlib.Path(__file__).parent
    with open(os.path.join(path, "config.yaml"), "r") as file:
        config = yaml.load(file)
    return config
