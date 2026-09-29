############################ Main Execution ############################
#
#     This is the main entry point for the network diagnostic tool. 
#     It runs a series of checks and outputs the results.
#

from datetime import datetime


from netdiag.checks import (
    check_gateway,
    check_internet,
    check_dns,
    check_https,
    check_http,
    check_latency,
    check_traceroute
)


from netdiag.reporters import (
    print_results,
    print_diagnoses,
    print_json
)


from netdiag.diagnostics import diagnose
from netdiag.cli import create_parser
from netdiag.history import History
from netdiag.monitor import monitor


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    checks = {
        "gateway": check_gateway,
        "internet": check_internet,
        "dns": check_dns,
        "https": check_https,
        "http": check_http,
        "latency": check_latency,
        "traceroute": check_traceroute
    }


    if args.history:
        history = History()

        runs = history.get_runs()

        print("Recent Diagnostic Runs")
        print()

        for run_id, timestamp, run_type in runs:
            print(f"  Type: {run_type.upper()}")

            checks = history.get_run_checks(run_id)

            if checks:
                print("  Checks:")

                for name, success, message, duration in checks:
                    status = "✓" if success else "✗"

                    print(f"    {status} {name} — {message} ({duration:.3f}s)")

                print()

            diagnoses = history.get_run_diagnoses(run_id)

            for problem, severity, cause in diagnoses:
                print(f"  Status: {severity}")
                print(f"  Problem: {problem}")
                print(f"  Cause: {cause}")
                print()

        history.close()
        exit()

    if args.stats:
        history = History()

        statistics = history.get_check_statistics()

        print("Historical Network Statistics")
        print()

        for name, data in statistics.items():
            print(name)
            print(f"  Runs: {data['runs']}")
            print(f"  Success Rate: {data['success_rate'] * 100:.1f}%")
            print(f"  Average Duration: {data['average_duration']:.3f}s")
            print()

        history.close()
        exit()




    if args.monitor:
        history = History()
        monitor(
            [
                check_gateway,
                check_internet,
                check_dns
            ],
            history,
            args.interval
        )
        history.close()
        exit()


    if args.check:
        results = [checks[args.check]()]
    else:
        results = [
            check_gateway(),
            check_internet(),
            check_dns(),
            check_https(),
            check_http(),
            check_latency(),
            check_traceroute()
        ]

    diagnoses = diagnose(results)

    history = History()

    run_id = history.create_run(
        datetime.now().isoformat(),
        "check" if args.check else "full"
    )

    for result in results:
        history.add_check(run_id, result)

    for diagnosis in diagnoses:
        history.add_diagnosis(run_id, diagnosis)

    history.close()

    if args.json:
        print_json(results, diagnoses)
    else:
        print_results(results)
        print_diagnoses(diagnoses)