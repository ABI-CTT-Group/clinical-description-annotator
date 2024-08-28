from typing import Optional, Literal, List


class Quantity:
    def __init__(self, value: Optional[float] = None, comparator: Optional[Literal["<", "<=", ">=", ">"]] = None,
                 unit: Optional[str] = None, system: Optional[str] = "http://unitsofmeasure.org",
                 code: Optional[str] = None):
        """
        :param value: Numerical value (with implicit precision) for Observation
        :param comparator: < | <= | >= | > - how to understand the value
        :param unit: Unit representation
        :param system: System that defines coded unit form
        :param code: Coded form of the unit
        """
        self.value = value
        self.comparator = comparator
        self.unit = unit
        self.system = system
        self.code = code

    def get(self):
        quantity = {
            "value": self.value if isinstance(self.value, float) or isinstance(self.value, int) else None,
            "comparator": self.comparator if self.comparator in ["<", "<=", ">=", ">"] else None,
            "unit": self.unit if isinstance(self.unit, str) else None,
            "system": self.system if isinstance(self.system, str) else None,
            "code": self.code if isinstance(self.code, str) else None
        }
        return {k: v for k, v in quantity.items() if v not in ("", None)}


class Coding:

    def __init__(self, system: str = "", version: str = "", code: str = "", display: Optional[str] = None,
                 user_selected: Optional[bool] = None):
        self.system = system
        self.version = version
        self.code = code
        self.display = display
        self.user_selected = user_selected

    def get(self):
        coding = {
            "system": self.system if isinstance(self.system, str) else None,
            "version": self.version if isinstance(self.version, str) else None,
            "code": self.code if isinstance(self.code, str) else None,
            "display": self.display if isinstance(self.display, str) else None,
            "userSelected": self.user_selected if isinstance(self.user_selected, bool) else None
        }
        return {k: v for k, v in coding.items() if v not in ("", None)}


class CodeableConcept:

    def __init__(self, codings: List[Coding] = None, text: str = ""):
        self.codings = codings
        self.text = text

    def get(self):
        codeableconcept = {
            "coding": [coding.get() for coding in self.codings if isinstance(coding, Coding)] if isinstance(
                self.codings, list) else None,
            "text": self.text if isinstance(self.text, str) else None
        }

        return {k: v for k, v in codeableconcept.items() if v not in ("", None, [])}


class Range:

    def __init__(self, low: Optional[float] = None, high: Optional[float] = None):
        self.low = low
        self.high = high

    def get(self):
        _range = {
            "low": self.low if isinstance(self.low, float) else None,
            "high": self.high if isinstance(self.high, float) else None
        }
        return {k: v for k, v in _range.items() if v not in ("", None)}


class Ratio:

    def __init__(self, numerator: Optional[Quantity] = None, denominator: Optional[Quantity] = None):
        self.numerator = numerator
        self.denominator = denominator

    def get(self):
        ratio = {
            "numerator": self.numerator.get() if isinstance(self.numerator, Quantity) else None,
            "denominator": self.denominator.get() if isinstance(self.denominator, Quantity) else None
        }
        return {k: v for k, v in ratio.items() if v not in ("", None)}


class SampledData:

    def __init__(self, origin: str, period: float, dimensions: int, factor: Optional[float] = None,
                 lower_limit: Optional[float] = None, upper_limit: Optional[float] = None, data: Optional[str] = None):
        self.origin = origin
        self.period = period
        self.dimensions = dimensions
        self.factor = factor
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.data = data

    def get(self):
        sampled_data = {
            "origin": self.origin if isinstance(self.origin, str) else None,
            "period": self.period if isinstance(self.period, float) else None,
            "factor": self.factor if isinstance(self.factor, float) else None,
            "lowerLimit": self.lower_limit if isinstance(self.lower_limit, float) else None,
            "upperLimit": self.upper_limit if isinstance(self.upper_limit, float) else None,
            "dimensions": self.dimensions if isinstance(self.dimensions, int) and self.dimensions > 0 else None,
            "data": self.data if isinstance(self.data, str) else None
        }
        return {k: v for k, v in sampled_data.items() if v not in ("", None)}


class Period:

    def __init__(self, start: str = '', end: str = ''):
        self.start = start
        self.end = end

    def get(self):
        period = {
            "start": self.start if isinstance(self.start, str) else None,
            "end": self.end if isinstance(self.end, str) else None
        }
        return {k: v for k, v in period.items() if v not in ("", None)}


class ObservationValue:

    def __init__(self, value_quantity: Optional[Quantity] = None,
                 value_codeable_concept: Optional[CodeableConcept] = None, value_string: Optional[str] = None,
                 value_boolean: Optional[bool] = None, value_integer: Optional[int] = None,
                 value_range: Optional[Range] = None, value_ratio: Optional[Ratio] = None,
                 value_sampled_data: Optional[SampledData] = None, value_time: Optional[str] = None,
                 value_date_time: Optional[str] = None, value_period: Optional[Period] = None):
        self.value_quantity = value_quantity
        self.value_codeable_concept = value_codeable_concept
        self.value_string = value_string
        self.value_boolean = value_boolean
        self.value_integer = value_integer
        self.value_range = value_range
        self.value_ratio = value_ratio
        self.value_sampled_data = value_sampled_data
        self.value_time = value_time
        self.value_date_time = value_date_time
        self.value_period = value_period

    def get(self):
        value = {
            "valueQuantity": self.value_quantity.get() if isinstance(self.value_quantity, Quantity) else None,
            "valueCodeableConcept": self.value_codeable_concept.get() if isinstance(self.value_codeable_concept,
                                                                                    CodeableConcept) else None,
            "valueString": self.value_string if isinstance(self.value_string, str) else None,
            "valueBoolean": self.value_boolean if isinstance(self.value_boolean, bool) else None,
            "valueInteger": self.value_integer if isinstance(self.value_integer, int) else None,
            "valueRange": self.value_range.get() if isinstance(self.value_range, Range) else None,
            "valueRatio": self.value_ratio.get() if isinstance(self.value_ratio, Ratio) else None,
            "valueSampledData": self.value_sampled_data.get() if isinstance(self.value_sampled_data,
                                                                            SampledData) else None,
            "valueTime": self.value_time if isinstance(self.value_time, str) else None,
            "valueDateTime": self.value_date_time if isinstance(self.value_date_time, str) else None,
            "valuePeriod": self.value_period.get() if isinstance(self.value_period, Period) else None
        }
        return {k: v for k, v in value.items() if v not in ("", None)}


class WorkflowGoal:

    def __init__(self, description: str):
        self.description = description

    def get(self):
        goal = {
            "description": self.description.get() if isinstance(self.description, str) else None,
        }
        return {k: v for k, v in goal.items() if v not in ("", None, [])}
