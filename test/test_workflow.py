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
        annotator = Annotator("./dataset/workflow").workflow()
        # annotator = Annotator(r"C:\Users\lgao142\Desktop\Development\DigitalTWIN tools\digitalTwin-fhir-adapter\test\dataset\ep4\measurements").measurements()

        (annotator.update_uuid("sparc-workflow-breast-tumour_position_1123")
         .update_author("Ayah")
         .update_name("Breast tumour position workflow")
         .update_purpose(
            "This workflow standardizes identifying and recording breast tumour positions, and supporting diagnosis for improved clinical decision-making.")
         .update_usage("Enables research by analyzing tumour positions."))
        actions = annotator.annotate_action()
        action_1 = actions[0].set_related_tool_uuid("tool-001")
        pprint(action_1.get())
        action_1_input_1 = action_1.annotate_input()[0]
        action_1_input_1.set_resource_type("ImagingStudy")
        action_1_output_1 = action_1.annotate_output()[0]
        action_1_output_1.set_resource_type("ImagingStudy")

        action_2 = actions[1].set_related_tool_uuid("tool-002")
        pprint(action_2.get())
        action_2_inputs = action_2.annotate_input()
        action_2_inputs[0].set_resource_type("ImagingStudy")
        action_2_inputs[1].set_resource_type("DocumentReference")
        action_2_inputs[2].set_resource_type("DocumentReference")
        action_2_outputs = action_2.annotate_output()
        action_2_outputs[0].set_resource_type("DocumentReference")

        action_3 = actions[2].set_related_tool_uuid("tool-003")
        pprint(action_3.get())
        action_3_inputs = action_3.annotate_input()
        action_3_inputs[0].set_resource_type("DocumentReference")
        action_3_outputs = action_3.annotate_output()
        action_3_outputs[0].set_resource_type("DocumentReference")

        action_4 = actions[3].set_related_tool_uuid("tool-004")
        pprint(action_4.get())
        action_4_inputs = action_4.annotate_input()
        action_4_inputs[0].set_resource_type("DocumentReference")
        action_4_inputs[1].set_resource_type("DocumentReference")
        action_4_outputs = action_4.annotate_output()
        action_4_outputs[0].set_resource_type("DocumentReference")

        action_5 = actions[4].set_related_tool_uuid("tool-005")
        pprint(action_5.get())
        action_5_inputs = action_5.annotate_input()
        action_5_inputs[0].set_resource_type("ImagingStudy")
        action_5_inputs[1].set_resource_type("DocumentReference")
        action_5_inputs[2].set_resource_type("DocumentReference")
        action_5_outputs = action_5.annotate_output()
        action_5_outputs[0].set_resource_type("Observation").set_system("https://loinc.org/").set_code(
            "85904-1").set_unit("mm")

        action_6 = actions[5]
        pprint(action_6.get())
        action_6_inputs = action_6.annotate_input()
        action_6_inputs[0].set_resource_type("Observation")
        action_6_outputs = action_6.annotate_output()
        action_6_outputs[0].set_resource_type("DiagnosticReport")

        # EP1
        annotator.save()

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Function took {elapsed_time:.4f} seconds to complete.")

        print(annotator.get_descriptions())


if __name__ == '__main__':
    test = Test()
    test.test_workflow_annotator()
    # test.test_measurements_annotator_update_mode()
    # test.test_workflow_annotator()
