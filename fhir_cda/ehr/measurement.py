from typing import Union


class Measurement:
    def __init__(self, value: Union[str, int, float], code: str, units: str, code_system="http://loinc.org",
                 units_system="http://unitsofmeasure.org"):

        if not isinstance(value, (str, int, float)) or isinstance(value, bool):
            raise ValueError(f"value={value} is not an instance of any of the types in the tuple (str, int, float)")
        elif not isinstance(code, str):
            raise ValueError(f"code={code} is not an instance of type str")
        elif not isinstance(units, str):
            raise ValueError(f"units={units} is not an instance of type str")
        elif not isinstance(code_system, str):
            raise ValueError(f"value_system={code_system} is not an instance of type str")
        elif not isinstance(units_system, str):
            raise ValueError(f"units_system={units_system} is not an instance of type str")

        self.value = value
        self.code = code
        self.units = units
        self.code_system = code_system
        self.units_system = units_system

    def __repr__(self):
        return (f"Measurement(value={self.value}, code='{self.code}', units='{self.units}', "
                f"value_system='{self.code_system}', units_system='{self.units_system}')")

    def get(self):
        return {
            "value": self.value,
            "code": self.code,
            "units": self.units,
            "codeSystem": self.code_system,
            "unitsSystem": self.units_system
        }
