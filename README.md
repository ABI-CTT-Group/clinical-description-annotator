# Clinical Description Annotator

![Python3.9+](https://img.shields.io/badge/python_3.9+-34d399)
![PyPI - Version](https://img.shields.io/pypi/v/fhir-cda)

Annotator for annotating measurement results, workflows, workflow tools, models, and workflow tool process datasets in
SPARC SDS datasets to the data format required for digitaltwins-on-fhir.

## Usage

## Annotator measurements for SPARC SDS dataset

- Add measurement for one patient

```py
from fhir_cda import Annotator
from fhir_cda.ehr import Measurement, ObservationValue, Quantity

annotator = Annotator("./dataset/dataset-sparc").measurements()

m = Measurement(
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
m1 = Measurement(
    value=ObservationValue(
        value_quantity=Quantity(
            value=0.15,
            unit="cm",
            code="cm")),
    code="21889-1")
m2 = Measurement(
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
m = Measurement(
    value=ObservationValue(value_string="Female"),
    code="99502-7",
    display="Recorded sex or gender",
    code_system="http://loinc.org")
annotator.add_measurements(["sub-001", "sub-002"], m).save()
```

- A measurements for multiple patients

```py
m1 = Measurement(
    value=ObservationValue(value_string="Female"),
    code="99502-7",
    display="Recorded sex or gender",
    code_system="http://loinc.org")
m2 = Measurement(
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

- Notice: The default value for `unit system` and `code system` are:

```python
unit_system = "http://unitsofmeasure.org"
code_system = "http://loinc.org"
```