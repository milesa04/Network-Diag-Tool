############################## Models ############################
#
#     Defines the data models used in the network diagnostic tool.
#



from dataclasses import dataclass
from typing import Optional


@dataclass
class CheckResult:
    name: str
    success: bool
    message: str
    duration: float
    details: Optional[dict] = None

@dataclass
class Diagnosis:
    problem: str
    severity: str
    cause: str
    recommendations: list[str]


