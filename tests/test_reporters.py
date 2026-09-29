import json

from netdiag.models import CheckResult, Diagnosis
from netdiag.reporters import print_json


def test_print_json(capsys):
    results = [
        CheckResult(
            name="DNS Resolution",
            success=True,
            message="DNS working",
            duration=0.01
        )
    ]

    diagnoses = [
        Diagnosis(
            problem="NO_PROBLEMS_DETECTED",
            severity="HEALTHY",
            cause="All selected network diagnostics completed successfully.",
            recommendations=["No action required"]
        )
    ]

    print_json(results, diagnoses)

    captured = capsys.readouterr()
    output = json.loads(captured.out)

    assert output["checks"][0]["name"] == "DNS Resolution"
    assert output["checks"][0]["success"] is True
    assert output["diagnoses"][0]["problem"] == "NO_PROBLEMS_DETECTED"