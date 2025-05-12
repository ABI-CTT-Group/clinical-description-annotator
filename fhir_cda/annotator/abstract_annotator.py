from pathlib import Path
from abc import ABC
import json


class AbstractAnnotator(ABC):

    def __init__(self, dataset_path, category):
        self.root = Path(dataset_path)
        self.category = category
        self.descriptions = {}

    def save(self, path=None):
        if path:
            save_path = Path(path) / f"{self.category}.json"
        else:
            save_path = self.root / f"{self.category}.json"

        with open(save_path, "w") as json_file:
            json.dump(self.descriptions, json_file, indent=4)