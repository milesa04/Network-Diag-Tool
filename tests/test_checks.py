import dns.resolver
import ssl
import urllib.error
import subprocess

from netdiag.checks import (
    get_default_gateway,
    check_gateway,
    check_internet,
    check_dns,
    check_https,
    check_http,
    check_latency,
    check_traceroute
)


def test_get_default_gateway():
    gateway = get_default_gateway()

    assert gateway is not None
    assert isinstance(gateway, str)


def test_check_gateway():
    result = check_gateway()

    assert result.name == "Default Gateway"
    assert isinstance(result.success, bool)
    assert result.duration >= 0
    assert isinstance(result.message, str)


def test_check_internet():
    result = check_internet()

    assert result.name == "Internet Connectivity"
    assert isinstance(result.success, bool)
    assert result.duration >= 0
    assert isinstance(result.message, str)


def test_check_dns():
    result = check_dns()

    assert result.name == "DNS Resolution"
    assert isinstance(result.success, bool)
    assert result.duration >= 0
    assert isinstance(result.message, str)


def test_check_https():
    result = check_https()

    assert result.name == "HTTPS Connectivity"
    assert isinstance(result.success, bool)
    assert result.duration >= 0
    assert isinstance(result.message, str)


def test_check_http():
    result = check_http()

    assert result.name == "HTTPS Request"
    assert isinstance(result.success, bool)
    assert result.duration >= 0
    assert isinstance(result.message, str)


def test_check_dns_nxdomain(monkeypatch):
    def mock_resolve(*args, **kwargs):
        raise dns.resolver.NXDOMAIN

    monkeypatch.setattr(
        dns.resolver.Resolver,
        "resolve",
        mock_resolve
    )

    result = check_dns()

    assert result.name == "DNS Resolution"
    assert result.success is False
    assert "NXDOMAIN" in result.message


def test_check_dns_timeout(monkeypatch):
    def mock_resolve(*args, **kwargs):
        raise dns.resolver.LifetimeTimeout()

    monkeypatch.setattr(
        dns.resolver.Resolver,
        "resolve",
        mock_resolve
    )

    result = check_dns()

    assert result.name == "DNS Resolution"
    assert result.success is False
    assert "did not respond within 3 seconds" in result.message


def test_check_https_tls_failure(monkeypatch):
    def mock_wrap_socket(*args, **kwargs):
        raise ssl.SSLError("TLS handshake failed")

    monkeypatch.setattr(
        ssl.SSLContext,
        "wrap_socket",
        mock_wrap_socket
    )

    result = check_https()

    assert result.name == "HTTPS Connectivity"
    assert result.success is False
    assert "TLS handshake failed" in result.message


def test_check_http_failure(monkeypatch):
    def mock_urlopen(*args, **kwargs):
        raise urllib.error.HTTPError(
            url="https://www.google.com",
            code=404,
            msg="Not Found",
            hdrs=None,
            fp=None
        )

    monkeypatch.setattr(
        "urllib.request.urlopen",
        mock_urlopen
    )

    result = check_http()

    assert result.name == "HTTPS Request"
    assert result.success is False
    assert "HTTP Error 404" in result.message


def test_check_latency(monkeypatch):
    class MockResult:
        stdout = """
64 bytes from 8.8.8.8: icmp_seq=0 ttl=117 time=15.20 ms
64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=14.80 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=117 time=15.10 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=117 time=15.40 ms
"""

    def mock_run(*args, **kwargs):
        return MockResult()

    monkeypatch.setattr(
        "subprocess.run",
        mock_run
    )

    result = check_latency()

    assert result.name == "Latency"
    assert result.success is True
    assert "Packet loss: 0%" in result.message
    assert result.duration >= 0


def test_check_latency_packet_loss(monkeypatch):

    class MockResult:
        stdout = """
64 bytes from 8.8.8.8: icmp_seq=0 ttl=117 time=15.20 ms
64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=14.80 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=117 time=15.40 ms
"""

    def mock_run(*args, **kwargs):
        return MockResult()

    monkeypatch.setattr(
        "subprocess.run",
        mock_run
    )

    result = check_latency()

    assert result.name == "Latency"
    assert result.success is True
    assert "Packet loss: 25%" in result.message


def test_check_traceroute(monkeypatch):
    class MockResult:
        stdout = """
traceroute to 8.8.8.8 (8.8.8.8), 8 hops max, 40 byte packets
 1  192.168.4.1 (192.168.4.1)  5.000 ms  5.100 ms  5.200 ms
 2  100.69.184.1 (100.69.184.1)  8.000 ms  8.100 ms  8.200 ms
 3  100.64.253.43 (100.64.253.43)  10.000 ms  10.100 ms  10.200 ms
 4  100.64.253.43 (100.64.253.43)  10.000 ms  10.100 ms  10.200 ms
 5  100.64.253.34 (100.64.253.34)  12.000 ms  12.100 ms  12.200 ms
 6  170.250.254.37 (170.250.254.37)  14.000 ms  14.100 ms  14.200 ms
 7  66.103.15.142 (66.103.15.142)  15.000 ms  15.100 ms  15.200 ms
 8  192.178.109.89 (192.178.109.89)  16.000 ms  16.100 ms  16.200 ms
"""

    def mock_run(*args, **kwargs):
        return MockResult()

    monkeypatch.setattr(
        "subprocess.run",
        mock_run
    )

    result = check_traceroute()

    assert result.name == "Traceroute"
    assert result.success is True
    assert "Hop 1: 192.168.4.1" in result.message
    assert "Hop 8: 192.178.109.89" in result.message
    assert result.duration >= 0


def test_check_traceroute_failure(monkeypatch):
    def mock_run(*args, **kwargs):
        raise subprocess.CalledProcessError(
            returncode=1,
            cmd=["traceroute", "-m", "8", "8.8.8.8"]
        )

    monkeypatch.setattr(
        "subprocess.run",
        mock_run
    )

    result = check_traceroute()

    assert result.name == "Traceroute"
    assert result.success is False
    assert result.message == "Traceroute failed"

