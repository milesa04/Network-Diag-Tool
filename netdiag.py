############################ Main Execution ############################
#
#     This is the main entry point for the network diagnostic tool. 
#     It runs a series of checks and outputs the results.
#


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

    if args.json:
        print_json(results, diagnoses)
    else:
        print_results(results)
        print_diagnoses(diagnoses)