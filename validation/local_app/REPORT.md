# Z-L1 — working local ZUGOT, 2026-11-03

The authorized synthetic application runs at `http://127.0.0.1:8787/`. [Launch and operating guide](../../ZUGOT.md). ARH main `76234ff1816d95432a87de69b3337db5401349d4` is integrated and pushed normally. The remote README commit `7083ec0` is preserved; ARH tracked source has no additional changes. ZUGOT is the renamed application; existing historical Murmuration names and checkout path are retained as evidence.

## Observed gates

| Gate | Result | Retained evidence |
| --- | --- | --- |
| Integrated ARH unit suite | 106 pass | `arh-integrated/full-unit/output.txt` |
| Integrated native acceptance | 77 schedules pass | `arh-integrated/acceptance/output.txt` |
| Unchanged V-01 | 14 mandatory witnesses pass | [complete gate report](../v01_integrated_m1/REPORT.md) |
| ZUGOT contract tests | 10 pass | `installed-tests.txt` |
| Actual process continuity | 1 full test passes, four coordinator kills plus host reopen | `installed-continuity/zugot-cpoc-ouaat0o2/` |
| Browser | Desktop/mobile; no horizontal overflow or page errors; controls and drawer work | `browser/result.json`, screenshots and test source |
| Public client installation | Every module byte-identical to exact pinned public source | `client-install.json` |

All paths in the final column are beneath [retained app evidence](../../evidence/local-app-20261103). The installed full suite ran 11 tests in 59.608 seconds. No check was fabricated or skipped to obtain a pass. Native Linux T06, B10 core-outage substitution and R14 STOP-language limits remain as documented in ARH; these 77 schedules are not universal certification.

The complete two-cycle run closes at 198 AAA, cash 80,140.40, NAV 99,940.40 and fees 59.60. Final required exits close at zero shares and cash/NAV 99,920.60 with fees 79.40. Preserved records include rejection, correct-calculation/insufficient-dossier refusal, same-Theme follow-ups, two-way shared history, 199/99/99 allocations, partial fills, unknown response recovery against original order IDs, actual parallel worker death, UNKNOWN maximum settlement, quiescence-required refusal and one lawful replacement. Original records and independent checks survive restarts.

## Coherence and continuity review

Ownership follows the frozen constitution/contracts: ARH governance remains authoritative; the application journal owns strategy and portfolio facts; adapter state owns simulated execution receipts; displayed budgets and graph checkpoints are projections/orchestration state. There is no ARH constitutional delta or new ARH implementation. The owner's later build instruction authorizes the application responsibilities and synthetic policy choices previously proposed. This records a bounded implementation decision, not acceptance of a production constitution.

CPOC retains its established meaning, Cross-Process Operational Continuity. The installed test kills actual web coordinators at the lost-order, partial-exit and uncertain-parallel-work boundaries, kills/reopens the core host at the third boundary, and kills again after cycle 2. Fresh processes reproduce the same book/budgets and preserve public closure. Six orders, eight fills and two allocations remain unique. Independent checks, decisions and charges are not rerun. A second coordinator is refused. Source-of-truth recovery occurs before the next step; LangGraph does not grant authority.

The trusted coordinator holds broad Principal authority locally. Its finite application ingress offers no arbitrary Principal command. Role subprocesses use separate credentials, but a shared OS account can read them. This app does not claim the control service has a narrower cryptographic capability or stronger OS isolation than V-01 demonstrated. The consumer CS gate itself retains its actual separate-service/custodian witnesses unchanged.

The app uses deterministic cohort arithmetic and finite research selection. Opening allocation requires a flat, reconciled starting portfolio; competing strategies share one batch. It refuses new batches over existing holdings/orders rather than claiming general rebalancing. The adapter is a replaceable fixture, not a chosen production engine. Fixed five-minute virtual marks, historical slots and deadlines implement the finite reconstruction; there is no live scheduler or investment-performance claim. Portfolio spending and research charges never share a scale or pool.

## Failures, repairs and limitations

- Invalid semantic and UUID5 request keys refused before bootstrap; changed to persisted public `Connection.new_key()` UUID4 values. Original source retained.
- An insufficiently distinguished Checker registration was rejected. Its 1.25 setup spend remains in the failed run. Added explicit cycle-Checker instructions and restarted a fresh host.
- Unsupported combined exclusion wording refused. Its run retains 4.50 charges and 0.25 proposal allowance. Switched to the public grammar's two explicit grant-chain exclusions and used a fresh host; no core changes.
- A unit assertion compared equivalent decimal strings. Changed it to numeric equality without changing the expected value.
- Browser final-exit wait initially matched a label in the Next field and sampled step 16. The incomplete result is retained. Corrected the wait and added exact step-17/flat/cash/fees assertions; the completed original desk passed without another order or charge.
- Reviewed recovery gaps before the final installed run: persist/materialize allocation children, derive owner pause projection from its durable record, require exact pinned client source, reject a new batch with preexisting exposure/orders, and reject wrong-order receipts. Relevant tests and full installed continuity pass.
- **RV-04 OPEN — ARH packaging reliability.** Direct VCS pip installation of the exact merged commit built a wheel using stale tracked `client/build/lib` modules. Importing the public `historical_document` export failed; installation log and failed test are retained. The explicit consumer installer exports unchanged `client/arh_client`, README and metadata from the exact Git pin to a clean directory, installs and verifies all module hashes. This is a disclosed packaging procedure, not a private API or governance bypass. ARH itself is unchanged. Recommended upstream follow-up: remove generated distribution outputs from version control and add a clean-wheel public-export/source-equivalence test. That upstream change is not part of this build.
- **RV-02 remains OPEN:** public convenience Checker helper usability; supported exported lower-level route remains in use. RV-03 is resolved at this exact pin.

## Separate accounts

[App accounting](../../evidence/local-app-20261103/accounting.json) reconciles seven retained development runs: two failed runs (1.25 + 4.50) and five complete runs (5 × 8.75) = **49.50 simulated charges**, with **5.25 retained allowances**. Installed-client import failures spent zero. Unit book fixtures create no ARH charges. The live inspection desk is separate, starting at 2.75 startup charges, with its current figures visible through its public budgets; it may be operated by the owner after launch.

A complete app run spends setup 2.75 + Research 1.75 + Research 2.25 + Checking 1.00 + Checking 1.00 = **8.75**, plus **1.00 retained proposal funding**. UNKNOWN reversal cost 1.00 stays charged; replacement costs 0.50 after real termination/proof. These amounts are within the existing synthetic envelopes, with no refill or increased lineage cap. Research funding remains distinct from settled charges.

Consumer validation remains separate: prior 159.50 + integrated successor 45.50 = **205.00** cumulative consumer charges. The integrated successor retains 2.50 allowances. Native ARH certification fixtures are separate again. No real money or provider charges.

## Review and publication

The historical README, all 14 B-02 files, previous source/evidence manifests and failed consumer runs are unchanged. `ZUGOT.md` and CURRENT.md route readers to the implementation. Current source, exact environment, test source/results, public authoritative references, accounts, screenshots, failures and hashes are retained. Private host state/credentials, runtime logs and virtual environments are excluded from Git. No tokens or token hashes are published.

Run `.venv/bin/python validation/local_app/audit.py` for read-only integrity inspection. Runtime reruns use fresh disposable hosts and their own accounts. The smallest next step is to inspect the running finite desk; broader research, arbitrary portfolio rebalancing, commodity-engine selection and production isolation remain future work. No further planning or framework authorization is required to use this local demonstration.
