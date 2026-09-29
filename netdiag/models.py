from dataclasses import dataclass

############################## Models ############################
#
#     Defines the data models used in the network diagnostic tool.
#

@dataclass
class CheckResult:
    name: str
    success: bool
    message: str
    duration: float


@dataclass
class Diagnosis:
    problem: str
    severity: str
    cause: str
    recommendations: list[str]