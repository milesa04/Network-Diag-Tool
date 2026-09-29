from netdiag.models import CheckResult
from netdiag.diagnostics import diagnose


def test_healthy_network():

    
    results = [
        CheckResult(
            name="Default Gateway",
            success=True,
            message="Gateway reachable",
            duration=0.01
        ),
        CheckResult(
            name="Internet Connectivity",
            success=True,
            message="Internet reachable",
            duration=0.01
        ),
        CheckResult(
            name="DNS Resolution",
            success=True,
            message="DNS working",
            duration=0.01
        ),
        CheckResult(
            name="HTTPS Connectivity",
            success=True,
            message="TLS working",
            duration=0.01
        ),
        CheckResult(
            name="HTTPS Request",
            success=True,
            message="HTTP 200",
            duration=0.01
        )
    ]

    diagnoses = diagnose(results)

    assert len(diagnoses) == 1
    assert diagnoses[0].problem == "NO_PROBLEMS_DETECTED"
    assert diagnoses[0].severity == "HEALTHY"


def test_dns_failure():
    results = [
        CheckResult(
            name="Default Gateway",
            success=True,
            message="Gateway reachable",
            duration=0.01
        ),
        CheckResult(
            name="Internet Connectivity",
            success=True,
            message="Internet reachable",
            duration=0.01
        ),
        CheckResult(
            name="DNS Resolution",
            success=False,
            message="DNS server did not respond",
            duration=0.01
        ),
        CheckResult(
            name="HTTPS Connectivity",
            success=False,
            message="TLS connection failed",
            duration=0.01
        ),
        CheckResult(
            name="HTTPS Request",
            success=False,
            message="Request failed",
            duration=0.01
        )
    ]

    diagnoses = diagnose(results)

    assert len(diagnoses) == 1
    assert diagnoses[0].problem == "DNS_FAILURE"
    assert diagnoses[0].severity == "DEGRADED"


def test_gateway_failure():
    results = [
        CheckResult(
            name="Default Gateway",
            success=False,
            message="Gateway unreachable",
            duration=0.01
        ),
        CheckResult(
            name="Internet Connectivity",
            success=False,
            message="Internet unreachable",
            duration=0.01
        ),
        CheckResult(
            name="DNS Resolution",
            success=False,
            message="DNS failed",
            duration=0.01
        ),
        CheckResult(
            name="HTTPS Connectivity",
            success=False,
            message="TLS failed",
            duration=0.01
        ),
        CheckResult(
            name="HTTPS Request",
            success=False,
            message="Request failed",
            duration=0.01
        )
    ]

    diagnoses = diagnose(results)

    assert any(
        diagnosis.problem == "GATEWAY_FAILURE"
        for diagnosis in diagnoses
    )


def test_tls_failure():
    results = [
        CheckResult(
            name="Default Gateway",
            success=True,
            message="Gateway reachable",
            duration=0.01
        ),
        CheckResult(
            name="Internet Connectivity",
            success=True,
            message="Internet reachable",
            duration=0.01
        ),
        CheckResult(
            name="DNS Resolution",
            success=True,
            message="DNS working",
            duration=0.01
        ),
        CheckResult(
            name="HTTPS Connectivity",
            success=False,
            message="TLS connection failed",
            duration=0.01
        ),
        CheckResult(
            name="HTTPS Request",
            success=False,
            message="Request failed",
            duration=0.01
        )
    ]

    diagnoses = diagnose(results)

    assert any(
        diagnosis.problem == "HTTPS_CONNECTIVITY_FAILURE"
        for diagnosis in diagnoses
    )


def test_https_request_failure():
    results = [
        CheckResult(
            name="Default Gateway",
            success=True,
            message="Gateway reachable",
            duration=0.01
        ),
        CheckResult(
            name="Internet Connectivity",
            success=True,
            message="Internet reachable",
            duration=0.01
        ),
        CheckResult(
            name="DNS Resolution",
            success=True,
            message="DNS working",
            duration=0.01
        ),
        CheckResult(
            name="HTTPS Connectivity",
            success=True,
            message="TLS working",
            duration=0.01
        ),
        CheckResult(
            name="HTTPS Request",
            success=False,
            message="HTTP 404",
            duration=0.01
        )
    ]

    diagnoses = diagnose(results)

    assert len(diagnoses) == 1
    assert diagnoses[0].problem == "HTTPS_REQUEST_FAILURE"
    assert diagnoses[0].severity == "DEGRADED"


def test_dns_only():
    results = [
        CheckResult(
            name="DNS Resolution",
            success=True,
            message="DNS working",
            duration=0.01
        )
    ]

    diagnoses = diagnose(results)

    assert len(diagnoses) == 1
    assert diagnoses[0].problem == "NO_PROBLEMS_DETECTED"


def test_latency_only():
    results = [
        CheckResult(
            name="Latency",
            success=True,
            message="Average latency: 15.00 ms, Packet loss: 0%",
            duration=3.0
        )
    ]

    diagnoses = diagnose(results)

    assert len(diagnoses) == 1
    assert diagnoses[0].problem == "NO_PROBLEMS_DETECTED"