from pathlib import Path
from .annotator import MeasurementAnnotator, WorkflowAnnotator


class Annotator:
    measurement_annotator = MeasurementAnnotator
    workflow_annotator = WorkflowAnnotator

    def __init__(self, dataset_path):
        self.root = Path(dataset_path)

    def measurements(self):
        return self.measurement_annotator(self.root)

    def workflow(self):
        return self.workflow_annotator(self.root)
