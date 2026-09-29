### Run an Individual Check

Run a specific diagnostic with `--check`:

```bash
python3 netdiag.py --check dns
```

Available checks:

```text
gateway
internet
dns
https
http
latency
traceroute
```

For example:

```bash
python3 netdiag.py --check traceroute
```

### Monitor Network Health

Continuously monitor the default gateway, internet connectivity, and DNS:

```bash
python3 netdiag.py --monitor
```

The default monitoring interval is 30 seconds.

A custom interval can be specified:

```bash
python3 netdiag.py --monitor --interval 5
```

Press `Ctrl+C` to stop monitoring.

### View Diagnostic History

View recent diagnostic runs:

```bash
python3 netdiag.py --history
```

History includes the run type, individual check results, and any diagnoses generated during the run.

### View Historical Statistics

View success rates and average check durations from recent monitoring runs:

```bash
python3 netdiag.py --stats
```

### JSON Output

Run diagnostics and return machine-readable JSON:

```bash
python3 netdiag.py --json
```

JSON output includes:

- Check names
- Success/failure status
- Messages
- Execution duration
- Detailed check data
- Diagnoses
- Recommendations

JSON can also be combined with an individual check:

```bash
python3 netdiag.py --check dns --json
```

### Command-Line Help

View all available options:

```bash
python3 netdiag.py --help
```

## Architecture

Network-Diag-Tool is organized into separate modules for network checks, diagnosis, persistence, reporting, monitoring, and command-line argument handling.

```text
                         ┌─────────────────────┐
                         │     CLI / Runner    │
                         │     netdiag.py      │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
             ┌────────────┐  ┌──────────────┐  ┌────────────┐
             │   Checks   │  │   Diagnosis  │  │  Monitor   │
             │  checks.py │  │diagnostics.py│  │monitor.py  │
             └──────┬─────┘  └──────┬───────┘  └─────┬──────┘
                    │               │                │
                    └───────────────┼────────────────┘
                                    ▼
                           ┌────────────────┐
                           │    History     │
                           │   history.py   │
                           │    SQLite      │
                           └───────┬────────┘
                                   │
                                   ▼
                           ┌────────────────┐
                           │   Reporting    │
                           │  reporters.py  │
                           └────────────────┘
```

### Core Components

**`checks.py`**

Contains the individual network diagnostics. Each check returns a structured `CheckResult` containing its name, success status, message, execution duration, and optional details.

**`diagnostics.py`**

Contains the diagnosis engine. It evaluates the results from multiple checks and determines whether a known network problem can be identified. Diagnoses include a problem identifier, severity, cause, and recommendations.

**`history.py`**

Provides SQLite-backed persistence for diagnostic runs, check results, and diagnoses. Runs are categorized as `full`, `check`, or `monitor`, allowing historical monitoring statistics to be separated from one-off diagnostics.

**`monitor.py`**

Provides continuous network monitoring using a lightweight subset of the available checks. Each monitoring cycle is stored in the history database.

**`reporters.py`**

Handles human-readable and JSON output formats.

**`cli.py`**

Defines and validates command-line arguments using Python's `argparse` module.

**`models.py`**

Defines the structured data models used throughout the application, including `CheckResult` and `Diagnosis`.

### Data Flow

A typical diagnostic run follows this process:

1. The CLI determines which checks should run.
2. Individual checks execute and return `CheckResult` objects.
3. Results are passed to the diagnosis engine.
4. The diagnosis engine identifies any known problems.
5. The run, checks, and diagnoses are stored in SQLite.
6. The reporter displays the results in either human-readable or JSON format.