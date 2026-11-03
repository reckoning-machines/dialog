# Proposed constitution — M-CV1

Status: **PROPOSED, NOT ADMITTED**, 2026-11-02. The owner alone can admit this constitution. Terms and invariants are defined here; [contracts](contracts.md) specify behavior without changing meaning. ARH terms retain their upstream meaning; Dialog does not amend ARH CV1.

## Jurisdiction and change

R-03: Dialog is a separate application and repository. No private ARH imports, direct ledger reads/writes, copied rules engine, or invented ARH commands are permitted. Public exact-record references are lawful; a local copy cannot decide ARH standing. Missing capability becomes a finding and a stopped dependent transition.

Use ARH’s adopted engineering motion **Audit → Plan → Implement → Verify**. Here Implement means documentary edits. Audit asks Ontology, Semantics and Authority (OSA); Verify challenges concrete fixtures and records repairs. CPOC retains **Cross-Process Operational Continuity**: already-lawful state must survive persistence, process death, fresh reopening, reconstruction, lawful continuation and historical verification using durable authority. CPOC creates no authority and is not portfolio composition checking.

Initial proposed constitutional delta relative to no Dialog system: ΔO = new application domain objects below; ΔS = new explicitly scoped paper semantics; ΔA = proposed owner delegation to Dialog boundaries. Delta to ARH: 0/0/0; no ARH authority moves by this document. D-01 in [build gate](build-gate.md) must resolve the compatibility of this split with ARH’s broader unimplemented trading constitution. After admission, ordinary work has ΔO/ΔS/ΔA=0/0/0. Meaning, identity, authority or evaluation-standard changes require a new owner decision, prospective version and impacted documentary reruns. Never reinterpret old results under new standards.

## Terms and authority map

All proposed Dialog authoritative records are append-only, use immutable content and identifiers, and include actor, mandate version, event time, effective time, predecessor where applicable, expected aggregate revision and command identity. An identifier cannot be rebound. A changed immutable object gets a successor ID; a lifecycle change appends an event. ARH identity rules remain ARH’s. Exact ARH references include host/run identity, ledger, sequence and hash; sequence alone is not globally unique.

| Object or fact | Meaning / identity | Single authority and commit boundary | Other representations and denied rights |
|---|---|---|---|
| Mandate / standard | Owner-approved universe, instruments, schedule, research caps, evaluation rules, portfolio limits, validity and delegates; M-1 / ES-M1 immutable versions | Dialog owner decision boundary; owner only | Config and UI are DERIVED; cannot grant rights. ARH grants separately require its Principal path |
| Cycle | One scheduled investigation slot; `(mandate, schedule, slot)` | Dialog scheduler command boundary; at most one accepted cycle per key | Job queues are CACHE; cannot create a second cycle |
| Method version | Immutable research recipe and search-space definition, e.g. MV-T1; includes family and parent | Dialog research-plan boundary registers proposed recipe and selection history; owner approves method eligibility | ARH Agent Design references describe execution identity, not duplicate method authority; rankings DERIVED |
| Research design, attempt, budget, receipt, check, proposal, admission | ARH’s own governed research facts | ARH public commands; its evidence/transition commit and Apply boundaries | Dialog stores exact references and CACHE snapshots; cannot settle, check or admit locally |
| Hypothesis | Testable proposition registered through ARH; immutable upstream identity | ARH registration/Apply; Dialog references it | Dialog hypothesis assessment is a DERIVED research summary, not ARH standing or forward Evaluation |
| Strategy version | Immutable signal-to-target recipe, instruments, timing, costs, risk and exit rules, method and hypothesis references; SV-T1 | Dialog strategy boundary creates candidate and applies lifecycle events after evaluation and owner/delegate decision | Backtest output is evidence; cannot activate itself. No ARH strategy identity claimed |
| Admission dossier | Frozen evidence bundle for one strategy and ES-M1, including provenance, search history and independent evaluation | Dialog evaluator commits domain assessment; strategy boundary alone decides eligibility | ARH arithmetic check cited exactly, never relabelled scientific support |
| Allocation batch | Desired attributed quantities for eligible strategies at one portfolio revision; AL-1 | Dialog portfolio boundary validates composition and commits targets atomically | Strategy requests are EPHEMERAL until recorded as inputs; target is not position |
| Order / fill | Paper instruction O-1 bound to allocation, strategy and decision event; fill F-1 with unique adapter execution ID | Dialog paper-book boundary admits orders and validated fill receipts | Adapter receipt is RECEIPT for simulated execution; cannot allocate. Positions/cash/NAV DERIVED from accepted fills, fees, cash events and marks |
| Market data manifest | Exact bytes/digest, universe membership, revisions, event time, publication availability interval, retrieval time and source | Dialog data intake owns provenance declaration; when imported, ARH owns its observation record | Local dataset cache cannot replace pinned input; origin declarations are not proof of truth |
| Request journal | Durable intent, key, payload hash and returned references for one command | Respective command owner; ARH client owns its operation journal | Operational RECEIPT, no substantive admission rights; graph checkpoint CACHE |
| Workspace / alerts | Joined presentation with per-source as-of and revision | DERIVED from the owners above; no new authoritative aggregate | Browser selection EPHEMERAL; stale CACHE cannot authorize commands |

The six representation classes are AUTHORITATIVE, DERIVED, CACHE, RECEIPT, LEGACY_ONLY and EPHEMERAL. Proposed, working, pending and retired are lifecycle standings, not extra classes. Imported obsolete displays, if any, are LEGACY_ONLY and barred from current decisions. Audit records are evidence and authorize nothing.

## Invariants and requirements

| ID | Invariant / requirement |
|---|---|
| I-01 | One authority per fact, exact historical identity, owner-resolved currentness. Every significant transition uses the owner's commit boundary; fail closed when authority is missing |
| I-02 | Owner grants authority; performance and agent capability confer none. Checkers cannot decide, proposers cannot check their own lineage or admit themselves |
| I-03 | Reserve before work; pending maximum liabilities count; rejection, restart and succession never erase charges or budget history. Research units and paper capital are different budgets |
| I-04 | Immutable design/expectation precedes the experiment. Preserve attempts, negative results, refusals and ancestry. Successor forward record starts at zero |
| I-05 | Historical Reconstruction and future Contemporaneous Forward Record are separate. Reused samples are exploration; no unavailable-at-time input may enter a valid replay closure |
| I-06 | Hypothesis belief, strategy operational/performance assessment and method research contribution are separate. Arithmetic PASS does not imply evidentiary sufficiency or strategy eligibility |
| I-07 | Every consequential decision pins current authority, evidence and base revisions. Stale, revoked or incompatible state refuses, without silent rebasing |
| I-08 | Portfolio admission evaluates aggregate exposure including open orders, strategy overlap, cash and fees. A strategy's individual limits do not establish composition legality |
| I-09 | Targets, orders, fills and positions are distinct. Suspension/retirement never erase open positions or exit obligations. Unknown order completion forbids replacement exposure |
| I-10 | Persist identity before side effects; reconstruct exact state after process death; no duplicate work, settlement, decision or order on ordinary replay. Explicit replacement is a distinct charged attempt |
| I-11 | UI facts name their authoritative sources and freshness; pending, stale, interrupted and unavailable are explicit. No screen state grants authority |
| I-12 | ARH is consumed through public supported surfaces only. Unsupported behavior stops with an upstream finding, not local governance substitution |

R-04: one small complete research-to-paper cycle plus a subsequent evidence-informed question. R-05: replaceable commodity replay and execution adapters, no vendor chosen. R-06: deterministic arithmetic, limits, scheduling and execution mechanics use ordinary code when authorized. R-07: IRIS may later contribute company forecasts, saved research, Methods and optionally conviction assessments as versioned source references; no conviction score definition or IRIS connection is needed now.

Routine standing authority, if D-02 is accepted: researchers run bounded predeclared investigations, evaluator checks independently, scheduler resumes existing cycles, allocator adjusts already eligible paper strategies within limits, paper executor fills under declared simulation rules. Owner decides mandate/grant changes, new methods, first strategy admission, resumption after suspension, retirement and exceptions. ARH Principal/policy actions remain exactly its own; a Dialog delegate does not acquire an ARH token right by implication. Emergency stop blocks new exposure; existing liabilities still require lawful settlement and exit handling.

The next consumer-validation request accepts neither this full constitution nor the portfolio/exit delegation above. Its separate V-01 profile exercises only the research ownership boundary and synthetic interface behavior. C-05's repaired exit semantics remain proposed until separately accepted by the owner.


Proposed delegation refinement DA-1: the current unattended-design proposal is defined once in [C-12/C-13](contracts.md) and tested in [W-3](away-replay.md). It would let deterministic Dialog admission/retirement boundaries decide narrowly defined routine cases after independent checks, while owner-only changes/judgment remain exceptions. This is a proposed authority delta relative to the W-2 manual baseline; the constitution remains unadmitted. ARH semantics/authority do not change here: DA-T requires separate upstream admission/implementation, P-1 keeps its current scope, and no Dialog policy grants itself an upstream right. Research completion and holding/exit authority have separate lifetimes, reflecting the owner's stated preference; exact parameters remain proposed.


Frozen B-01 scope interpretation: a more specific experiment within the exact admitted Theme/grant does not create a new Theme. Meaning/scope changes follow ARH successor rules and remain owner-gated unless an applicable upstream policy is separately admitted. [Final comparison](baseline-review.md) is the authoritative documentary classification for the proposed ordinary-follow-up path; immutable original content is not retroactively broadened.
