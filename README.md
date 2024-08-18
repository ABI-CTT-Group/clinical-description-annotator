# Clinic Description Annotator

## Usage

## Annotator measurements for SPARC SDS dataset

- Add measurement for one patient
```py
from fhir_cda import Annotator
from fhir_cda.ehr import Measurement

annotator = Annotator("./dataset/dataset-sparc")

m = Measurement(value="0.15", code="21889-1", units="cm")
annotator.add_measurements("sub-001", m).save()
```
- Add measurements for one patient
```py
m1 = Measurement(value="0.15", code="21889-1", units="cm")
m2 = Measurement(value="0.15", code="21889-1", units="cm", code_system="http://loinc.org", units_system="http://unitsofmeasure.org")
annotator.add_measurements("sub-001", [m1, m2]).save()
```

- Add measurement for multiple patients
```py
m = Measurement(value="0.15", code="21889-1", units="cm")
annotator.add_measurements(["sub-001", "sub-002"], m).save()
```

- A measurements for multiple patients

```py
m1 = Measurement(value="0.15", code="21889-1", units="cm")
m2 = Measurement(value="0.15", code="21889-1", units="cm", code_system="http://loinc.org", units_system="http://unitsofmeasure.org")
annotator.add_measurements(["sub-001", "sub-002"], [m1, m2])
annotator.save()
```