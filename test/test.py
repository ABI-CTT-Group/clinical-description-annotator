from fhir_cda import Annotator
from fhir_cda.ehr import Measurement
from typing import Union
from pprint import pprint
import time


class Test:

    def test_annotator(self):
        start_time = time.time()
        annotator = Annotator("./dataset/dataset-sparc")

        #
        m = Measurement(value="0.15", code="21889-1", units="cm")
        annotator.add_measurements(["sub-001"], [m]).save()

        annotator.add_measurements("sub-002", Measurement(value="25", code="30525-0", units="year", code_system="http://loinc.org"))

        annotator.add_measurements(["sub-001", "sub-002"], Measurement(value="170", code="8302-2", units="cm"))

        annotator.save()

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Function took {elapsed_time:.4f} seconds to complete.")



if __name__ == '__main__':
    test = Test()
    test.test_annotator()
