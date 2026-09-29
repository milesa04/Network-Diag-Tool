############################ Network Checks ############################
#
#      Provides the core network diagnostic checks for the tool.
#

import socket
import urllib.request
import time
import subprocess
import ssl
import dns.resolver

from netdiag.models import CheckResult


def get_default_gateway():
    try:
        result = subprocess.run(
            ["route", "-n", "get", "default"],
            capture_output=True,
            text=True,
            check=True
        )

        for line in result.stdout.splitlines():
            if "gateway:" in line:
                return line.split()[1]

        return None

    except subprocess.CalledProcessError:
        return None


def check_gateway():

    start_time = time.perf_counter()

    gateway = get_default_gateway()

    if gateway is None:
        duration = time.perf_counter() - start_time

        return CheckResult(
            name="Default Gateway",
            success=False,
            message="Could not determine default gateway",
            duration=duration
        )

    try:
        subprocess.run(
            ["ping", "-c", "1", "-W", "1000", gateway],
            capture_output=True,
            text=True,
            check=True
        )

        duration = time.perf_counter() - start_time

        return CheckResult(
            name="Default Gateway",
            success=True,
            message=f"Gateway {gateway} is reachable",
            duration=duration
        )

    except subprocess.CalledProcessError:
        duration = time.perf_counter() - start_time

        return CheckResult(
            name="Default Gateway",
            success=False,
            message=f"Gateway {gateway} is unreachable",
            duration=duration
        )


def check_internet():
    start_time = time.perf_counter()

    try:
        connection = socket.create_connection(
            ("www.google.com", 443),
            timeout=3
        )
        connection.close()

        duration = time.perf_counter() - start_time

        return CheckResult(
            name="Internet Connectivity",
            success=True,
            message="External HTTPS server is reachable",
            duration=duration
        )

    except OSError as error:
        duration = time.perf_counter() - start_time

        return CheckResult(
            name="Internet Connectivity",
            success=False,
            message=str(error),
            duration=duration
        )


def check_dns():
    start_time = time.perf_counter()

    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ["8.8.8.8"]

        answers = resolver.resolve(
            "google.com",
            "A",
            lifetime=3
        )

        ip_address = answers[0].address

        duration = time.perf_counter() - start_time

        return CheckResult(
            name="DNS Resolution",
            success=True,
            message=f"google.com resolves to {ip_address} using DNS server 8.8.8.8",
            duration=duration
        )

    except dns.resolver.NXDOMAIN:
        duration = time.perf_counter() - start_time

        return CheckResult(
            name="DNS Resolution",
            success=False,
            message="Domain does not exist (NXDOMAIN)",
            duration=duration
        )

    except dns.resolver.NoAnswer:
        duration = time.perf_counter() - start_time

        return CheckResult(
            name="DNS Resolution",
            success=False,
            message="DNS server responded, but provided no answer",
            duration=duration
        )

    except dns.resolver.LifetimeTimeout:
        duration = time.perf_counter() - start_time

        return CheckResult(
            name="DNS Resolution",
            success=False,
            message="DNS server did not respond within 3 seconds",
            duration=duration
        )

    except dns.resolver.NoNameservers:
        duration = time.perf_counter() - start_time

        return CheckResult(
            name="DNS Resolution",
            success=False,
            message="No usable DNS nameservers were available",
            duration=duration
        )

    except Exception as error:
        duration = time.perf_counter() - start_time

        return CheckResult(
            name="DNS Resolution",
            success=False,
            message=f"Unexpected DNS error: {error}",
            duration=duration
        )


def check_https():
    start_time = time.perf_counter()

    try:
        context = ssl.create_default_context()

        with socket.create_connection(
            ("www.google.com", 443),
            timeout=3
        ) as connection:

            with context.wrap_socket(
                connection,
                server_hostname="www.google.com"
            ) as secure_connection:

                cipher = secure_connection.cipher()

        duration = time.perf_counter() - start_time

        return CheckResult(
            name="HTTPS Connectivity",
            success=True,
            message=f"TLS connection established using {cipher[0]}",
            duration=duration
        )

    except (OSError, ssl.SSLError) as error:
        duration = time.perf_counter() - start_time

        return CheckResult(
            name="HTTPS Connectivity",
            success=False,
            message=str(error),
            duration=duration
        )


def check_http():
    start_time = time.perf_counter()

    try:
        response = urllib.request.urlopen(
            "https://www.google.com",
            timeout=5
     )

        duration = time.perf_counter() - start_time

        return CheckResult(
            name="HTTPS Request",
            success=True,
            message=f"HTTP status code: {response.status}",
            duration=duration
        )

    except Exception as error:
        duration = time.perf_counter() - start_time

        return CheckResult(
            name="HTTPS Request",
            success=False,
            message=str(error),
            duration=duration
        )


def check_latency():
    start_time = time.perf_counter()

    try:
        result = subprocess.run(
            ["ping", "-c", "4", "-W", "1000", "8.8.8.8"],
            capture_output=True,
            text=True,
            check=True
        )

        duration = time.perf_counter() - start_time

        lines = result.stdout.splitlines()

        latency_values = []

        for line in lines:
            if "time=" in line:
                time_value = line.split("time=")[1].split()[0]
                latency_values.append(float(time_value))

        if not latency_values:
            return CheckResult(
                name="Latency",
                success=False,
                message="No latency measurements were received",
                duration=duration
            )

        average_latency = sum(latency_values) / len(latency_values)

        packet_loss = 100 - (len(latency_values) / 4 * 100)

        return CheckResult(
            name="Latency",
            success=True,
            message=(
                f"Average latency: {average_latency:.2f} ms, "
                f"Packet loss: {packet_loss:.0f}%"
            ),
            duration=duration
        )

    except subprocess.CalledProcessError:
        duration = time.perf_counter() - start_time

        return CheckResult(
            name="Latency",
            success=False,
            message="Ping failed",
            duration=duration
        )

def check_traceroute():
    start_time = time.perf_counter()

    try:
        result = subprocess.run(
            ["traceroute", "-m", "8", "8.8.8.8"],
            capture_output=True,
            text=True,
            check=True
        )

        duration = time.perf_counter() - start_time

        lines = result.stdout.splitlines()

        hops = []
        current_hop = None
        unresponsive_hops = []

        for line in lines:
            line = line.strip()

            if not line or line.startswith("traceroute"):
                continue

            parts = line.split()

            if parts[0].isdigit():
                current_hop = parts[0]

                addresses = []

                for part in parts[1:]:
                    if "(" in part and ")" in part:
                        address = part.strip("()")
                        addresses.append(address)

                if addresses:
                    hops.append(
                        f"Hop {current_hop}: {', '.join(addresses)}"
                    )
                else:
                    hops.append(
                        f"Hop {current_hop}: No response"
                    )
                    unresponsive_hops.append(int(current_hop))

            elif current_hop is not None:
                addresses = []

                for part in parts:
                    if "(" in part and ")" in part:
                        address = part.strip("()")
                        addresses.append(address)

                if addresses:
                    hops[-1] += f", {', '.join(addresses)}"

        if not hops:
            return CheckResult(
                name="Traceroute",
                success=False,
                message="No traceroute hops were detected",
                duration=duration,
                details={
                    "hop_count": 0,
                    "unresponsive_hops": [],
                    "destination_reached": False
                }
            )

        destination_reached = not (
            hops[-1].endswith("No response")
        )

        return CheckResult(
            name="Traceroute",
            success=True,
            message=" | ".join(hops),
            duration=duration,
            details={
                "hop_count": len(hops),
                "unresponsive_hops": unresponsive_hops,
                "destination_reached": destination_reached
            }
        )

    except subprocess.CalledProcessError:
        duration = time.perf_counter() - start_time

        return CheckResult(
            name="Traceroute",
            success=False,
            message="Traceroute failed",
            duration=duration,
            details={
                "hop_count": 0,
                "unresponsive_hops": [],
                "destination_reached": False
            }
        )



    