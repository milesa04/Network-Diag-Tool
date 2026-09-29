import argparse


def create_parser():
    parser = argparse.ArgumentParser(
        description="Network diagnostic and troubleshooting tool"
    )

    parser.add_argument(
        "--check",
        choices=[
            "gateway",
            "internet",
            "dns",
            "https",
            "http",
            "latency",
            "traceroute"
        ],
        help="Run a specific network diagnostic"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )

    parser.add_argument(
    "--history",
    action="store_true",
    help="Show recent diagnostic history"
    )


    parser.add_argument(
    "--monitor",
    action="store_true",
    help="Continuously monitor network health"
    )

    parser.add_argument(
    "--interval",
    type=int,
    default=30,
    help="Monitoring interval in seconds (default: 30)"
    )

    return parser