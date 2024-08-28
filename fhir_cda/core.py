from pathlib import Path
from .annotator import MeasurementAnnotator


class Annotator:
    measurement_annotator = MeasurementAnnotator

    def __init__(self, dataset_path):
        self.root = Path(dataset_path)

    def measurements(self):
        return self.measurement_annotator(self.root)
