from fhir_cda import Annotator
from fhir_cda.ehr import Measurement, ObservationValue, Quantity
from typing import Union
from pprint import pprint
import time


class Test:

    def test_annotator(self):
        start_time = time.time()
        annotator = Annotator("./dataset/dataset-sparc")

        #
        m = Measurement(value=ObservationValue(value_quantity=Quantity(value=30, unit="year", code="a")),
                        code="30525-0")
        annotator.add_measurements(["sub-001"], [m]).save()

        annotator.add_measurements("sub-002", Measurement(value=ObservationValue(value_string="M"), code="99502-7",
                                                          code_system="https://loinc.org",
                                                          display="Recorded sex or gender"))

        annotator.add_measurements(["sub-001", "sub-002"], Measurement(
            value=ObservationValue(value_quantity=Quantity(value=175, unit="cm", code="cm")), code="8302-2",
            display="Body height"))

        annotator.save()

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Function took {elapsed_time:.4f} seconds to complete.")


if __name__ == '__main__':
    test = Test()
    test.test_annotator()
