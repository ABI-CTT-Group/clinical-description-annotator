from typing import Union, Optional


class Measurement:
    def __init__(self, value: Union[str, int, float], code: str, unit: str, code_system="http://loinc.org",
                 unit_system="http://unitsofmeasure.org", display: Optional[str] = None):

        if not isinstance(value, (str, int, float)) or isinstance(value, bool):
            raise ValueError(f"value={value} is not an instance of any of the types in the tuple (str, int, float)")
        elif not isinstance(code, str):
            raise ValueError(f"code={code} is not an instance of type str")
        elif not isinstance(unit, str):
            raise ValueError(f"units={unit} is not an instance of type str")
        elif not isinstance(code_system, str):
            raise ValueError(f"value_system={code_system} is not an instance of type str")
        elif not isinstance(unit_system, str):
            raise ValueError(f"units_system={unit_system} is not an instance of type str")
        elif display is not None and not isinstance(unit_system, str):
            raise ValueError(f"display={display} is not an instance of type str")

        self.value = value
        self.code = code
        self.unit = unit
        self.code_system = code_system
        self.unit_system = unit_system
        self.display = display

    def __repr__(self):
        return (f"Measurement(value={self.value}, code='{self.code}', unit='{self.unit}', "
                f"value_system='{self.code_system}', unit_system='{self.unit_system}')")

    def get(self):
        return {
            "value": self.value,
            "code": self.code,
            "unit": self.unit,
            "codeSystem": self.code_system,
            "unitSystem": self.unit_system,
            "display": self.display if isinstance(self.display, str) else ""
        }
