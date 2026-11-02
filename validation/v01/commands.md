# Commands and process perimeter

Authorized baseline:58aad1a4e17e37b574e08a10a86e6e8c77ead27d.
ARH checkout:/Users/jedgore/dev/speedway at93436406c8a1fd2c06e5713b1def09d90104db54.
Interpreter:/private/tmp/murmur-v01.1dUJI5/venv/bin/python.

1. Create isolated venv; copy client source to scratch; pip install client plus langgraph==1.2.19 and langgraph-checkpoint-sqlite==3.1.3. Record pip freeze --all before host execution.
2. consumer/profile.py <external-profile-directory> writes inspectable setup JSON.
3. PYTHONDONTWRITEBYTECODE=1 python -m adaptive_research_harness.local_host --setup <external-profile-directory> --run <disposable-run>, working directory ARH checkout. Public CLI only.
4. bootstrap_probe.py <probe-run> <evidence/bootstrap> captures helper/tariff limitation.
5. startup.py <profile-check-run> <evidence/profile-check> checks real setup; repair own document metadata and resume existing BOOT-1; stop on independent FAIL.
6. service_tests.py <profile-check-run> <evidence/service-from-repository>, working directory Murmuration, launches separate service and TC using runtime-only credentials.
7. lifecycle.py <run> <evidence/before-reopen> stop; confirm host termination; repeat step3 for same run; lifecycle.py <run> <evidence/after-reopen> stop.
8. retain.py exports inventory, exact package pins, public parity and secret-free evidence; final evidence manifest verifies all retained source/data.
9. Delete only runtime credential files after secret scan and host termination. Retain exported public history, source, pins and evidence; do not read/export private ledgers as authority.

No token is supplied in a command argument or log. Paths above are correlation metadata, not credentials. Initial sandbox network/local-socket/archive failures were rerun with required permission. Core/service and BC/TC process evidence is retained.
