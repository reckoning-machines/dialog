# RV-03-C1 reproduction and evidence

Pin `dependency-pin.json` exactly; use `../../evidence/v01-rv03-c1-20261102/dependencies.lock`. The installed public client remains byte-identical to the repaired checkout; the repair changes core validation only. No private import or ARH ledger access is used by the consumer.

Prepare a fresh disposable root with this directory copied to `source/`, plus `runtime/` and `evidence/`. Copy the dependency lock into `evidence/`. The observed root is `/private/tmp/murmur-rv03-h694t7nc`; the interpreter is `/private/tmp/murmur-v01.1dUJI5/venv/bin/python`; the exact ARH checkout is `/Users/jedgore/dev/speedway`. Local-host socket permission is required. Never restore old credentials or overwrite historical evidence.

Run the modes sequentially: `orchestrate.py contention`, `parallel-success`, `parallel-blocked`, `cs`, `policy-edges`; then `boundary_test.py`; then `orchestrate.py reopen`. The runner uses only the documented host CLI and exported client. Each family has its own initial pools; repeated runs retain additional spending separately. `evidence/commands.json` records exact commands, outcomes and elapsed times.

After all families: `reconcile_runs.py` (fresh public-host reopening and exports), `verify_evidence.py` (all 14 mandatory outcomes), `finish_evidence.py export` (accounts, pins, B-02 integrity). Finish the report, then `finish_evidence.py finalize` (secret scan, credential removal, manifests) and `audit_retained.py` (structural token scan and hash verification). Retained consumer checkpoints are consumer-owned; ARH ledgers are not exported or inspected.

`bootstrap_probe.py`, `lifecycle.py`, `service_tests.py`, and `retain.py` are inherited unused diagnostic helpers. No run invokes them. The final report does not replace the retained source-at-start snapshots. Old B-02, ccf31b4 and RV-01-A1 results remain unchanged.
