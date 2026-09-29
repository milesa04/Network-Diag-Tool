# Network-Diag-Tool

A Python-based network diagnostics and monitoring tool that performs connectivity checks, identifies common network issues, tracks diagnostic history, and reports network health through a command-line interface.

## Overview

Network-Diag-Tool is a command-line network troubleshooting application built with Python.

The tool runs a series of network checks to evaluate connectivity from the local machine outward, including the default gateway, internet access, DNS resolution, HTTPS connectivity, HTTP requests, latency, and traceroute.

Results are collected as structured data and passed through a diagnosis layer that identifies common connectivity problems and provides recommended actions. Diagnostic runs are stored locally in SQLite, allowing users to review previous runs, continuously monitor network health, and analyze historical check performance.

The project was built to practice practical networking concepts, Python application design, command-line interfaces, database persistence, automated testing, and troubleshooting workflows.

## Features

### Network Diagnostics

- **Default Gateway** — Verifies that the local network gateway is reachable.
- **Internet Connectivity** — Tests external network connectivity.
- **DNS Resolution** — Resolves domains using a configured DNS server and reports resolution failures.
- **HTTPS Connectivity** — Establishes a TLS connection and reports the negotiated cipher.
- **HTTPS Request** — Performs an HTTPS request and reports the HTTP status code.
- **Latency** — Measures average network latency and packet loss.
- **Traceroute** — Traces the network path to an external destination and identifies unresponsive hops.

### Automatic Diagnosis

The diagnostic engine evaluates check results together to identify common network problems, including:

- Gateway failures
- Internet connectivity failures
- DNS failures
- HTTPS connectivity failures
- HTTPS request failures
- Traceroute destination failures

Each diagnosis includes a severity level, likely cause, and recommended actions.

### Monitoring

The built-in monitoring mode continuously checks:

- Default gateway
- Internet connectivity
- DNS resolution

Each monitoring cycle is stored in the local SQLite database and reports the current network health.

### Historical Analysis

Diagnostic history can be reviewed from the command line, including:

- Previous diagnostic runs
- Run type (`FULL`, `CHECK`, or `MONITOR`)
- Individual check results
- Diagnoses and recommendations
- Historical success rates
- Average check durations

### Output Formats

- Human-readable command-line output
- JSON output for programmatic use

## Usage

### Run Full Diagnostics

Run the complete network diagnostic suite:

```bash
python3 netdiag.py


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