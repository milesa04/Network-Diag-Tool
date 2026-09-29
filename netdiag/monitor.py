import time
from datetime import datetime

from netdiag.diagnostics import diagnose


def monitor(check_functions, history, interval=30):
    print("Starting network monitor...")
    print(f"Interval: {interval} seconds")
    print("Press Ctrl+C to stop.")
    print()

    try:
        while True:
            results = []

            for check_function in check_functions:
                result = check_function()
                results.append(result)

            timestamp = datetime.now().strftime("%H:%M:%S")

            passed = sum(result.success for result in results)
            total = len(results)

            status = "HEALTHY" if passed == total else "DEGRADED"

            print(f"[{timestamp}] {status} — {passed}/{total} checks passed")

            run_id = history.create_run(
                datetime.now().isoformat()
            )

            for result in results:
                history.add_check(run_id, result)

            diagnoses = diagnose(results)

            for diagnosis in diagnoses:
                history.add_diagnosis(run_id, diagnosis)

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")