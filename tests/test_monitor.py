from netdiag.models import CheckResult
from netdiag.monitor import monitor


def test_monitor_runs_check(monkeypatch, capsys):
    calls = []
    saved_checks = []
    saved_diagnoses = []

    def fake_check():
        calls.append(True)

        return CheckResult(
            name="Test Check",
            success=True,
            message="Network is healthy",
            duration=0.1
        )

    class FakeHistory:
        def create_run(self, timestamp):
            return 1

        def add_check(self, run_id, result):
            saved_checks.append((run_id, result))

        def add_diagnosis(self, run_id, diagnosis):
            saved_diagnoses.append((run_id, diagnosis))

    sleep_calls = []

    def fake_sleep(interval):
        sleep_calls.append(interval)

        if len(sleep_calls) == 1:
            raise KeyboardInterrupt

    monkeypatch.setattr("netdiag.monitor.time.sleep", fake_sleep)

    monitor([fake_check], FakeHistory(), interval=10)

    assert len(calls) == 1
    assert sleep_calls == [10]
    assert len(saved_checks) == 1
    assert len(saved_diagnoses) == 1

    output = capsys.readouterr().out

    assert "Starting network monitor..." in output
    assert "Interval: 10 seconds" in output
    assert "HEALTHY" in output
    assert "1/1 checks passed" in output
    assert "Monitoring stopped." in output