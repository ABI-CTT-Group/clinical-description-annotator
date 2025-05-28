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

        # Add measurements with uuid by user
        m2 = ObservationMeasurement(
            uuid="sparc-xxx-1111",
            value=ObservationValue(
                value_string="this the test value."),
            display="test value string with uuid"
        )
        annotator.add_measurements("sub-001", m2).save()

        annotator.add_measurements(["sub-001", "sub-002"], ObservationMeasurement(
            value=ObservationValue(value_quantity=Quantity(value=175, unit="cm", code="cm")), code="8302-2",
            display="Body height"))
        m3 = DocumentReferenceMeasurement(
            url="https://example.org/files/mesh-breast-surface-df0c4efd-69a6-428a-ba70-786caecfadfb.obj",
            content_type="model/obj",
            title="Breast Surface Mesh")
        annotator.add_measurements(["sub-001"], [m3])

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

        # add ImagingStudy Measurement manually
        dcm_samples = [{"uuid": "jjshgsh", "path": "./dataset/dataset-sparc/primary/sub-001/sam-001"}]
        mi = ImagingStudyMeasurement(uuid="sparc-imaging-study-11981",
                                     sample_details=dcm_samples,
                                     description="test dcm for manual imaging study",
                                     endpoint_url="https://example.org/files/imagingstudy/1"
                                     )
        annotator.add_measurements("sub-001", mi).save()

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

        # update dataset uuid
        annotator.update_dataset("uuid", "aaxaaa")
        annotator.save()

        # update patient uuid
        annotator.update_patient(subject="sub-001", field="uuid", value="sparc-patient-sub-001").save()

        # update patient observation
        observations = annotator.update_patient_measurements(subject="sub-001", category="ObservationMeasurement")
        ob = observations[0]
        assert isinstance(ob, ObservationMeasurement)
        ob.set_uuid("sparc-patient-sub-001-observation-uuid-xx01")
        annotator.save()

        # update patient ImagingStudy uuid and endpoint url
        image_studies = annotator.update_patient_measurements(subject="sub-001", category="ImagingStudyMeasurement")
        image_study = image_studies[0]
        assert isinstance(image_study, ImagingStudyMeasurement)
        image_study.set_uuid("sparc-patient-sub001-image-uuid-xxx-ss01").set_endpoint_url("http://localhost:8000/fhir")
        annotator.save()

        # update patient ImagingStudy series's uuid and endpoint url
        series = image_study.get_series()
        s = series[0]
        assert isinstance(s, ImagingStudySeries)
        s.set_endpoint_uuid("sparc-patient-imagingstudy-series-01-xxx-001").set_endpoint_url(
            "http://localhost:8000/fhir/series")
        annotator.save()

        # update document reference uuid
        document_references = annotator.update_patient_measurements("sub-001", category="DocumentReferenceMeasurement")
        document = document_references[0]
        assert isinstance(document, DocumentReferenceMeasurement)
        document.set_uuid("sparc-patient-document-uuid-0001")
        annotator.save()

    def test_workflow_annotator(self):
        annotator = Annotator("./dataset/workflow").workflow()
        pprint(annotator.descriptions)


if __name__ == '__main__':
    test = Test()
    test.test_measurements_annotator()
    # test.test_measurements_annotator_update_mode()
    # test.test_workflow_annotator()
