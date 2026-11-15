# Open questions

Questions not yet settled by an ADR, in the order we plan to answer them. Each answer becomes an ADR or an amendment, and its entry moves to "Answered". Numbers are stable.

| # | Question | Needed before |
| --- | --- | --- |
| 6 | How do Lean proofs attach to Ariadne code? **Deferred on 2026-11-15**; nothing in milestone 1 needs it. Options on the table: export code as terms of the mechanized core (deep embedding, smallest trusted base, laborious proofs); translate to native Lean functions (easy proofs, translator is trusted); both, linked by an agreement theorem. The export is part of the compiler in this repository under any option. | The Lean escape hatch being usable |
| 7 | Who writes the proofs that are not automatic: the model or a human? | The proof route for `idempotent` and other Lean obligations |
| 8 | Row-polymorphic records: add them? | Generic schema code |
| 9 | A sort for nonlinear arithmetic or units of measure? | Numerical code |
| 10 | Should `await` exist as optional sugar? | No deadline |
| 11 | Optional synchronous groups of machines? | Control and numerical code |
| 12 | Compile targets: native, WebAssembly, or both? | The optimizing compiler |
| 13 | Constrained decoding: grammar only, or types too? | Tuning the agent loop |
| 14 | Patterns backlog: sagas, deadline propagation, supervision, schema evolution, staleness and fencing, determinism boundaries | Each feature |
| 15 | Standard-library machines beyond `lift`, `>>>` and `|||` (retry, scatter-gather, routing): which ones, and how are they typed? The core combinators and their laws are settled by ADR-0018. | The standard library |
| 18 | System-wide properties over all replicas: quantified invariants, or composition from per-machine invariants and channel contracts? | Properties spanning many machines |
| 19 | Recognized machine kinds for further unbounded guarantees: replicated, monotone, topology restrictions, deterministic pipeline regions | Each kind |

To measure rather than decide: how much real handler code falls inside the automatic idempotence proof (ADR-0015).

## Answered

- 1. Effect types and capabilities: expressions are pure, machines are the only effect, channels are the capabilities (ADR-0016).
- 2. Multi-shot effect handlers: no longer arises (ADR-0016).
- 16. Liveness: deadlines with declared fault and scheduling budgets; true "eventually" deferred to finite models (ADR-0017).
- 17. Reference machines: used alongside "never" monitors, run as monitors, human-approved, optional per system (ADR-0017).
- 5. One-way channel send window: removed; one-way channels are always lossy, and `reject` needs a protocol (ADR-0021).
- 4. Storage contract: an append-only log per machine plus snapshots; a purpose-built engine possibly later (ADR-0019).
- 3. Spec layer: specs are written in Ariadne; invariants by default, native exploration as the fallback (ADR-0017).
- What success looks like for the first milestone: ADR-0011, ADR-0012.
- How far dependent types go, and which proof options go into the language: ADR-0010.
- Whether Mealy machines plus extensions are enough: ADR-0004.
- Whether `idempotent` can rest on simulation alone: no, proof required (ADR-0015).
- Whether there is a default between `durable` and `ephemeral`: no default, checker-enforced (ADR-0013).
