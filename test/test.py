from fhir_cda import Annotator
from fhir_cda.ehr import ObservationMeasurement, ObservationValue, Quantity, DocumentReferenceMeasurement
from typing import Union
from pprint import pprint
import time


class Test:

    def test_measurements_annotator(self):
        start_time = time.time()
        annotator = Annotator("./dataset/dataset-sparc").measurements()
        # annotator = Annotator(r"C:\Users\lgao142\Desktop\Development\DigitalTWIN tools\digitalTwin-fhir-adapter\test\dataset\ep4\measurements").measurements()

        # EP4
        m = ObservationMeasurement(value=ObservationValue(value_quantity=Quantity(value=28, unit="year", code="a")),
                                   code="30525-0")
        annotator.add_measurements(["sub-001"], [m]).save()

        m1 = ObservationMeasurement(value=ObservationValue(value_quantity=Quantity(value=33, unit="year", code="a")),
                                    code="30525-0")
        annotator.add_measurements(["sub-002"], [m1]).save()

        annotator.add_measurements(["sub-001", "sub-002"], ObservationMeasurement(
            value=ObservationValue(value_quantity=Quantity(value=175, unit="cm", code="cm")), code="8302-2",
            display="Body height"))
        m2 = DocumentReferenceMeasurement(
            url="https://example.org/files/mesh-breast-surface-df0c4efd-69a6-428a-ba70-786caecfadfb.obj",
            content_type="model/obj",
            title="Breast Surface Mesh")
        annotator.add_measurements(["sub-001"], [m2])

        # EP1
        # annotator.add_measurements("sub-002", Measurement(value=ObservationValue(value_quantity=Quantity(value=65, unit="L/min", code="UCUM")), code="76565-1",
        #                                                   code_system="https://loinc.org",
        #                                                   display="Cardiac output by US.2D+Calculated"))
        #
        # annotator.add_measurements("sub-001", Measurement(value=ObservationValue(value_quantity=Quantity(value=72, unit="L/min", code="UCUM")), code="76565-1",
        #                                                   code_system="https://loinc.org",
        #                                                   display="Cardiac output by US.2D+Calculated"))

        annotator.save()

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Function took {elapsed_time:.4f} seconds to complete.")

    def test_measurements_annotator_update_mode(self):
        annotator = Annotator("./dataset/dataset-sparc").measurements(mode="update")
        print(annotator.descriptions)
        annotator.update_imaging_study_measurement_series_description("sub-004", 1, {
            "sam-007": "pre contrast",
            "sam-008": "contrast 1"
        })
        annotator.save()

    def test_workflow_annotator(self):
        annotator = Annotator("./dataset/workflow").workflow()
        pprint(annotator.descriptions)


if __name__ == '__main__':
    test = Test()
    # test.test_measurements_annotator()
    test.test_measurements_annotator_update_mode()
    # test.test_workflow_annotator()
