# Development guide

## Setup

Requires Python 3.12 or newer and Git.

```sh
python3.12 scripts/setup_local.py
.venv/bin/python run.py
```

Setup creates `.venv`, installs the locked Python dependencies, and downloads the pinned ARH dependency into `.local/dependencies/arh`. It installs the public client from clean source and verifies its module hashes. No separate ARH checkout or environment configuration is needed.

The server binds to loopback at `http://127.0.0.1:8787/`. State lives in `.local/dialog` and survives restarts. Both directories are ignored by Git. A second coordinator for the same desk is refused. Use `--port` and `--data` to run a separate synthetic desk.

## Exercise the workflow

Run both research cycles automatically or advance one step at a time. The fixed example includes competing hypotheses, an independent check, a rejected strategy, revised investigations, shared allocation, partial fills, a lost response, and interrupted researchers. Evidence can be inspected from the workspace.

At the second cycle's close, the portfolio holds 198 AAA, with $80,140.40 cash, $99,940.40 NAV and $59.60 fees. Advancing to the scheduled exits leaves no positions, $99,920.60 cash and $79.40 total fees. Research costs are separate: 8.75 simulated units for setup and both cycles, plus 1.00 retained hypothesis-funding allowance.

The clock advances through declared historical slots. Research deadlines do not close positions; holding deadlines and exit authority govern those. The two-cycle mandate ends after the scheduled work. No third cycle is authorized.

## Architecture

ARH owns research authorizations, budgets, evidence, independent checks and acceptance records. Dialog owns strategy admission, allocation, orders, fills, portfolio accounts and exits. LangGraph coordinates execution and resumes work; it grants no authority.

The application uses the public ARH client and records authoritative references. It never reads ARH ledgers directly. Public projections carry their observed closure and time. Dialog's journal and execution-adapter receipts reconstruct portfolio state; graph checkpoints do not authorize trades.

Researchers and the evaluator run in separate processes with role credentials. The trusted local coordinator holds a broad Principal credential. This is cooperative role separation, not operating-system isolation. The browser exposes finite actions with revision and origin checks, not arbitrary Principal commands.

The execution adapter is a deterministic fixture with a $100 price and $0.10-per-share fee. Its replaceable protocol supports stable order IDs, lookup, partial fills and cancellation. Allocation opens competing strategies from a flat, reconciled book; general rebalancing is outside this version. Exits retain their original cost limits and cannot oversell.

## Tests

```sh
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
.venv/bin/python validation/app/audit.py
```

Tests use disposable local hosts and synthetic accounts. They cover ten portfolio/evidence cases and a complete continuity run with real process termination and core reopening. See [validation results](validation/app/REPORT.md).

RV-02 remains an ARH convenience-helper usability finding. RV-04 records stale generated files in ARH's direct VCS wheel build; setup avoids those build outputs and verifies the unchanged public client source. These procedures do not modify ARH.

This version has no paid providers, live data, brokers, real capital, IRIS integration or public deployment. It demonstrates application and recovery behavior, not investment performance.
