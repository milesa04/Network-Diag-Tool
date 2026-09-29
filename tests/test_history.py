from netdiag.history import History
from netdiag.models import CheckResult, Diagnosis



def test_history_creates_database(tmp_path):
    database_path = tmp_path / "test.db"

    history = History(str(database_path))

    assert database_path.exists()

    history.close()


def test_create_run(tmp_path):
    database_path = tmp_path / "test.db"

    history = History(str(database_path))

    run_id = history.create_run("2026-09-29T12:00:00", "full")

    assert run_id == 1

    history.close()


def test_add_check(tmp_path):
    database_path = tmp_path / "test.db"

    history = History(str(database_path))

    run_id = history.create_run("2026-09-29T12:00:00", "full")

    result = CheckResult(
        name="Traceroute",
        success=True,
        message="Hop 1: 192.168.4.1 | Hop 2: 8.8.8.8",
        duration=0.45,
        details={
            "hop_count": 2,
            "unresponsive_hops": [],
            "destination_reached": True
        }
    )

    history.add_check(run_id, result)

    cursor = history.connection.execute(
        "SELECT name, success, message, duration, details FROM checks"
    )

    row = cursor.fetchone()

    assert row[0] == "Traceroute"
    assert row[1] == 1
    assert row[2] == "Hop 1: 192.168.4.1 | Hop 2: 8.8.8.8"
    assert row[3] == 0.45
    assert '"hop_count": 2' in row[4]

    history.close()

def test_add_diagnosis(tmp_path):
    database_path = tmp_path / "test.db"

    history = History(str(database_path))

    run_id = history.create_run("2026-09-29T12:00:00", "full")

    diagnosis = Diagnosis(
        problem="DNS_FAILURE",
        severity="DEGRADED",
        cause="DNS resolution failed.",
        recommendations=[
            "Check configured DNS server",
            "Test an alternate DNS server"
        ]
    )

    history.add_diagnosis(run_id, diagnosis)

    cursor = history.connection.execute(
        "SELECT problem, severity, cause, recommendations FROM diagnoses"
    )

    row = cursor.fetchone()

    assert row[0] == "DNS_FAILURE"
    assert row[1] == "DEGRADED"
    assert row[2] == "DNS resolution failed."
    assert "Check configured DNS server" in row[3]

    history.close()


def test_get_runs(tmp_path):
    database_path = tmp_path / "test.db"

    history = History(str(database_path))

    first_run = history.create_run("2026-09-29T12:00:00", "full")
    second_run = history.create_run("2026-09-29T12:05:00", "full"   )

    runs = history.get_runs()

    assert runs == [
        (second_run, "2026-09-29T12:05:00", "full"),
        (first_run, "2026-09-29T12:00:00", "full")
    ]

    history.close()


def test_get_run_diagnoses(tmp_path):
    database_path = tmp_path / "test.db"

    history = History(str(database_path))

    run_id = history.create_run("2026-09-29T12:00:00", "full")

    diagnosis = Diagnosis(
        problem="NO_PROBLEMS_DETECTED",
        severity="HEALTHY",
        cause="No network problems detected.",
        recommendations=["No action required."]
    )

    history.add_diagnosis(run_id, diagnosis)

    diagnoses = history.get_run_diagnoses(run_id)

    assert diagnoses == [
        (
            "NO_PROBLEMS_DETECTED",
            "HEALTHY",
            "No network problems detected."
        )
    ]

    history.close()



def test_get_run_checks():
    history = History(":memory:")

    run_id = history.create_run("2026-09-29T12:00:00", "full")

    result = CheckResult(
        name="Internet Connectivity",
        success=True,
        message="External HTTPS server is reachable",
        duration=0.25
    )

    history.add_check(run_id, result)

    checks = history.get_run_checks(run_id)

    assert len(checks) == 1
    assert checks[0][0] == "Internet Connectivity"
    assert checks[0][1] == 1
    assert checks[0][2] == "External HTTPS server is reachable"
    assert checks[0][3] == 0.25

    history.close()



def test_get_recent_checks():
    history = History(":memory:")

    run_id = history.create_run("2026-09-29T12:00:00", "monitor")

    history.add_check(
        run_id,
        CheckResult(
            name="Internet Connectivity",
            success=True,
            message="External HTTPS server is reachable",
            duration=0.25
        )
    )

    checks = history.get_recent_checks()

    assert len(checks) == 1
    assert checks[0][0] == run_id
    assert checks[0][1] == "2026-09-29T12:00:00"
    assert checks[0][2] == "Internet Connectivity"
    assert checks[0][3] == 1
    assert checks[0][4] == 0.25

    history.close()





def test_get_check_statistics():
    history = History(":memory:")

    run_id_1 = history.create_run("2026-09-29T12:00:00", "monitor")
    run_id_2 = history.create_run("2026-09-29T12:00:00", "monitor")

    history.add_check(
        run_id_1,
        CheckResult(
            name="Internet Connectivity",
            success=True,
            message="Reachable",
            duration=0.20
        )
    )

    history.add_check(
        run_id_2,
        CheckResult(
            name="Internet Connectivity",
            success=True,
            message="Reachable",
            duration=0.40
        )
    )

    statistics = history.get_check_statistics()

    assert statistics["Internet Connectivity"]["runs"] == 2
    assert statistics["Internet Connectivity"]["successes"] == 2
    assert statistics["Internet Connectivity"]["success_rate"] == 1.0
    assert statistics["Internet Connectivity"]["average_duration"] == 0.30

    history.close()

