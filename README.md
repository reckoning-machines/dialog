# Reckoning Machines Murmuration

**B-01 — documentary baseline frozen for review.** Read the [final Theme comparison and freeze](docs/baseline-review.md), then [C-12/C-13](docs/contracts.md) and [CL-04/CL-05](docs/review.md). Ordinary in-scope follow-ups need no new Theme approval; exact initial Theme/grant fit is a precondition. DA-T is optional for autonomous scope changes, not required by these routine questions. This corrects the earlier replay’s architectural inference without rewriting its records or totals.


**Murmur** is a proposed adaptive trading research and paper-trading application, presented as IRIS’s sibling. It owns its swarm, trading-domain decisions, shared paper portfolio and visual workspace. Adaptive Research Harness (ARH) supplies the research governance it actually implements, through its public client and host interfaces.

**Standing: documentation only; constitution and build decision PROPOSED. No application, executable fixtures, infrastructure, broker, deployment or remote repository exists in this package.** The initial name Trial Balance was replaced by the owner during this assignment. Repository name: `murmuration`. Trademark investigation was explicitly stopped by the owner; no clearance claim is made.

Two equally weighted goals:

- **R-01 Investment behavior:** establish a useful, bounded process that learns from unsuccessful as well as successful research, distinguishes hypotheses, strategies and methods, and translates eligible strategies into a controlled shared paper portfolio.
- **R-02 Dependency validation:** independently consume ARH and assess public-interface completeness, clarity, reliability and usability. Research profitability and interface robustness receive separate verdicts.

The proposed first slice is two competing research approaches (trend persistence and reversal), one independent evaluation role, one deterministic scheduler and allocator, and one shared paper portfolio. Scheduled historical cycles and synthetic fixtures establish operational behavior. Historical performance is labelled **Historical Reconstruction**, never forward evidence. Roles need not be LLM agents. “Starlings” is optional presentation vocabulary for researchers, with no authority implied. A “turn” may label an allocation batch; neither term is a new governed object.

Read in order:

1. [Proposed constitution](docs/constitution.md): terms, ownership, invariants and authority.
2. [Behavioral contracts](docs/contracts.md): research, strategy, portfolio and recovery.
3. [ARH assessment](docs/arh-assessment.md): inspected implementation and integration gaps.
4. [Workspace and worked example](docs/workspace.md).
   Then [operate the desk for two cycles](docs/desk-walkthrough.md): successive workspace cards, exact records, disrupted research/orders, exits and evidence-informed next choices.
5. [Documentary scenarios and traceability](docs/scenarios.md).
6. [Review, CPOC and findings](docs/review.md).
7. [Implementation sequence and proposed build gate](docs/build-gate.md).
8. [Current work](docs/current-work.md): resumption instructions.

The paper design is coherent within the proposed ownership split. Python and ARH's public Python client are the foundation; LangGraph is the orchestration candidate pending the worked two-researcher validation gates. The complete slice is **not ready for unconditional implementation authorization**: owner admission, externally composed multi-researcher setup, and consumer recovery/compatibility questions remain open. ARH roadmap overlap alone does not block the design. Documentary closure does not close upstream findings or demonstrate runtime behavior.

The next request is narrower than accepting the full design: accept the ownership boundary and standalone synthetic consumer profile V-01 in the build gate. Portfolio semantics and broader delegation remain proposed. The reviewed repairs specify separate successful/blocked parallel-recovery fixtures with exact accounting, and a required-exit scenario exceeding ordinary turnover under an explicit cost envelope.

The latest product test is [W-3: owner-away replay](docs/away-replay.md), with proposed standing authority in C-12/C-13 and closure CL-04. Current ARH still requires one batched successor-Theme approval interruption on this exact journey; zero routine interruptions is conditional on a documented upstream policy extension. Research schedules and position lifetimes are separate. W-2 remains the retained manual-owner comparison.
