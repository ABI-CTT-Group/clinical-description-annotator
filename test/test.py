from fhir_cda import Annotator
from fhir_cda.utils import check_first_file_extension
from fhir_cda.ehr import ObservationMeasurement, ObservationValue, Quantity, DocumentReferenceMeasurement, ImagingStudyMeasurement
from pathlib import Path
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


        # add ImagingStudy Measurement automatically by scan dataset
        annotator.automated_generating_imaging_study_measurement_by_scan_dataset()

        # add ImagingStudy Measurements manually
        # p1 = Path("./dataset/dataset-sparc/primary/sub-001")
        # p1_sams = [x for x in p1.iterdir() if x.is_dir()]
        # p1_dcm_sams = [sam for sam in p1_sams if check_first_file_extension(sam) == "dcm"]
        # m4 = ImagingStudyMeasurement(uuid="",
        #                              sample_paths=p1_dcm_sams,
        #                              endpoint_url="",
        #                              description="dcm")
        # annotator.add_measurements(["sub-001"], [m4])


        annotator.save()

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Function took {elapsed_time:.4f} seconds to complete.")

    def test_measurements_annotator_update_mode(self):
        annotator = Annotator("./dataset/dataset-sparc").measurements(mode="update")
        annotator.update_imaging_study_measurement_series_description("sub-004", 1, {
            "sam-007": "pre contrast",
            "sam-008": "contrast 1"
        })
        annotator.update_dataset("uuid", "aaxaaa")
        annotator.save()
        # pprint(annotator.descriptions)
        pprint(annotator.elements)

    def test_workflow_annotator(self):
        annotator = Annotator("./dataset/workflow").workflow()
        pprint(annotator.descriptions)


if __name__ == '__main__':
    test = Test()
    test.test_measurements_annotator()
    test.test_measurements_annotator_update_mode()
    # test.test_workflow_annotator()
