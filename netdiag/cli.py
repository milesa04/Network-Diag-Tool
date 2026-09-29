################## Command Line Parser #####################
#
#     Provides a command line interface for the network diagnostic tool.
#

import argparse


def create_parser():
    parser = argparse.ArgumentParser(
        description="Network diagnostic and troubleshooting tool",
        epilog=(
            "Examples:\n"
            "  python3 netdiag.py\n"
            "  python3 netdiag.py --check traceroute\n"
            "  python3 netdiag.py --monitor --interval 30\n"
            "  python3 netdiag.py --history\n"
            "  python3 netdiag.py --stats\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    mode_group = parser.add_mutually_exclusive_group()

    mode_group.add_argument(
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
        help="Run one specific diagnostic instead of the full diagnostic"
    )

    mode_group.add_argument(
        "--history",
        action="store_true",
        help="Show recent diagnostic runs and their results"
    )

    mode_group.add_argument(
        "--stats",
        action="store_true",
        help="Show historical success rates and average check durations"
    )

    mode_group.add_argument(
        "--monitor",
        action="store_true",
        help="Continuously monitor gateway, internet, and DNS health"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output diagnostic results in JSON format"
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=30,
        help="Seconds between monitoring checks (default: 30)"
    )

    return parser

