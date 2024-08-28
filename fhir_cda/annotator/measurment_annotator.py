from pathlib import Path
import pydicom
from pydicom.uid import UID
from fhir_cda.terms import SNOMEDCT
from fhir_cda.ehr import Measurement
import json
from concurrent.futures import ThreadPoolExecutor
import os


class MeasurementAnnotator:

    def __init__(self, dataset_path):
        self.root = Path(dataset_path)
        self.descriptions = {}
        self._analysis_dataset()

    def _analysis_dataset(self):
        primary_folder = self.root / "primary"
        if not primary_folder.exists():
            self.descriptions = {}
            raise ValueError(
                'The dataset structure is not based on a SPARC SDS dataset format, please check it and try again!')

        self.descriptions["dataset"] = {
            "id": "",
            "uuid": "",
            "name": self.root.name,
            "path": "/",
        }

        self.descriptions["patients"] = []

        patients_dir = [x for x in primary_folder.iterdir() if x.is_dir()]

        for p in patients_dir:
            patient = {
                "id": "",
                "uuid": "",
                "name": p.name,
                "path": p.relative_to(self.root).as_posix(),
                "observations": [],
                "imagingStudy": self._analysis_dicom_study_samples(p)
            }
            self.descriptions["patients"].append(patient)

    def _analysis_dicom_study_samples(self, study):

        if study.exists():
            imaging_study = {
                "endpointUrl": "",
                "path": study.relative_to(self.root).as_posix(),
                "series": []
            }
            sams = [x for x in study.iterdir() if x.is_dir()]
            if len(sams) < 1:
                return imaging_study

            if len(self.descriptions["patients"]) < 5:
                for sam in sams:
                    s = self._read_sam(sam)
                    if s is not None:
                        imaging_study["series"].append(s)
            else:
                imaging_study["series"] = self._analysis_dicom_samples_worker(sams)

            return imaging_study

        return None

    def _read_sam(self, sam):
        try:
            dcm_files = list(sam.glob("*.dcm"))
            if len(dcm_files) < 1:
                return
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
        for d in dcms:
            dcm = pydicom.dcmread(d)

            # Get the SOP Class UID
            sop_class_uid = dcm.SOPClassUID
            # Get the SOP Class Name using the UID dictionary
            sop_class_name = UID(sop_class_uid).name

            instance = {
                "uid": dcm[(0x0008, 0x0018)].value,
                "sopClassUid": sop_class_uid,
                "sopClassName": sop_class_name,
                "number": dcm[(0x0020, 0x0013)].value
            }
            instances.append(instance)
        return instances

    def add_measurements(self, subjects, measurements):
        self.add_measurement(subjects, measurements)
        return self

    def add_measurement(self, subjects, measurement):
        if isinstance(subjects, list) and isinstance(measurement, list):
            for s in subjects:
                self.add_measurements_by_subject(s, measurement)
        elif isinstance(subjects, list) and isinstance(measurement, Measurement):
            m = measurement
            for s in subjects:
                self.add_measurement_by_subject(s, m)
        elif isinstance(subjects, str) and isinstance(measurement, list):
            s = subjects
            for m in measurement:
                self.add_measurement_by_subject(s, m)
        elif isinstance(subjects, str) and isinstance(measurement, Measurement):
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
        if not isinstance(measurement, Measurement):
            raise ValueError(f"measurement={measurement} is not an instance of type Measurement")
        subject_path = self.root / "primary" / subject
        if not subject_path.exists():
            raise ValueError(f"subject_path={subject_path} is not exists")

        matched_patient = [p for p in self.descriptions.get("patients") if
                           p.get("path") == subject_path.relative_to(self.root).as_posix()][0]
        matched_patient["observations"].append(measurement.get())

        return self

    def save(self, path=None):
        if path:
            save_path = Path(path) / "measurements.json"
        else:
            save_path = self.root / "measurements.json"

        with open(save_path, "w") as json_file:
            json.dump(self.descriptions, json_file, indent=4)
