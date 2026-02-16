from pathlib import Path

import yaml


def load_yml(filename:str) -> dict:
    path = Path(__file__).parent.parent / "schemas" / filename
    with path.open() as file:
        return yaml.safe_load(file)
