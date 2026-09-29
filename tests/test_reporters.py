import json

from netdiag.models import CheckResult, Diagnosis
from netdiag.reporters import print_json


def test_print_json(capsys):
    results = [
        CheckResult(
            name="Traceroute",
            success=True,
            message="Hop 1: 192.168.4.1 | Hop 2: 8.8.8.8",
            duration=0.01,
            details={
                "hop_count": 2,
                "unresponsive_hops": [],
                "destination_reached": True
            }
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

    assert output["checks"][0]["name"] == "Traceroute"
    assert output["checks"][0]["success"] is True

    assert output["checks"][0]["details"] == {
        "hop_count": 2,
        "unresponsive_hops": [],
        "destination_reached": True
    }

    assert output["diagnoses"][0]["problem"] == "NO_PROBLEMS_DETECTED"