from typing import Optional
from .elements import ObservationValue


class ObservationMeasurement:
    def __init__(self, value: ObservationValue, code: str, code_system="http://loinc.org",
                 display: Optional[str] = None):

        if not isinstance(value, ObservationValue):
            raise ValueError(f"value={value} is not an ObservationValue type")
        elif not isinstance(code, str):
            raise ValueError(f"code={code} is not an instance of type str")
        elif display is not None and not isinstance(display, str):
            raise ValueError(f"display={display} is not an instance of type str")

        self.measurement_type = "ObservationMeasurement"
        self.value = value
        self.code = code
        self.code_system = code_system
        self.display = display

    def __repr__(self):
        return (f"ObservationMeasurement(value={self.value}, code='{self.code}', value_system='{self.code_system}')")

    def get(self):
        measurement = {
            "value": self.value.get(),
            "code": self.code,
            "codeSystem": self.code_system,
            "display": self.display if isinstance(self.display, str) else ""
        }
        return {k: v for k, v in measurement.items() if v not in ("", None)}


class DocumentReferenceMeasurement:
    def __init__(self, url: str, content_type: str, title: str):

        if not isinstance(url, str):
            raise ValueError(f"url={url} is not an instance of type str")
        elif not isinstance(content_type, str):
            raise ValueError(f"content_type={content_type} is not an instance of type str")
        elif not isinstance(title, str):
            raise ValueError(f"title={title} is not an instance of type str")

        self.measurement_type = "DocumentReferenceMeasurement"
        self.url = url
        self.content_type = content_type
        self.title = title

    def __repr__(self):
        return (f"DocumentReferenceMeasurement(url={self.url}, content_type={self.content_type}, title={self.title})")

    def get(self):
        measurement = {
            "url": self.url,
            "contentType": self.content_type,
            "title": self.title
        }
        return {k: v for k, v in measurement.items() if v not in ("", None)}
