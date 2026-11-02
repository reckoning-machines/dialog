# V-01 runtime result — 2026-11-02

**G-CONSUMER BLOCKED; LangGraph not selected.** Owner authorized B-02 V-01 in chat. Reference B-02 commit58aad1a4e17e37b574e08a10a86e6e8c77ead27d; ARH93436406c8a1fd2c06e5713b1def09d90104db54. No ARH tracked file changed, no portfolio/UI/provider/broker/deployment/publication work occurred.

This run established an actual profile incompatibility before admitting a Research grant. Dependent witnesses were stopped, as authorized. It is not a full V-01 pass or complete CPOC evidence.

## Decisive finding RV-01: approved grant profile cannot be admitted

B-02 explicitly authorizes Research pool10.00 and per-lineage cap20.00 across bootstrap/measured grants. The public evaluator requires per_lineage_cap_units ≤ research_budget_units for each Research grant.

At BOOT-5 (G-BR), independent Check FAIL records grant_content NOT MET. No decide/apply followed that failure. Upstream evidence T20 is the proposal; exact check/settlement/closure references are retained in profile-check/BOOT-5-check.json and profile-check/closure.json. R-T and R-R designs had independently passed registration; their grants did not become active. Neither original Theme could lawfully be registered/funded as the complete profile requires.

Observed setup controls: Observation authorization PASS, zero-capital LIMITS PASS, R-T design PASS, R-R design PASS, G-BR authorization FAIL. Each used0.25. Checker committed1.25; spendable10.75; pending0; no decided-unapplied/binding obligations. Research committed0; G-BR/G-R unadmitted. The failed gate is a defect in the approved profile's fit to ARH, not evidence that shared spending itself failed.

**Smallest proposed amendment:** cap each Research lineage at10.00 (instead of20.00) on the two10.00 grants, preserving the32.00 total pool ceilings and separate12.00 Checker budget. Forecast per-lineage bootstrap+measured usage under that cap before dispatch; where a witness no longer fits, report the shortfall. Do not silently lower or broaden the approved profile. No upstream code change is necessary merely to test this amended arrangement. Owner acceptance is needed before continuing dependent work.

## Finding RV-02: public Checker convenience helper cannot select two tariffs

The profile exposes0.25 and0.50 check steps/tools under CK. Public Checker.check raises CAPABILITY_UNSUPPORTED: “one check step expected.” It consumes no check charge. A direct public attempt using0.25 against the0.50 step refuses INVALID_ESTIMATE and its unused0.25 reservation was closed, with zero charge.

A supported lower-level route did work: public Connection command envelopes plus the public arh_client.analysis.evaluator wrapper produced funded, independent checks without private core imports or a copied governance evaluator. It enabled the five startup checks above and exposed RV-01. Thus this is a convenience/interface usability deficiency, not proof the core lacks multiple check steps. No private checking.evaluate import or forged PASS was used.

## Actual independent service results

Separate BC launcher, CS-V1 service and TC processes ran from retained Murmur source. CS-V1 reads a Principal-only runtime view; TC receives only endpoint and its own caller-auth file. All files are cooperative same-OS-user separation, not enforced isolation.

Ten assertions passed: eight disallowed operations refused (decide, grant, limits, standard, fence, tick, token-export, scope-extension); wrong researcher caller refused; changed payload under a reused request ID refused. Forwarded privileged commands:0. This passes the bounded CS-04 refusal witness (nine assertions) and one CS-06 component. It does not validate positive service calls, core capability enforcement, fresh-service persistent deduplication or all of CS-06. Positive paths remain unvalidated scaffolding and must not be deployed.

The original launch and the rerun from validation/v01 are separate service-only runs, not twenty independent acceptance assertions. The repository run records the definitive10/10 result.

## Gate matrix

| Mandatory witness | Status | Evidence/limit |
|---|---|---|
| S-05 simultaneous spending | BLOCKED | Research grants unadmitted |
| S-09 core self/cross-check/approval refusals | BLOCKED | Service caller refusal is not a substitute for this witness |
| S-15A successful parallel recovery | BLOCKED | Both Research workers cannot begin lawfully |
| S-15B blocked parallel recovery | BLOCKED | No fabricated in-flight Research attempt |
| S-16 external setup/reopen/incompatible identity | BLOCKED, partial diagnostic evidence | External host/profile/genesis/partial startup and compatible blocked-state reopen worked; full setup/incompatible test not completed |
| S-19 same-root continuation | BLOCKED | Exact intended Themes remain profile data, not applied authoritative registrations |
| S-20 out-of-scope refusal | BLOCKED | No substituted test on an incomplete startup |
| S-21 ambiguous-scope refusal | BLOCKED | Same dependency; no synthetic passing claim |
| CS-01 permitted P-1 continuation | BLOCKED | No valid funded Research hypothesis |
| CS-02 policy/core refusal cases | BLOCKED | Startup/tariff diagnostic is not this measured policy suite |
| CS-03 proof/uncertain attempt recovery | BLOCKED | No lawful Research attempt in flight |
| CS-04 prohibited operations/caller | PASS, bounded |9 assertions; service-side refusal only,0 forwarded commands |
| CS-05 broad Principal-credential probe | BLOCKED | Intended independently checked hypothesis probe unavailable; no false narrow-credential claim |
| CS-06 drift/replay/restart | BLOCKED, one component passed | Changed request refusal passed; other required conditions untested |

Mandatory gates:1 bounded PASS,13 BLOCKED; no gate waived. Additional diagnostic assertions/criteria are separately reported, not added as full-suite passes.

## Continuity and accounts actually observed

The partial host was stopped, its old core process termination established, and the exact same run reopened in a fresh host. Fresh BC process public reads matched state, both-ledger closure, Checker budget and obligations byte-for-byte as decoded records. Head N4, Checker committed1.25, no pending attempts and no new charge/decision. This is reconstruction of a blocked startup, not the two-active-researcher S-15 journey.

The initial helper-only diagnostic host spent0.00 Checker units. The substantive startup host spent1.25. Service-only tests spent0.00 governed units. Total observed actual spending across disposable runs1.25; no actual provider/capital spend. Each independent run has its own approved cap/profile; no charges moved between runs.

One consumer fixture error was repaired: Observer.observe requires file metadata for a many-item source. Startup first stopped with KeyError:file after the first0.25 check. The consumer then used public historical_document over retained synthetic JSON bytes and resumed previously applied BOOT-1 rather than checking/charging it again. Both failure note and source-repair diff are retained. Pre-repair source was reconstructed from the recorded edit delta; it was not timestamped independently before execution. No additional Check was hidden.

## Reproduction and retained evidence

Run source: profile.py creates external inspectable setup/design/experiment JSON through public Project generation and explicit documented data edits; tools.py is the synthetic computation; evaluator.py uses the public wrapper. startup.py performs BC public control checks and stops on FAIL. bootstrap_probe.py captures the convenience-helper and core-tariff diagnostic. control_service.py/service_tests.py implement the isolated refusal witness. lifecycle.py/retain.py capture public snapshots and redacted evidence.

Runtime setup used an isolated Python3.12.3 venv, installed public client0.1.0 from a temporary byte-identical source copy, LangGraph1.2.19 and SQLite checkpoint3.1.3. dependencies.lock pins all installed packages. environment.json and client-source-comparison.json retain actual versions and module hashes. Dependency installation initially hit sandbox DNS restrictions, then succeeded with approved network access. No source build wrote to the ARH client directory.

Host invocation: from the pinned ARH checkout, with PYTHONDONTWRITEBYTECODE=1, invoke its documented local_host module with external --setup and disposable --run. B-02 requires a checkout-based host; direct core imports/ledgers are absent from consumer code. The freeze command creates its normal development build archive in the ARH checkout; one sandbox-denied archive attempt is recorded as operational setup, not governance failure. Retained inventories name exact execution bytes. ARH tracked-source diff stayed empty.

Evidence index is evidence-manifest.json: public profile/closure/check/budget/obligation JSON, original synthetic input, service/refusal/process evidence, compatible-reopen parity, package lock and exact-secret redaction scan. No raw runtime connection file, Principal/TC credential or ledger database is copied. The frozen B-02 document manifest remains a review snapshot; runtime artifacts have a separate integrity manifest.

The hosts and service processes were stopped. Runtime credential files are deleted after evidence/redaction capture; no token values or token hashes are retained. Durable public history remains in exported closure JSON. Disposable state databases remain private scratch material and are not evidence fallbacks.

## Next decision

Authorize the narrow RV-01 profile amendment, or decline further validation. If accepted, regenerate inspectable setup/source pins and rerun V-01 with unchanged success/refusal requirements. The0.25/0.50 helper finding is handled by the demonstrated public lower-level route; it warrants an explicit upstream interface usability report, not a hidden workaround. Do not select LangGraph, start a broad documentation cycle or implement portfolio/UI from these partial results.
