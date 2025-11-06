from fhir_cda import Annotator
from fhir_cda.ehr.elements import ImagingStudySeries
from fhir_cda.utils import check_first_file_extension, read_dataset_samples
from fhir_cda.ehr import ObservationMeasurement, ObservationValue, Quantity, DocumentReferenceMeasurement, \
    ImagingStudyMeasurement
from pathlib import Path
from typing import Union
from pprint import pprint
import time
import json


class Test:

    def test_workflow_annotator(self):
        start_time = time.time()
        print(start_time)
        fhir_note = "[{\"name\":\"extract_clinical_measurements\",\"id\":\"a810a616-1bca-4adb-9350-998b606e6860\",\"uuid\":\"sparc-tool-$07ef3cda-e90e-41ab-92d1-2c867027244b\",\"tool_fhir_note\":{\"name\":\"extract_clinical_measurements\",\"inputs\":[{\"name\":\"surface_mesh_ply_scapula\",\"resource\":\"DocumentReference\"},{\"name\":\"surface_mesh_ply_humerus\",\"resource\":\"DocumentReference\"},{\"name\":\"surface_mesh_ply_clavicle\",\"resource\":\"DocumentReference\"},{\"name\":\"surface_mesh_ply_thorax\",\"resource\":\"DocumentReference\"}],\"outputs\":[{\"name\":\"clinical_measurements_csv\",\"resource\":\"DocumentReference\",\"code\":\"\",\"system\":\"\",\"unit\":\"\"}]}},{\"name\":\"extract_clinical_measurements_csv\",\"id\":\"49092873-6386-48e3-8f4a-6fcb5978da2d\",\"uuid\":\"sparc-tool-$d5d32563-034c-4ca7-aaf1-2265328be251\",\"tool_fhir_note\":{\"name\":\"extract_clinical_measurements_csv\",\"inputs\":[{\"name\":\"clinical_measurements_csv\",\"resource\":\"DocumentReference\"}],\"outputs\":[{\"name\":\"l_inferior_angle\",\"resource\":\"Observation\",\"code\":\"000001\",\"system\":\"https://www.auckland.ac.nz/en/abi/our-research/research-groups-themes/12-Labours.html\",\"unit\":\"deg\"},{\"name\":\"l_version_angle\",\"resource\":\"Observation\",\"code\":\"000002\",\"system\":\"https://www.auckland.ac.nz/en/abi/our-research/research-groups-themes/12-Labours.html\",\"unit\":\"deg\"},{\"name\":\"r_inferior_angle\",\"resource\":\"Observation\",\"code\":\"000003\",\"system\":\"https://www.auckland.ac.nz/en/abi/our-research/research-groups-themes/12-Labours.html\",\"unit\":\"deg\"},{\"name\":\"r_version_angle\",\"resource\":\"Observation\",\"code\":\"000004\",\"system\":\"https://www.auckland.ac.nz/en/abi/our-research/research-groups-themes/12-Labours.html\",\"unit\":\"deg\"}]}}]"
        fhir = json.loads(fhir_note)
        fhir[1]["tool_fhir_note"]["outputs"].extend([{'name': 'nrrd images', 'resource': 'ImagingStudy'},
                                                     {'name': 'jpg image', 'resource': 'DocumentReference'},
                                                     {'name': 'vtk model', 'resource': 'DocumentReference'},
                                                     {'name': 'mhd model', 'resource': 'DocumentReference'},
                                                     {'name': 'breast dicom', 'resource': "ImagingStudy"}])
        assay_map = {
            "measurements": {
                "sub-1": {
                    "uuid": "sparc-result-sub-001",
                    "sams": [
                        {
                            "uuid": "sparc-measurement-sam-001",
                            "sample_type": "surface_mesh_ply_scapula"
                        },
                        {
                            "uuid": "sparc-measurement-sam-002",
                            "sample_type": "surface_mesh_ply_humerus"
                        },
                        {
                            "uuid": "sparc-measurement-sam-003",
                            "sample_type": "surface_mesh_ply_clavicle"
                        },
                        {
                            "uuid": "sparc-measurement-sam-004",
                            "sample_type": "surface_mesh_ply_thorax"
                        }
                    ]
                }
            },
            "results": {
                "sub-1": {
                    "uuid": "sparc-result-sub-001",
                    "sams": [
                        {
                            "dataset": "sparc-dataset-001",
                            "dataset_name": "new dataset",
                            "uuid": "sparc-result-sam-001",
                            "name": "sam-1",
                            "url": "http://localhost:9000/workflow-tools/createmesh_44ad158d/primary/sub-1/sam-1"
                        },
                        {
                            "dataset": "sparc-dataset-001",
                            "dataset_name": "new dataset",
                            "uuid": "sparc-result-sam-002",
                            "name": "sam-2",
                            "url": "http://localhost:9000/workflow-tools/createmesh_44ad158d/primary/sub-1/sam-2"
                        },
                        {
                            "dataset": "sparc-dataset-001",
                            "dataset_name": "new dataset",
                            "uuid": "sparc-result-sam-003",
                            "name": "sam-3",
                            "url": "http://localhost:9000/workflow-tools/createmesh_44ad158d/primary/sub-1/sam-3"
                        },
                        {
                            "dataset": "sparc-dataset-001",
                            "dataset_name": "new dataset",
                            "uuid": "sparc-result-sam-004",
                            "name": "sam-4",
                            "url": "http://localhost:9000/workflow-tools/createmesh_44ad158d/primary/sub-1/sam-4"
                        },
                        {
                            "dataset": "sparc-dataset-001",
                            "dataset_name": "new dataset",
                            "uuid": "sparc-result-sam-005",
                            "name": "sam-5",
                            "url": "http://localhost:9000/workflow-tools/createmesh_44ad158d/primary/sub-1/sam-5"
                        },
                        {
                            "dataset": "sparc-dataset-001",
                            "dataset_name": "new dataset",
                            "uuid": "sparc-result-sam-006",
                            "name": "sam-6",
                            "url": "http://localhost:9000/workflow-tools/createmesh_44ad158d/primary/sub-1/sam-6"
                        },
                        {
                            "dataset": "sparc-dataset-001",
                            "dataset_name": "new dataset",
                            "uuid": "sparc-result-sam-007",
                            "name": "sam-7",
                            "url": "http://localhost:9000/workflow-tools/createmesh_44ad158d/primary/sub-1/sam-7"
                        },
                        {
                            "dataset": "sparc-dataset-001",
                            "dataset_name": "new dataset",
                            "uuid": "sparc-result-sam-008",
                            "name": "sam-8",
                            "url": "http://localhost:9000/workflow-tools/createmesh_44ad158d/primary/sub-1/sam-8"
                        },
                        {
                            "dataset": "sparc-dataset-002",
                            "dataset_name": "breast mri dcm",
                            "uuid": "sparc-result-sam-009",
                            "name": "sam-9",
                            "url": "http://localhost:9000/workflow-tools/createmesh_44ad158d/primary/sub-1/sam-9"
                        }
                    ]
                }
            },
            "workflow": {
                "uuid": "sparc-workflow-001",
                "tools": []
            }
        }
        for tool in fhir:
            assay_map["workflow"]["tools"].append({
                "uuid": tool["uuid"],
                "inputs": tool["tool_fhir_note"]["inputs"],
                "outputs": tool["tool_fhir_note"]["outputs"],
            })
        annotator = Annotator("./dataset/process/ep2-workflow2-result").process(assay_map)

        annotator.update_study(uuid="sparc-study-ep2-001",
                               name="investigating coupling between upper limb bones").update_assay(
            uuid="sparc-assay-ep2-001",
            name="Extracting the clinical measurements from the patient model").update_researcher(
            uuid="sparc-researcher-ep2-001")

        # annotator.update_uuid("tool-1").update_title("create_nifti").update_version("1.0.0")
        # # EP1
        annotator.save()

        end_time = time.time()
        print(end_time)
        elapsed_time = end_time - start_time
        print(f"Function took {elapsed_time:.4f} seconds to complete.")


if __name__ == '__main__':
    test = Test()
    test.test_workflow_annotator()
    # test.test_measurements_annotator_update_mode()
    # test.test_workflow_annotator()
