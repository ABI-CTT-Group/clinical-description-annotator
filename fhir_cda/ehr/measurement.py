from typing import Optional
from .elements import ObservationValue


class Measurement:
    def __init__(self, value: ObservationValue, code: str, code_system="http://loinc.org",
                 display: Optional[str] = None):

        if not isinstance(value, ObservationValue):
            raise ValueError(f"value={value} is not an ObservationValue type")
        elif not isinstance(code, str):
            raise ValueError(f"code={code} is not an instance of type str")
        elif display is not None and not isinstance(display, str):
            raise ValueError(f"display={display} is not an instance of type str")

        self.value = value
        self.code = code
        self.code_system = code_system
        self.display = display

    def __repr__(self):
        return (f"Measurement(value={self.value}, code='{self.code}', value_system='{self.code_system}')")

    def get(self):
        measurement = {
            "value": self.value.get(),
            "code": self.code,
            "codeSystem": self.code_system,
            "display": self.display if isinstance(self.display, str) else ""
        }
        return {k: v for k, v in measurement.items() if v not in ("", None)}
