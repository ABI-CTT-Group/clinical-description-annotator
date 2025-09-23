from fhir_cda import Annotator
from fhir_cda.ehr.elements import ImagingStudySeries
from fhir_cda.utils import check_first_file_extension
from fhir_cda.ehr import ObservationMeasurement, ObservationValue, Quantity, DocumentReferenceMeasurement, \
    ImagingStudyMeasurement
from pathlib import Path
from typing import Union
from pprint import pprint
import time


class Test:

    def test_workflow_annotator(self):
        start_time = time.time()
        annotator = Annotator("./dataset/tools/dataset-workflow-tool-1").workflow_tool()

        annotator.update_uuid("tool-1").update_title("create_nifti").update_version("1.0.0")
        # EP1
        annotator.save()

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Function took {elapsed_time:.4f} seconds to complete.")


if __name__ == '__main__':
    test = Test()
    test.test_workflow_annotator()
    # test.test_measurements_annotator_update_mode()
    # test.test_workflow_annotator()
