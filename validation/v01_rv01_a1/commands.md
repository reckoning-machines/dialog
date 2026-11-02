# Reproduction layout and retained evidence

Use the exact pinned ARH checkout and an isolated interpreter satisfying `../../evidence/v01-rv01-a1-20261102/dependencies.lock`. The installed client was built from a byte-identical temporary copy, avoiding source/build mutations in ARH. Do not install over the source checkout or use a newer unreviewed dependency.

The consumer runner expects a disposable root with `source/`, `runtime/`, and `evidence/`. Copy this validation directory to that root's `source/`; copy the dependency lock to its `evidence/`. Create fresh runtime directories through the runner. Local-host socket permission is necessary. Paths to the pinned checkout/interpreter were `/Users/jedgore/dev/speedway` and `/private/tmp/murmur-v01.1dUJI5/venv/bin/python` in the observed run. New credentials are host-generated; never restore or fabricate old credentials.

Recorded commands, with the actual scratch source path:

```text
python /private/tmp/murmur-rv01.bV2lvE/source/profile.py /private/tmp/murmur-rv01.bV2lvE/source
python /private/tmp/murmur-rv01.bV2lvE/source/orchestrate.py contention
python /private/tmp/murmur-rv01.bV2lvE/source/orchestrate.py parallel-success
python /private/tmp/murmur-rv01.bV2lvE/source/orchestrate.py parallel-blocked
python /private/tmp/murmur-rv01.bV2lvE/source/orchestrate.py cs
python /private/tmp/murmur-rv01.bV2lvE/source/orchestrate.py policy-edges
python /private/tmp/murmur-rv01.bV2lvE/source/boundary_test.py
python /private/tmp/murmur-rv01.bV2lvE/source/orchestrate.py reopen
python /private/tmp/murmur-rv01.bV2lvE/source/reconcile_runs.py
python /private/tmp/murmur-rv01.bV2lvE/source/verify_evidence.py
python /private/tmp/murmur-rv01.bV2lvE/source/finish_evidence.py export
python /private/tmp/murmur-rv01.bV2lvE/source/finish_evidence.py finalize
```

These are the command forms used across successive repairs, not a claim of one uninterrupted shell session. Failure/repair logs and named runtime rows preserve the actual repeats. `orchestrate.py` invokes the documented host CLI (`python -m adaptive_research_harness.local_host --setup ... --run ...`) in the ARH checkout; it does not import core code. `reconcile_runs.py` is specialized to these observed run IDs for the one known pending receipt, not a general automated settlement policy.

`bootstrap_probe.py`, `lifecycle.py`, `service_tests.py`, and `retain.py` are inherited diagnostic helpers, not the successor suite entry points. Use `finish_evidence.py` for this successor. The retained finalized evidence is sufficient for inspection without executing anything. New execution would be a new set of disposable runs with separately retained costs; do not overwrite historical evidence or attempt to mutate the frozen B-02 package.
