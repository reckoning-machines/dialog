# Dialog — the local research desk

Dialog is a local research and paper-trading desk. Python runs the application, ARH governs research, and LangGraph coordinates the work.

This is a working, finite **Historical Reconstruction**, with generated data, deterministic researchers, independent checking, two scheduled research cycles and a shared paper portfolio. No paid provider, broker, real capital, IRIS or remote deployment. Synthetic strategy results demonstrate behavior, not investment merit.

## Open the desk

The local workspace is **http://127.0.0.1:8787/**. Run from this checkout:

```sh
.venv/bin/python run.py --data .local/dialog --port 8787
```

For a new installation, use Python 3.12, `python3.12 -m venv .venv`, then `.venv/bin/python -m pip install -r requirements.lock` and `.venv/bin/python scripts/install_arh_client.py`. ARH must be checked out at the exact commit in [arh-dependency.json](arh-dependency.json). Set `DIALOG_ARH_ROOT` if its path differs from `/Users/jedgore/dev/speedway`. Startup refuses a different commit, tracked changes, or nonmatching public client source. The running app has its own environment in `.venv`; it does not depend on temporary development environments.

`Run two cycles` executes through step 15. `Next step` lets you inspect each boundary. The deliberate lost order response and simultaneous research-worker deaths recover under the mandate. `Advance to scheduled exits` executes steps 16–17, including opening-authority expiry and final sales. `Pause new work` leaves existing settlement, reconciliation and required exits authorized. This demo's clock advances through declared historical slots; it is not a real-time market scheduler. A slot advances only through the coordinator; no third research cycle is authorized.

At cycle 2 close, inspect **198 AAA**, **$80,140.40 cash**, **$99,940.40 NAV**, and **$59.60 fees**. T1 is retired; R1 is rejected; T2 and R2 hold 99 shares each. Final required exits leave **$99,920.60 cash**, no holdings, and **$79.40 total fees**. Constant $100 marks make all paper P&L execution costs.

Evidence links expose dossier criteria, original ARH references and order receipts. The two approach cards retain the failed reversal and its revised quiet-regime question. Correct arithmetic alone does not admit a strategy. Research-unit bars and paper dollars have separate scales. Relationship arrows have fixed widths and express recorded relationships, not quantitative conservation.

## Implementation and authority

The owner's implementation direction authorizes the documented bounded synthetic mandate Z-M1, DA-1 standing policies, portfolio mechanics and local browser. It supersedes the earlier docs-only/domain-build prohibition for this demonstration. It does not approve production, real investments, arbitrary scope changes or a new ARH constitution.

Python owns application behavior. LangGraph 1.2.19 coordinates the research branches and resumable desk; the unchanged [14-witness gate](validation/v01_integrated_m1/REPORT.md) passed against merged ARH `76234ff1816d95432a87de69b3337db5401349d4`. ARH retains authoritative research budgets, evidence, checks, P-1 decisions and Apply records. Dialog owns strategy dossiers/admission, allocation, paper orders, fills, exits and portfolio cash. Domain facts cite ARH records and never reinterpret an ARH Check as investment approval.

The app is a trusted local service. The loopback browser offers only finite actions, expected-revision checks and same-origin mutation controls. Research and Checker subprocesses load actor-specific credentials. The coordinator/bootstrap service holds a broad Principal credential. This is cooperative separation, **not OS isolation or narrow credential enforcement**. Bootstrap may establish the exact controls; routine hypothesis admission uses public `policy-decide` and `apply`, not discretionary owner decisions. No private imports, direct ARH storage reads or copied governance validator.

All durable app files live under the selected `--data` directory: domain journal, governance request journal, LangGraph checkpoints, adapter receipts and private local host state. Own journals never open ARH databases. Stable public request keys recover original outcomes. The domain journal is authoritative for book transitions; LangGraph is orchestration state. Public ARH projections include their closure/as-of values; display reads do not claim an atomic cross-ledger snapshot. Reopening the same directory restores the same desk. A process lock refuses two coordinators. Do not reuse or publish private connection files.

The [execution adapter protocol](src/dialog/execution.py) requires stable order IDs, query-by-ID, cumulative receipts, cancellation and explicit partial fills. The current durable fixture adapter implements the declared $100 price and $0.10/share fee model. It is not a commodity backtesting engine. No external vendor was selected without evidence. This first slice allocates a batch only from a flat, reconciled book; nonzero exposure or outstanding orders refuse another batch. It demonstrates competing strategies in one batch, not a general rebalancer.

Five-minute virtual marks are generated from the declared fixture and recorded as such. Fixed holding deadlines remain separate from research expiry. Exits retain their original cost envelope, reconcile/cancel buys first, cannot oversell, and may exceed ordinary turnover only under the bounded exit policy. Stale marks refuse; current fixed fixture marks are not fresh market observations.

Research grants are 10.00 per cycle with unchanged 10.00 lineage ceilings; separate checking is 2.00 per cycle plus up to 8.00 startup checking. Actual complete-run charges are **8.75 units**: setup 2.75, cycle research 1.75 + 2.25, and independent cycle checking 1.00 + 1.00. Four 0.25 hypothesis funding allowances remain separately reserved (1.00 total), not spent again. Prior failures, validation runs and new demo instances have separate accounts. The startup cost differs from the paper example because actual ARH registrations require eleven independent 0.25 checks; it remains within its documented 8.00 envelope.

## Verify and inspect

```sh
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
.venv/bin/python validation/v01_integrated_m1/audit_retained.py
```

Tests create disposable local hosts and virtual synthetic accounts. They exercise ten book/evidence contract cases and one full fresh-process continuity test, including actual SIGKILL and core-host reopening. Evidence, screenshots, repair history and source hashes are in [the implementation record](validation/dialog/REPORT.md). The installed environment and source manifest identify the tested bytes. Old failed consumer runs and B-02 are preserved.

The finite demo does not infer unknown scope, grant extra budget, choose new instruments, or continue after the second scheduled research cycle. There are no general-purpose strategy editing, authority issuance, live quotes or production security controls. RV-02 remains open as an ARH client-helper usability finding; its supported public lower-level Checker route is used.

RV-04: direct VCS wheel installation was observed to package stale tracked `client/build/lib` modules. The explicit installer exports only the unchanged public package and its metadata from the exact Git pin into a clean temporary directory, installs it, then compares every module hash. ARH is not modified. This packaging deficiency remains an upstream finding; do not substitute the known-bad cached wheel.
