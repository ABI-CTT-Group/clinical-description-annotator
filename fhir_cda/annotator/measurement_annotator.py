from abc import ABC
from .abstract_annotator import AbstractAnnotator

from fhir_cda.ehr import ObservationMeasurement, DocumentReferenceMeasurement, ImagingStudyMeasurement
import json

from ..utils import check_first_file_extension
from pathlib import Path


class MeasurementAnnotator(AbstractAnnotator, ABC):

    def __init__(self, dataset_path, mode="default"):
        """

        :param dataset_path:
        :param mode: string, "default" or "update"
        """
        super().__init__(dataset_path, "measurements")
        self._patient_paths = []
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
        self._patient_paths = [x for x in primary_folder.iterdir() if x.is_dir()]
        for p in self._patient_paths:
            patient = {
                "uuid": "",
                "name": p.name,
                "observations": [],
                "imagingStudy": [],
                "documentReference": [],
            }
            self.descriptions["patients"].append(patient)

    def automated_generating_imaging_study_measurement_by_scan_dataset(self):
        print(self._patient_paths)
        for path, patient in zip(self._patient_paths, self.descriptions["patients"]):
            patient["imagingStudy"] = self._analysis_imaging_study_samples(path)

    @staticmethod
    def _analysis_imaging_study_samples(study):
        imaging_studies = []
        if study.exists():
            sams = [x for x in study.iterdir() if x.is_dir()]
            if len(sams) < 1:
                return imaging_studies
            else:
                dcm_sams = [sam for sam in sams if check_first_file_extension(sam) == "dcm"]
                nrrd_sams = [sam for sam in sams if check_first_file_extension(sam) == "nrrd"]
            if len(dcm_sams) > 0:
                imaging_study = ImagingStudyMeasurement(sample_paths=dcm_sams, description="dcm")
                if len(imaging_study.series) > 0:
                    imaging_studies.append(imaging_study.get())
            if len(nrrd_sams) > 0:
                imaging_study = ImagingStudyMeasurement(sample_paths=nrrd_sams, description="nrrd")
                if len(imaging_study.series) > 0:
                    imaging_studies.append(imaging_study.get())
        return imaging_studies

    def add_measurements(self, subjects, measurements):
        self.add_measurement(subjects, measurements)
        return self

    def add_measurement(self, subjects, measurement):
        if isinstance(subjects, list) and isinstance(measurement, list):
            for s in subjects:
                self.add_measurements_by_subject(s, measurement)
        elif isinstance(subjects, list) and isinstance(measurement, (ObservationMeasurement, DocumentReferenceMeasurement, ImagingStudyMeasurement)):
            m = measurement
            for s in subjects:
                self.add_measurement_by_subject(s, m)
        elif isinstance(subjects, str) and isinstance(measurement, list):
            s = subjects
            for m in measurement:
                self.add_measurement_by_subject(s, m)
        elif isinstance(subjects, str) and isinstance(measurement, (ObservationMeasurement, DocumentReferenceMeasurement, ImagingStudyMeasurement)):
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
        if not isinstance(measurement, (ObservationMeasurement, DocumentReferenceMeasurement, ImagingStudyMeasurement)):
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
        elif measurement.measurement_type == "ImagingStudyMeasurement":
            matched_patient["imagingStudy"].append(measurement.get())
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
