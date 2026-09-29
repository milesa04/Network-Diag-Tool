############################# Diagnostics ############################
#
#     Provides the diagnostic logic for the network diagnostic tool.
#

from netdiag.models import Diagnosis


def diagnose(results):
    diagnoses = []

    internet = next(
        (result for result in results
         if result.name == "Internet Connectivity"),
        None
    )

    dns = next(
        (result for result in results
         if result.name == "DNS Resolution"),
        None
    )

    https = next(
        (result for result in results
         if result.name == "HTTPS Connectivity"),
        None
    )

    http = next(
        (result for result in results
         if result.name == "HTTPS Request"),
        None
    )

    gateway = next(
        (result for result in results
         if result.name == "Default Gateway"),
        None
    )

    traceroute = next(
    (result for result in results
     if result.name == "Traceroute"),
    None
    )

    if gateway is not None and not gateway.success:
        diagnoses.append(
            Diagnosis(
                problem="GATEWAY_FAILURE",
                severity="OFFLINE",
                cause="The default gateway could not be reached.",
                recommendations=[
                    "Check your Wi-Fi or Ethernet connection",
                    "Check your local network configuration",
                    "Restart your router or access point if necessary"
                ]
            )
        )

    if internet is not None and not internet.success:
        diagnoses.append(
            Diagnosis(
                problem="INTERNET_CONNECTIVITY_FAILURE",
                severity="OFFLINE",
                cause="External network connectivity could not be established.",
                recommendations=[
                    "Check your local network connection",
                    "Check your network gateway",
                    "Verify that Wi-Fi or Ethernet is connected"
                ]
            )
        )

    if (
        internet is not None
        and dns is not None
        and internet.success
        and not dns.success
    ):
        diagnoses.append(
            Diagnosis(
                problem="DNS_FAILURE",
                severity="DEGRADED",
                cause="Internet connectivity is working, but DNS resolution failed.",
                recommendations=[
                    "Check configured DNS server",
                    "Test an alternate DNS server",
                    "Check local network configuration"
                ]
            )
        )

    if (
        dns is not None
        and https is not None
        and dns.success
        and not https.success
    ):
        diagnoses.append(
            Diagnosis(
                problem="HTTPS_CONNECTIVITY_FAILURE",
                severity="DEGRADED",
                cause="DNS resolution is working, but the TLS connection could not be established.",
                recommendations=[
                    "Check firewall or network security settings",
                    "Check whether HTTPS traffic is being blocked or intercepted",
                    "Verify that the remote server supports TLS"
                ]
            )
        )

    if (
        https is not None
        and http is not None
        and https.success
        and not http.success
    ):
        diagnoses.append(
            Diagnosis(
                problem="HTTPS_REQUEST_FAILURE",
                severity="DEGRADED",
                cause="HTTPS connectivity is working, but the web request failed.",
                recommendations=[
                    "Check the remote server status",
                    "Check for HTTP or TLS errors",
                    "Try accessing another HTTPS website"
                ]
            )
        )

    if (
        traceroute is not None
        and traceroute.success
        and traceroute.details is not None
        and not traceroute.details["destination_reached"]
    ):
        diagnoses.append(
            Diagnosis(
                problem="TRACEROUTE_DESTINATION_FAILURE",
                severity="DEGRADED",
                cause="Traceroute completed, but the destination could not be reached.",
                recommendations=[
                    "Check connectivity to the remote network",
                    "Check firewall or routing configuration",
                    "Run traceroute again to determine whether the issue persists"
                ]
            )
        )

    if not diagnoses:
        diagnoses.append(
            Diagnosis(
                problem="NO_PROBLEMS_DETECTED",
                severity="HEALTHY",
                cause="All selected network diagnostics completed successfully.",
                recommendations=[
                    "No action required"
                ]
            )
        )

    return diagnoses




