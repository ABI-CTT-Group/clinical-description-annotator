# Clinical Description Annotator

![Python3.9+](https://img.shields.io/badge/python_3.9+-34d399)
![PyPI - Version](https://img.shields.io/pypi/v/fhir-cda)

Annotator for annotating measurement results, workflows, workflow tools, models, and workflow tool process datasets in
SPARC SDS datasets to the data format required for [digitaltwins-on-fhir](https://pypi.org/project/digitaltwins-on-fhir/).

## Usage

## Annotate the measurements data for SPARC SDS dataset

- Add measurement for one patient

```py
from fhir_cda import Annotator
from fhir_cda.ehr import ObservationMeasurement, ObservationValue, Quantity

annotator = Annotator("./dataset/dataset-sparc").measurements()

m = ObservationMeasurement(
    value=ObservationValue(
        value_quantity=Quantity(
            value=30,
            unit="year",
            code="a")),
    code="30525-0")

annotator.add_measurements("sub-001", m).save()
```

- Add measurements for one patient

```py
m1 = ObservationMeasurement(
    value=ObservationValue(
        value_quantity=Quantity(
            value=0.15,
            unit="cm",
            code="cm")),
    code="21889-1")
m2 = ObservationMeasurement(
    value=ObservationValue(
        value_quantity=Quantity(
            value=0.15,
            unit="cm",
            code="cm",
            system="http://unitsofmeasure.org")),
    code="21889-1",
    code_system="http://loinc.org",
    display="Size Tumor")
annotator.add_measurements("sub-001", [m1, m2]).save()
```

- Add measurement for multiple patients

```py
m = ObservationMeasurement(
    value=ObservationValue(value_string="Female"),
    code="99502-7",
    display="Recorded sex or gender",
    code_system="http://loinc.org")
annotator.add_measurements(["sub-001", "sub-002"], m).save()
```

- A measurements for multiple patients

```py
m1 = ObservationMeasurement(
    value=ObservationValue(value_string="Female"),
    code="99502-7",
    display="Recorded sex or gender",
    code_system="http://loinc.org")
m2 = ObservationMeasurement(
    value=ObservationValue(
        value_quantity=Quantity(
            value=0.15,
            unit="cm",
            code="cm",
            system="http://unitsofmeasure.org")),
    code="21889-1",
    code_system="http://loinc.org",
    display="Size Tumor")
annotator.add_measurements(["sub-001", "sub-002"], [m1, m2])
annotator.save()
```
- Add DocumentReference measurements
```python
from fhir_cda.ehr import DocumentReferenceMeasurement
m2 = DocumentReferenceMeasurement(
        url="https://example.org/files/mesh-breast-surface-df0c4efd-69a6-428a-ba70-786caecfadfb.obj",
        content_type="model/obj",
        title="Breast Surface Mesh")
annotator.add_measurements(["sub-001"], [m2]).save()
```


- Notice: The default value for `unit system` and `code system` are:

```python
unit_system = "http://unitsofmeasure.org"
code_system = "http://loinc.org"
```

## Design Decisions
- `ImagingStudy Instances` are not include at this stage, because but can be added it if required. 

## Contributors

<div style="display: flex; flex-direction: row; flex-wrap: wrap; gap: 20px">
    <div style="flex: 1; min-width: 300px">
        <div style="display: flex; align-items: center; margin-bottom: 15px">
            <a href="https://github.com/LinkunGao">
                <img src="https://avatars.githubusercontent.com/LinkunGao" width="50" height="50" style="border-radius: 50%" alt="LinkunGao"/>
            </a>
            <span style="margin-left: 10px;">Linkun Gao</span>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 15px">
            <a href="https://github.com/chinchien-lin">
                <img src="https://avatars.githubusercontent.com/chinchien-lin" width="50" height="50" style="border-radius: 50%" alt="chinchien-lin"/>
            </a>
            <span style="margin-left: 10px;">Chinchien Lin</span>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 15px">
            <a href="https://profiles.auckland.ac.nz/g-sands">
                <img src="https://profiles.auckland.ac.nz/g-sands/thumbnail" width="50" height="50" style="border-radius: 50%" alt="Gregory Sands"/>
            </a>
            <span style="margin-left: 10px;">Gregory Sands</span>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 15px">
            <a href="https://profiles.auckland.ac.nz/tp-babarendagamage">
                <img src="https://profiles.auckland.ac.nz/tp-babarendagamage/thumbnail" width="50" height="50" style="border-radius: 50%" alt="Prasad"/>
            </a>
            <span style="margin-left: 10px;">Thiranja Prasad Babarenda Gamage</span>
        </div>
    </div>
    <div style="flex: 1; min-width: 300px">
        <div style="display: flex; align-items: center; margin-bottom: 15px">
            <a href="https://profiles.auckland.ac.nz/a-elsayed">
                <img src="https://profiles.auckland.ac.nz/a-elsayed/thumbnail" width="50" height="50" style="border-radius: 50%" alt="Ayah Elsayed"/>
            </a>
            <span style="margin-left: 10px;">Ayah Elsayed</span>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 15px">
            <a href="https://profiles.auckland.ac.nz/jiali-xu">
                <img src="https://profiles.auckland.ac.nz/jiali-xu/thumbnail" width="50" height="50" style="border-radius: 50%" alt="Jiali Xu"/>
            </a>
            <span style="margin-left: 10px;">Jiali Xu</span>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 15px">
            <a href="https://profiles.auckland.ac.nz/d-nickerson">
                <img src="https://profiles.auckland.ac.nz/d-nickerson/thumbnail" width="50" height="50" style="border-radius: 50%" alt="David Nickerson"/>
            </a>
            <span style="margin-left: 10px;">David Nickerson</span>
        </div>
    </div>
</div>

## Publications

1. **[Paper Title One](https://doi.org/...)**, Author1, Author2. *Journal Name*, Year.
2. **[Paper Title Two](https://arxiv.org/abs/...)**, Author1, Author2. *Conference Name*, Year.

Please cite the corresponding paper if you use this project in your research.

