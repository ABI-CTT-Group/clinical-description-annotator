from abc import ABC
from .abstract_annotator import AbstractAnnotator
import pydicom
from pydicom.uid import UID
from fhir_cda.terms import SNOMEDCT
from fhir_cda.ehr import ObservationMeasurement, DocumentReferenceMeasurement
import json
from concurrent.futures import ThreadPoolExecutor
import os
from ..utils import check_first_file_extension


class MeasurementAnnotator(AbstractAnnotator, ABC):

    def __init__(self, dataset_path, mode="default"):
        """

        :param dataset_path:
        :param mode: string, "default" or "update"
        """
        super().__init__(dataset_path, "measurements")
        if mode == "update":
            self._read_measurements()
        else:
            self._analysis_dataset()

    def _read_measurements(self):
        measurements_path = self.root / "measurements.json"
        if not measurements_path.exists():
            raise ValueError("Measurements file does not exist")
        else:
            with open(measurements_path, "r") as f:
                self.descriptions = json.load(f)

    def _analysis_dataset(self):
        primary_folder = self.root / "primary"
        if not primary_folder.exists():
            self.descriptions = {}
            raise ValueError(
                'The dataset structure is not based on a SPARC SDS dataset format, please check it and try again!')
        self.descriptions["dataset"] = {
            "uuid": "",
            "name": self.root.name,
        }
        self.descriptions["patients"] = []
        patients_dir = [x for x in primary_folder.iterdir() if x.is_dir()]
        for p in patients_dir:
            patient = {
                "uuid": "",
                "name": p.name,
                "observations": [],
                "imagingStudy": self._analysis_imaging_study_samples(p),
                "documentReference": [],
            }
            self.descriptions["patients"].append(patient)

    def _analysis_imaging_study_samples(self, study):
        imaging_studies = []
        if study.exists():
            sams = [x for x in study.iterdir() if x.is_dir()]
            if len(sams) < 1:
                return imaging_studies
            else:
                dcm_sams = [sam for sam in sams if check_first_file_extension(sam) == "dcm"]
                nrrd_sams = [sam for sam in sams if check_first_file_extension(sam) == "nrrd"]
            if len(dcm_sams) > 0:
                imaging_study = self._generate_imaging_study(dcm_sams, "dcm")
                if len(imaging_study["series"]) > 0:
                    imaging_studies.append(imaging_study)
            if len(nrrd_sams) > 0:
                imaging_study = self._generate_imaging_study(nrrd_sams, "nrrd")
                if len(imaging_study["series"]) > 0:
                    imaging_studies.append(imaging_study)
        return imaging_studies

    def _generate_imaging_study(self, sams, description):
        imaging_study = {
            "endpointUrl": "",
            "description": description,
            "series": []
        }
        if len(self.descriptions["patients"]) < 5:
            for sam in sams:
                s = self._read_sam(sam)
                if s is not None:
                    imaging_study["series"].append(s)
        else:
            imaging_study["series"] = self._analysis_dicom_samples_worker(sams)

        return imaging_study

    def _read_sam(self, sam):
        try:
            dcm_files = list(sam.glob("*.dcm"))
            nrrd_files = list(sam.glob("*.nrrd"))
            if len(dcm_files) < 1 and len(nrrd_files) < 1:
                return
            if len(dcm_files) > 0 and len(nrrd_files) > 0:
                raise ValueError("dataset format error: Detected dcm and nrrd files under the same sample folder.")

            if len(dcm_files) >= 1:
                s_dicom_file = pydicom.dcmread(dcm_files[0])
                body_part_examined = s_dicom_file.get((0x0018, 0x0015), None)
                body_site = SNOMEDCT.get(body_part_examined.value.upper(),
                                         None) if body_part_examined is not None else None

                suid = s_dicom_file.get((0x0020, 0x000e), None)
                s = {
                    "endpointUrl": "",
                    "uid": suid.value if suid is not None else "",
                    "name": sam.name,
                    "numberOfInstances": len(dcm_files),
                    "bodySite": body_site,
                    "instances": self._analysis_dicom_sample_instances(dcm_files)
                }
                return s
            if len(nrrd_files) >= 1:
                s = {
                    "endpointUrl": "",
                    "uid": None,
                    "name": sam.name,
                    "numberOfInstances": len(nrrd_files),
                    "instances": []
                }
                return s
        except Exception as e:
            print(f"Error reading {sam}: {e}")
            return None

    def _analysis_dicom_samples_worker(self, sams):
        samples = []
        max_workers = os.cpu_count()
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = executor.map(self._read_sam, sams)

        for result in results:
            if result is not None:
                samples.append(result)

        return samples

    @staticmethod
    def _analysis_dicom_sample_instances(dcms):
        instances = []
        # TODO: 14/05/2025 decision: not consider the instance level at this stage
        # for d in dcms:
        #     dcm = pydicom.dcmread(d)
        #
        #     # Get the SOP Class UID
        #     sop_class_uid = dcm.SOPClassUID
        #     # Get the SOP Class Name using the UID dictionary
        #     sop_class_name = UID(sop_class_uid).name
        #
        #     instance = {
        #         "uid": dcm[(0x0008, 0x0018)].value,
        #         "sopClassUid": sop_class_uid,
        #         "sopClassName": sop_class_name,
        #         "number": dcm[(0x0020, 0x0013)].value
        #     }
        #     instances.append(instance)
        return instances

    def add_measurements(self, subjects, measurements):
        self.add_measurement(subjects, measurements)
        return self

    def add_measurement(self, subjects, measurement):
        if isinstance(subjects, list) and isinstance(measurement, list):
            for s in subjects:
                self.add_measurements_by_subject(s, measurement)
        elif isinstance(subjects, list) and (isinstance(measurement, ObservationMeasurement) or isinstance(measurement,
                                                                                                           DocumentReferenceMeasurement)):
            m = measurement
            for s in subjects:
                self.add_measurement_by_subject(s, m)
        elif isinstance(subjects, str) and isinstance(measurement, list):
            s = subjects
            for m in measurement:
                self.add_measurement_by_subject(s, m)
        elif isinstance(subjects, str) and (isinstance(measurement, ObservationMeasurement) or isinstance(measurement,
                                                                                                          DocumentReferenceMeasurement)):
            s = subjects
            m = measurement
            self.add_measurement_by_subject(s, m)
        return self

    def add_measurements_by_subject(self, subject, measurements):
        s = subject
        for m in measurements:
            self.add_measurement_by_subject(s, m)

        return self

    def add_measurement_by_subject(self, subject, measurement):
        if not isinstance(subject, str):
            raise ValueError(f"subject={subject} is not an instance of type str")
        if not (isinstance(measurement, ObservationMeasurement) or isinstance(measurement,
                                                                              DocumentReferenceMeasurement)):
            raise ValueError(f"measurement={measurement} is not an instance of type Measurement")
        subject_path = self.root / "primary" / subject
        if not subject_path.exists():
            raise ValueError(f"subject_path={subject_path} is not exists")

        matched_patient = self._find_matched_patient(subject)
        assert isinstance(matched_patient, dict)

        if measurement.measurement_type == "ObservationMeasurement":
            matched_patient["observations"].append(measurement.get())
        elif measurement.measurement_type == "DocumentReferenceMeasurement":
            matched_patient["documentReference"].append(measurement.get())
        return self

    def update_imaging_study_measurement_series_description(self, subject: str, imaging_study_order: int,
                                                            series_description: dict):
        matched_patient = self._find_matched_patient(subject)
        assert isinstance(matched_patient, dict)

        if len(matched_patient["imagingStudy"]) <= imaging_study_order:
            raise ValueError(f"imaging_study_order={imaging_study_order} is invalid")

        if not isinstance(series_description, dict):
            raise ValueError(f"series_description={series_description} is not an instance of type dict")
        for name, des in series_description.items():
            matched_series = [s for s in matched_patient["imagingStudy"][imaging_study_order]["series"] if
                              s.get("name") == name]
            if len(matched_series) <= 0:
                raise ValueError(f"series_name={name} is invalid")
            else:
                series = matched_series[0]
                series["description"] = des

    def _find_matched_patient(self, subject):
        matched_patients = [p for p in self.descriptions.get("patients", []) if
                            p.get("name") == subject]
        if len(matched_patients) == 0:
            raise ValueError(f"No patients found for {subject}")
        matched_patient = matched_patients[0]
        return matched_patient
