# RV-01-A1 consumer validation — completed, gate failed

2026-11-02. **12 of 14 mandatory witnesses passed; CS-01 and S-09 failed. LangGraph remains unselected.** This is bounded synthetic consumer evidence, not investment, portfolio, UI, isolation or production validation.

The authorized Research cap amendment was applied and independently checked at startup: G-BR and G-R each have pool 10.00 and lineage cap 10.00; the Checker pool/cap remains 12.00. Exact original Theme statements were preserved. No ARH source, acceptance criterion or other limit changed. B-02 at `58aad1a4e17e37b574e08a10a86e6e8c77ead27d` and the failed run at `ccf31b48447b7d44308e20e6da7f4e3491387385` remain historical inputs.

## Observed outcomes

| Witness | Result | Retained observation |
|---|---|---|
| S-05 shared spending | PASS | Two barrier-synchronized reservations compete after real 9.00 prefix; exactly one commits, other BUDGET_EXCEEDED; winner closes unused 1.00 |
| S-09 role refusal and legitimate Checker completion | FAIL | All six actual self/cross check/decision/policy requests are UNAUTHORIZED; required independent 0.50 Check cannot commit |
| S-15A parallel successful recovery | PASS | Both researcher workers and coordinator killed/reaped; original receipt recovered, other original charged UNKNOWN 1.00; retry refused before host proof, replacement 0.50 after proof; actual graph resume completes both branches |
| S-15B blocked recovery | PASS | Same simultaneous interruption; without proof no replacement; fresh process reconstructs 1.75 settled plus 1.00 retained allowance; graph remains interrupted |
| S-16 reopening | PASS | Fresh exact-run host preserves closure/accounts; modified disposable executable refuses ARTIFACT_CHANGED; restored exact bytes reopen without new charge |
| S-19 same Theme | PASS | New quiet-cohort design, actual calculation, independent check, P-1 decision and Apply; original Theme map unchanged |
| S-20 outside scope | PASS | CCC motivation refused SCOPE_VIOLATION; service refuses missing authorized proposal; no dispatch/scope rewrite |
| S-21 ambiguous scope | PASS | Wrong exact-reference hash refuses INVALID_REFERENCE; fixture records TB_SCOPE_UNRESOLVED and stops |
| CS-01 permitted P-1 path | FAIL | Declared 0.50 attempt/receipt accepted; Check commit refuses UNFUNDED_CHECK, so required positive path incomplete |
| CS-02 invalid policy | PASS | Genuine FAIL/STOP/stale/missing-check/funding cases; separate checked Theme refuses P1_CLASS, service refuses it; checked suspended-policy fixture refuses POLICY_SUSPENDED |
| CS-03 recovery service | PASS | Original attempt charged; retry refuses WORKER_NOT_QUIESCENT until separate public host proof; replacement retains ancestry and cost |
| CS-04 service restrictions | PASS | Eight disallowed operations plus wrong researcher caller refused before forwarding, including explicit researcher requests |
| CS-05 broad credential | PASS | Separate raw-credential process successfully requests legitimate P-1/Apply; service allowlist is not a scoped Principal token |
| CS-06 drift/restart | PASS | Wrong caller, changed payload/key and stale base refuse; recheck/current decision, service restart and replay preserve one decision |

[results.json](../../evidence/v01-rv01-a1-20261102/results.json) contains exact outcomes/references. [export-verification.json](../../evidence/v01-rv01-a1-20261102/export-verification.json) records subsequent assertions over exports; these assertions are not additional runtime witnesses.

Each researcher reads retained failed variants from the other and records its subsequent selection. Research, checking and acceptance remain different roles. Graph checkpoints restore execution, not authority: retry still fails before public host quiescence proof. No paper order is implemented or claimed.

## Upstream findings

**RV-01 — closed by owner-authorized profile amendment.** The original lineage 20.00/grant 10.00 mismatch was correctly rejected by independent checking. Successor startup checks admit the specified 10.00/10.00 profile.

**RV-02 — open, public interface usability.** The convenience Checker context assumes the first check step and its fixed maximum. The authorized public lower-level `Connection`/`invocation`/top-level exported evaluator route works for the 0.25 step and exposes the next limitation. Consumer code supplies scientific arithmetic/uncertainty, not copied governance or fabricated criteria.

**RV-03 — open, blocking core interface incompatibility.** ARH's Experiment permits multiple named check steps and admits `check-half` with maximum 0.50. `rules.py:252` then requires the literal `check-transition` at Check commit and returns UNFUNDED_CHECK. Attempt maximum must also equal its declared step maximum (`rules.py:174`); relabeling the half-unit attempt as a quarter-unit step is not a lawful repair. Both tariffs are required by B-02. The refused attempt stays charged 0.50, and no Check/decision is invented. S-09's second required 0.50 completion is blocked by the same interface; it was not dispatched as a doomed duplicate. [ARH-source-pins.json](../../evidence/v01-rv01-a1-20261102/ARH-source-pins.json) pins inspected source bytes. No upstream repair was made.

## Accounts and boundary

All amounts below are simulated research units. No paid provider or portfolio capital was used. Pre-dispatch conservative combined bootstrap/measured bounds are 7.50 per lineage for contention, 4.00 for recovery, and 7.75 for CS/scope, below 10.00; proposal allowances and pending maxima are included. Authoritative preflight and ready snapshots preserve actual prior charges. Bootstrap settles T 0.75 plus R 1.00, closes unused allowance, then fences G-BR. There is no refill or cross-run transfer. ARH computes lineage caps within a selected grant; the consumer's combined forecast is deliberately stricter.

| Final family | G-BR settled | G-R settled | G-R retained allowance | G-R spendable | Checker settled |
|---|---:|---:|---:|---:|---:|
| Contention | 1.75 | 9.00 | 0.00 | 1.00 | 2.00 |
| Successful parallel | 1.75 | 2.25 | 0.00 | 7.75 | 2.00 |
| Blocked parallel | 1.75 | 1.75 | 1.00 | 7.25 | 2.00 |
| Reopen | 1.75 | 0.00 | 0.00 | 10.00 | 2.00 |
| Main CS/scope | 1.75 | 2.25 | 0.75 | 7.00 | 4.50 |
| Auxiliary policy edges | 1.75 | 0.00 | 0.25 | 9.75 | 2.75 |
| Repaired process boundary | 1.75 | 0.00 | 0.25 | 9.75 | 2.25 |

Final seven families settle 45.00. All 19 successor hosts, including failed/replaced runs, settle **112.75**: Checker 47.50, bootstrap Research 31.50, measured Research 33.75. Their retained allowances total 5.25, separately from charges. The predecessor's 1.25 Checker spending remains separate and was not reused. No individual pool/lineage ceiling was exceeded; no pending unsettled attempt remains. The deliberately blocked replacement allowance and applied-proposal funding remain visible. [accounting.json](../../evidence/v01-rv01-a1-20261102/accounting.json) enumerates every host and public authoritative export.

Main CS planned measured Checker consumption was 3.00; actual is 2.50 plus setup 2.00 because the required second half-unit check could not run. This is a failed fixture outcome, not an accepted new accounting profile. The first failed half-unit run initially left a known receipt pending; fresh public reconciliation settled exactly 0.50 and closed its original reservation. Before/after evidence retains that failure without a refund. Extra class/suspension checks are separately itemized in fresh auxiliary hosts within the unchanged setup ceiling. No budget shortfall required another limit change.

Combined custodian/controller instrumentation initially failed to demonstrate the requested credential boundary. The repaired dedicated witness shows BC provisioning and exiting before TC requests; TC receives only its own authenticated service endpoint/caller credential, never a Principal token. Service holds the Principal-only connection view; separate researcher/Checker views are mode 0600. Same-user file access remains possible and is explicitly observed. This is cooperative process organization, not OS isolation or narrowly scoped token enforcement. [boundary/separation-witness.json](../../evidence/v01-rv01-a1-20261102/boundary/separation-witness.json) records actual process/call results. Other fixture instrumentation remains privileged custodian instrumentation and is not presented as TC separation proof.

## Reproduction and limits

ARH stays at `93436406c8a1fd2c06e5713b1def09d90104db54`, tracked diff empty. Normal disposable-host freezing produces development archives; existing unrelated work was preserved. Python 3.12.3, byte-identical public client 0.1.0, LangGraph 1.2.19 and checkpoint-sqlite 3.1.3 are pinned with transitive dependencies in the evidence lock/environment. All 14 frozen B-02 document hashes/byte counts still match.

[commands.md](commands.md) explains the scratch layout. Complete source at the final required family starts is retained and hash-verified; some earlier required-family snapshots were reconstructed from bytes matching their pre-run hashes, not falsely described as pre-run copies. Earlier superseded runs retain public exports, hashes and known repair history. Consumer operation/receipt journals and graph checkpoints are retained separately from ARH governance exports; no ARH database was accessed or retained. [repair-log.json](../../evidence/v01-rv01-a1-20261102/repair-log.json) preserves consumer failures and repairs.

Services/hosts/workers are stopped; evidence is compared against actual provisioned secrets before credential files are deleted. The exact-value scan covers 103 secrets still available in private provisioning views; earlier rotated host tokens were not retained for rescanning. A separate structural JSON audit and search for the host’s 48-hex token format also found no credential material. Source/evidence manifests pin the retained files. Runtime receipts and command records retain outcomes/references without authentication headers/tokens. Service restart was tested; arbitrary storage faults or every possible kill point were not. These results establish bounded governance/consumer behavior and expose an interface incompatibility. They establish no strategy profitability or production guarantee.

**Smallest next decision:** authorize a bounded upstream repair of Checker-step validation with regression tests, then explicitly pin/review the revised ARH dependency and rerun the unchanged mandatory V-01 gate. Alternatively decline that repair and leave the integration/framework gate failed. A profile/acceptance amendment would be a separate decision; none is silently substituted here. Portfolio/UI implementation remains unauthorized.
