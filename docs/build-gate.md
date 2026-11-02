# Proposed implementation sequence and build gate

**PROPOSED — NO IMPLEMENTATION AUTHORIZATION.** User has accepted the stack as the right proposal for docs-only design, not authorized code, installation, runtime tests or infrastructure. [Review CL-01](review.md) closes only this documentary assignment.

Latest sequence: first operate and review [W-2 on paper](desk-walkthrough.md), as requested by the owner; [CL-03](review.md) records repairs and unresolved product choices. Runtime consumer validation comes afterward and still requires explicit authorization. W-2's hypothetical owner decisions do not accept the constitution, change V-01 or select LangGraph.

## Broader design decisions — remain proposed

The consumer test does **not** require acceptance of M-CV1, ES-M1, M-1, D-02 or D-05. Only the scoped ownership boundary of D-01 and the standalone synthetic validation profile V-01 below are submitted for the next authorization. Correcting the portfolio documents does not admit their semantics or delegation.

| ID | Proposed decision | Remaining choice / consequence |
|---|---|---|
| D-01 | Murmur owns strategy versions, allocation, risk limits, paper orders/fills and retirement under M-CV1; ARH owns only the research governance actually consumed | Accept scoped boundary. Roadmap overlap alone is not blocking. Do not exercise capital actions under ARH's zero-capital grants. If later adopting ARH trading authority, migrate by explicit owner decision with history/identity mapping and cutover, never parallel owners |
| D-02 | Accept M-CV1/ES-M1, two approaches, shared research pool plus independent Checker budget, finite two scheduled slots, cooperative synthetic trust boundary | Numeric budgets, universe, limits, costs, cadence and admission criteria are proposed fixtures. Owner must accept or revise before runtime grants. Historical data needs point-in-time availability evidence |
| D-03 | Python application and public ARH Python client foundation; LangGraph candidate coordinator only | Select LangGraph only after S-05/S-09/S-15/S-16 show supported two-researcher integration and recovery; otherwise document failure and compare simpler coordinator without changing authority semantics |
| D-04 | No paid providers, broker, deployment, remote publication, real capital or IRIS dependency in first slice | UI and simulation engine remain unselected. Engine choice requires adapter capability comparison; UI choice follows C-09/10 needs |
| D-05 | Owner retains first strategy eligibility, resumption, retirement and policy/standard/grant changes; deterministic standing authority covers routine research, bounded allocation and exits | Approve exact delegation; do not treat a scheduler or graph resume as consent or an ARH Principal grant |

## Intended stack

| Layer | Proposed choice | Responsibility |
|---|---|---|
| Application | Python | Murmur research/trading-domain behavior |
| Research governance | ARH public Python client | Its implemented authorization, budgets, evidence, checks, acceptance |
| Swarm orchestration | LangGraph, pending validation | Coordinate distinct researcher operations, branches and interruption/resume; no authority |
| Portfolio mechanics | Ordinary Python | Deterministic allocation, limits and paper-order rules |
| UI and simulation engine | Unselected | Meet contracts before choosing components |

## Sequence after explicit authorization

1. **Consumer validation first, under V-01 only.** Pin exact dependency and cooperative synthetic profile in the sibling repository. Use documented external setup and lower-level public keyed interfaces where necessary. Demonstrate two separate researcher lineages sharing G-R, mutual rejected-history visibility, designated-token self/cross-check and approval refusals, simultaneous last-unit contention, and both S-15A successful and S-15B blocked recovery with both researchers active. Record integration effort and confusing/unsupported interfaces. No ARH repairs in that scope; report upstream findings.
2. **Framework gate.** Choose LangGraph only if those witnesses pass with durable independent operation journals and resumed authorization checks. Document every skip/refusal/failure; framework convenience cannot waive semantics. If supported setup cannot express the required role/budget arrangement, stop dependent work and request a bounded upstream interface change, not a local duplicate ledger.
3. **Murmur domain core.** After separate authorization, implement owner mandate, methods, strategy dossier/lifecycle and portfolio command boundaries with exact histories. Choose an existing backtesting/paper engine against C-06; retain synthetic fixtures as the initial controlled witness. Implement W-1, S-03/S-11/S-12 and duplicate-order recovery before UI actions can execute them.
4. **One workspace.** Choose UI only after owner-resolved read/command contracts exist. Implement C-09/10, including stale/pending/interrupted/unavailable behavior and rejected ancestry. No infrastructure chatter in primary view.
5. **Bounded runtime acceptance.** Execute full scenario/traceability coverage including CPOC process boundaries; retain exact reports. Assess investment/research usefulness separately from ARH reliability/usability. Later historical replay needs independently reviewed timing/reuse and engine evidence; fresh forward research requires F-03 resolution and new authorization.

## Gates and current standing

| Gate | Requirement | Current disposition |
|---|---|---|
| G-DOC | Navigable design, ownership, fixtures, source assessment, adversarial repairs and explicit unresolved issues | Complete as documentation; not admitted |
| G-DESK | Two complete paper cycles, successive workspace states, behavior/continuity/clarity checks and replayed defects | W-2 complete conditionally on its proposed owner choices; U-W2-01–04 visible, no runtime or usability attestation |
| G-OWNER | Owner accepts D-01's scoped ownership boundary, V-01 and its bounded implementation/evidence-retention scope | Pending; full constitution and portfolio delegation are not prerequisites |
| G-CONSUMER | S-05/09/15A/15B/16 actual independent-consumer evidence, keyed recovery and compatible reopen, no private workaround | Not executed; both success and blocked fixtures mandatory; cannot claim ARH integration validated |
| G-DOMAIN | Runtime behavior for admitted paper lifecycle/limits/exits and replaced commodity adapters | Not implemented |
| G-CPOC | Exact durable state survives forced process boundaries and historical read with surface parity | Not executed |
| G-USEFUL | Research choice responds to retained evidence; realistic historical assessment distinct from API verdict | Toy documentary witness only; profitability unknown |

Ready to request a **bounded consumer-validation implementation authorization**, not an unconditional build of the full application. Shared-pool core support is visible in source; public external composition remains to demonstrate. An upstream packaged host is not a prerequisite if the documented checkout-based host works unchanged. Forward APIs and hardened isolation are later-scope blockers, not invented first-slice prerequisites.

Exact next requested authorization:

> Accept only D-01's scoped ownership boundary and synthetic validation profile V-01, and authorize local ARH consumer validation in `murmuration`: distinct researchers, shared budget, mutual rejection-history access, role refusals, simultaneous spending, and both successful and blocked forced parallel recovery. Use Python and ARH's public client, with LangGraph remaining a candidate until all required evidence exists. Allow minimal dependency installation and disposable local host initialization for those tests. Retain test source, exact dependency versions and complete evidence in Murmur; hosts may be temporary. Do not modify ARH, use paid providers, implement portfolio/UI execution, connect a broker, deploy or publish. Report unsupported paths without private workarounds. M-CV1, ES-M1, M-1 and broader portfolio/delegation decisions remain proposed and require separate acceptance before domain implementation.

This request is a concrete future scope; writing it does not grant it. The current assignment ends with documentation.

## V-01 — standalone synthetic consumer-validation profile

Status: proposed, independent of the paper-trading mandate. Its subjects are research operations, role refusals and recovery, not strategies, positions or capital. Scope is one local cooperative environment, immutable generated inputs, no network data/provider calls, two distinct Research designs R-T/R-R, independent Checker CK and explicit owner/operator role. Researcher grants contain no checking or decision authority; owner credentials are used only by the designated test controller. The shared local token-file weakness is disclosed; no isolation claim.

Pin ARH commit `93436406c8a1fd2c06e5713b1def09d90104db54` and client0.1.0 as the inspected candidate. Before execution record actual source digests/dirty state, exact Python, LangGraph and transitive package versions and immutable install inputs. No floating dependency resolution counts as a retained pin. If another ARH revision is needed, stop and document the compatibility delta before changing the baseline.

Use independent fresh disposable runs for S-05, S-09, S-15A, S-15B and S-16 as needed to avoid state contamination. Fixture-specific prefixes are part of each run, with no database edits or arbitrary reset of balances. Shared G-R cap10.00 uses synthetic research units; R-T/R-R may reserve under the same grant. V-01 uses a separate G-C cap12.00 covering setup as well as measured checking, instead of M-1's2.00 checker default; its exact charges are retained and it is untouched during S-15A/B. S-05 creates its documented9.00 committed prefix through public metered work, then races the final1.00. S-15A/B use the exact maxima/actual tariffs and accounting tables in scenarios.md, no extra costs inside the measurement interval. A refused admission is not a provider call.

Startup and prior rejected variants must also be genuinely created through public interfaces and separately accounted. One shared bootstrap Research grant G-BR has cap10.00; close its reservations and fence it before the measured G-R interval. G-C is the same Checker grant throughout, with per-lineage cap12.00; setup/history checking may consume at most10.00, leaving at least2.00 for measured role checks. The test controller must stop if this preparation threshold is exceeded, not dispatch work with inadequate checking funds. Record every actual charge, pending liability and release. No checkpoint or dataset import can fabricate a prior rejection.

For V-01 only, research per-lineage caps are20.00 across G-BR and G-R; lineage usage is retained across grants. Total grant pools bound authorized run expenditure to32.00 units (G-BR10 + G-R10 + G-C12), with no transfers or implicit refills. The bootstrap and measurement grants must be legitimately activated via supported checked controls, not direct ledger changes. If setup cannot fit or the public interface cannot express this profile, record a blocked consumer finding; do not silently enlarge budgets. Both researchers must read the same exact rejected variant/check/decision references and cite the other's rejection in subsequent research selection; any metered follow-up outside S-15's accounting interval must use remaining declared grants and be separately reported. This profile supersedes M-1's defaults only for these consumer fixtures; M-1 is not accepted.

S-09 must demonstrate refusal under each designated research identity of self-checking, checking the other researcher's proposal and approval/decision, followed by a legitimate CK check and owner action. S-16 must start from the separate Murmur repository, run the shared-budget/role/parallel cases, reopen exact inputs and reject incompatible execution identity. Unsupported public behavior is a finding, never a passing skip. LangGraph is selected only after all required fixtures have their exact expected results; a safe blocked result passes only the deliberately blocked S-15B fixture.

Retention is mandatory even if hosts are deleted: keep the test source and configuration, exact dependency lock/inventory, input hashes, commands, environment, complete run-level and per-grant accounting (including bootstrap), authoritative record exports through public reads, operation journals/receipts, process IDs and termination/quiescence evidence, refusals, observed-versus-expected tables and actual pass/fail/skip counts. Store these in the Murmur repository or its retained local evidence directory with an index and digests; do not commit identity tokens. Retain evidence before removing a temporary host. No executable witness or dependency lock is created in this documentary repair.


## Latest product proposal — DA-1 remains documentary

[W-3](away-replay.md) and [C-12/C-13](contracts.md) are the owner-away proposal, with closure CL-04. Research and holding duration are separate per owner preference; numerical deadlines, delegation and trusted control-service assumptions remain proposed. D-05's per-instance owner decisions in W-2 are now the baseline being challenged, not the unattended design target. No broader baseline acceptance is inferred.

The exact existing V-01 authorization request remains bounded consumer validation, not implementation/admission of DA-1 or an ARH repair. Add documentary acceptance obligations for any later autonomy scope: current P-1 continuation through public privileged ingress, rejection when used by a researcher, fresh-base/funding and suspension behavior, pending Theme after P1_CLASS, and no grant inheritance on design succession. DA-T is a separate proposed upstream change requiring its own legitimate decision and implementation authorization. DA-S/DA-X and independent portfolio duration belong to later Murmur domain authorization. No zero-interruption runtime claim is possible from these papers.


## B-01 frozen review baseline

The [final narrow comparison](baseline-review.md) establishes the intended ordinary path: preserve existing Theme identity, use supported selection/design/revision/evidence and P-1 hypothesis transitions within exact grant scope. Genuine domain/scope change remains an owner exception; DA-T is not requested for these follow-ups. Initial exact Theme/grant references must demonstrate fit; no retrospective widening.

The next proposed V-01 validation additionally includes NC-05 CS-01–06: trusted-service public permitted calls, service refusals, upstream refusals and explicit broad Principal-credential negative control, plus same-root continuation/out-of-scope cases. Retain evidence inside existing declared validation pools; if additional funded checks cannot fit, report the budget gap before requesting an amended profile, never silently enlarge it. This is a refinement of the next proposed test scope, not permission to execute it or implement portfolio delegation.

Review freeze is B-01 with local commit/content manifest. Constitution/DA-1/parameters and implementation remain proposed. Next step is owner review and a concrete bounded implementation decision, not another broad documentation cycle or upstream Theme-policy request.
