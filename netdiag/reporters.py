############################# Reporters ############################
#
#     Provides the reporting logic for the network diagnostic tool.
#

import json


def print_results(results):
    print("\n================================")
    print("       NETWORK DIAGNOSTICS")
    print("================================\n")

    for result in results:
        if result.success:
            print(f"✓ {result.name}")
        else:
            print(f"✗ {result.name}")

        print(f"  {result.message}")
        print(f"  Duration: {result.duration:.3f}s")
        print()

    passed = sum(result.success for result in results)
    total = len(results)

    print("--------------------------------")
    print(f"Checks Passed: {passed}/{total}")

    if passed == total:
        print("Overall Status: HEALTHY")
    elif passed == 0:
        print("Overall Status: OFFLINE")
    else:
        print("Overall Status: DEGRADED")

    print("--------------------------------")


def print_diagnoses(diagnoses):
    print("\n================================")
    print("          DIAGNOSIS")
    print("================================\n")

    for diagnosis in diagnoses:
        print(f"Problem: {diagnosis.problem}")
        print(f"Severity: {diagnosis.severity}")
        print(f"Cause: {diagnosis.cause}")
        print("Recommendations:")

        for recommendation in diagnosis.recommendations:
            print(f"  - {recommendation}")

        print()



def print_json(results, diagnoses):
    output = {
        "checks": [
            {
                "name": result.name,
                "success": result.success,
                "message": result.message,
                "duration": round(result.duration, 3),
                "details": result.details
            }
            for result in results
        ],
        "diagnoses": [
            {
                "problem": diagnosis.problem,
                "severity": diagnosis.severity,
                "cause": diagnosis.cause,
                "recommendations": diagnosis.recommendations
            }
            for diagnosis in diagnoses
        ]
    }

    print(json.dumps(output, indent=2))