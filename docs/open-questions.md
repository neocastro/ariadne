# Open questions

Each open question is a GitHub issue labelled `decision`. The issue states why it matters, the options with their trade-offs, and a suggested pick. Answer by commenting with an option letter; the answer is then recorded as an ADR and the issue is closed. This file is the index.

Questions S1 to S6 came from the syntax draft (pull request #30). Numbers 6 to 19 are the original open questions; their numbers are stable.

| # | Question | Issue | Blocks |
| --- | --- | --- | --- |
| S1 | How does a machine receive replies? | [#31](https://github.com/neocastro/ariadne/issues/31) | Blocks #8 |
| S2 | How is the `Rejected` control event declared? | [#32](https://github.com/neocastro/ariadne/issues/32) | Blocks #8 |
| S3 | How is a system wired together? | [#33](https://github.com/neocastro/ariadne/issues/33) | Blocks #8 and #12 |
| S4 | What may a monitor observe? | [#34](https://github.com/neocastro/ariadne/issues/34) | Blocks #10 |
| S5 | Should there be type aliases? | [#35](https://github.com/neocastro/ariadne/issues/35) | Nothing |
| S6 | Should a state be updatable without rebuilding it field by field? | [#36](https://github.com/neocastro/ariadne/issues/36) | Nothing |
| 9 | A sort for nonlinear arithmetic or units of measure? | [#37](https://github.com/neocastro/ariadne/issues/37) | Nothing in milestone 1 |
| 10 | Should `await` exist as optional sugar? | [#38](https://github.com/neocastro/ariadne/issues/38) | Nothing in milestone 1 |
| 11 | Optional synchronous groups of machines? | [#39](https://github.com/neocastro/ariadne/issues/39) | Nothing in milestone 1 |
| 12 | Compile targets: native, WebAssembly, or both? | [#40](https://github.com/neocastro/ariadne/issues/40) | Nothing in milestone 1 |
| 13 | Constrained decoding: grammar only, or types too? | [#41](https://github.com/neocastro/ariadne/issues/41) | Nothing in milestone 1 |
| 14 | Patterns backlog: what comes after milestone 1, and in what order? | [#42](https://github.com/neocastro/ariadne/issues/42) | Nothing in milestone 1 |
| 15 | Which standard-library machines exist beyond the core combinators? | [#43](https://github.com/neocastro/ariadne/issues/43) | Nothing in milestone 1 |
| 18 | How are system-wide properties over many machines established? | [#46](https://github.com/neocastro/ariadne/issues/46) | Nothing in milestone 1 |
| 19 | Which machine kinds, if any, unlock further unbounded guarantees? | [#47](https://github.com/neocastro/ariadne/issues/47) | Nothing in milestone 1 |
| 6 | How do Lean proofs attach to Ariadne code? (deferred) | [#44](https://github.com/neocastro/ariadne/issues/44) | Nothing in milestone 1 |
| 7 | Who writes the proofs that are not automatic? (deferred) | [#45](https://github.com/neocastro/ariadne/issues/45) | Nothing in milestone 1 |

To measure rather than decide: how much real handler code falls inside the automatic idempotence proof (ADR-0015).

## Note on Petri nets (corrected 2026-11-15)

An earlier note here said that the header skeleton of replicated machines "is a Petri net", so safety for any number of instances is a coverability question and place invariants are candidate inductive invariants. An adversarial review found that overstated. The corrected statement:

- A net built from machine headers is a sound over-approximation of the system. A safe verdict transfers to the real system; an unsafe verdict may be spurious and must be replayed concretely.
- Headers alone do not determine branches that depend on a payload or on data, so for the rate limiter the header net proves nothing useful until transitions carry guards (ADR-0020, deferred).
- A place invariant ranges over global counts of machines, not over one machine's state, so it is not directly the per-machine invariant of ADR-0017.
- The rate limiter's property is better stated as a single-machine invariant with ghost state plus channel contracts (see issue #46).

Details and the conditions for a possible `replicated` machine kind are in issue #47.

## Answered

- 1. Effect types and capabilities: expressions are pure, machines are the only effect, channels are the capabilities (ADR-0016).
- 2. Multi-shot effect handlers: no longer arises (ADR-0016).
- 16. Liveness: deadlines with declared fault and scheduling budgets; true "eventually" deferred to finite models (ADR-0017).
- 17. Reference machines: used alongside "never" monitors, run as monitors, human-approved, optional per system (ADR-0017).
- 8. Row-polymorphic records: not adding. Records stay nominal and generic schema code comes from build-time generation (ADR-0010). Revisit on evidence from real programs.
- 5. One-way channel send window: removed; one-way channels are always lossy, and `reject` needs a protocol (ADR-0021).
- 4. Storage contract: an append-only log per machine plus snapshots; a purpose-built engine possibly later (ADR-0019).
- 3. Spec layer: specs are written in Ariadne; invariants by default, native exploration as the fallback (ADR-0017).
- What success looks like for the first milestone: ADR-0011, ADR-0012.
- How far dependent types go, and which proof options go into the language: ADR-0010.
- Whether Mealy machines plus extensions are enough: ADR-0004.
- Whether `idempotent` can rest on simulation alone: no, proof required (ADR-0015).
- Whether there is a default between `durable` and `ephemeral`: no default, checker-enforced (ADR-0013).
