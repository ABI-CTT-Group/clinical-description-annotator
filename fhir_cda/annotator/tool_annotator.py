from abc import ABC
from .abstract_annotator import AbstractAnnotator
from pathlib import Path
import json


class ToolAnnotator(AbstractAnnotator, ABC):
    def __init__(self, dataset_path):
        super().__init__(dataset_path, "workflow_tool")
        self._descriptions = {}
        self._metadata_path = Path(dataset_path, "workflow_tool.json")
        self._get_description()

    def _get_description(self):
        metadata_path = self._metadata_path
        if not metadata_path.exists():
            self._descriptions = {
                "workflow_tool": {
                    "uuid": "",
                    "name": "",
                    "title": "",
                    "version": "",
                    "description": "",
                    "model": [],
                    "software": [],
                    "input": [],
                    "output": []
                }
            }
        else:
            with open(metadata_path, "r") as f:
                self._descriptions = json.load(f)

    def update_workflow_tool_description(self, field, value):
        if field not in self._descriptions.get("workflow_tool"):
            raise ValueError(f"field {field} is not in descriptions['workflow_tool']")
        else:
            self._descriptions["workflow_tool"][field] = value
        return self

    def update_workflow_tool_model(self, value):
        if type(value) is list:
            self._descriptions["workflow_tool"]["model"].extend(value)
        elif type(value) is str:
            self._descriptions["workflow_tool"]["model"].append(value)
        else:
            raise ValueError(
                f"Value {value} is invalid. Expected a string or a list of strings (UUIDs), but got {type}.")
        return self

    def update_workflow_tool_software(self, value):
        if type(value) is list:
            self._descriptions["workflow_tool"]["software"].extend(value)
        elif type(value) is str:
            self._descriptions["workflow_tool"]["software"].append(value)
        else:
            raise ValueError(
                f"Value {value} is invalid. Expected a string or a list of strings (UUIDs), but got {type}.")
        return self

    def save(self, path=None):
        super().save(path)
