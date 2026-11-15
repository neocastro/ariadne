# Open questions

Questions not yet settled by an ADR, in the order we plan to answer them. Each answer becomes an ADR or an amendment, and its entry moves to the bottom.

| # | Question | Needed before |
| --- | --- | --- |
| 1 | Effect types and capabilities: what is the design? | Anything after milestone 1 |
| 2 | Are multi-shot effect handlers needed? | The effect system (depends on 1) |
| 3 | Is the spec layer part of the language or a separate one? | Model checking |
| 4 | What does the runtime require from a durable log store? | Real durability |
| 5 | How is a one-way channel's send window released: an acceptance event, or credits passed into the step? | One-way `reject` channels |
| 6 | How do Lean proofs attach to Ariadne code, and who maintains the core-to-Lean export? | The Lean escape hatch being usable |
| 7 | Who writes the proofs that are not automatic: the model or a human? | The proof route for `idempotent` and other Lean obligations |
| 8 | Row-polymorphic records: add them? | Generic schema code |
| 9 | A sort for nonlinear arithmetic or units of measure? | Numerical code |
| 10 | Should `await` exist as optional sugar? | No deadline |
| 11 | Optional synchronous groups of machines? | Control and numerical code |
| 12 | Compile targets: native, WebAssembly, or both? | The optimizing compiler |
| 13 | Constrained decoding: grammar only, or types too? | Tuning the agent loop |
| 14 | Patterns backlog: sagas, deadline propagation, supervision, schema evolution, staleness and fencing, determinism boundaries | Each feature |

To measure rather than decide: how much real handler code falls inside the automatic idempotence proof (ADR-0015).

## Answered

- What success looks like for the first milestone: ADR-0011, ADR-0012.
- How far dependent types go: ADR-0010.
- Which proof options go into the language: ADR-0010.
- Whether Mealy machines plus extensions are enough: ADR-0004.
- Whether `idempotent` can rest on simulation alone: no, proof required (ADR-0015).
- Whether there is a default between `durable` and `ephemeral`: no default, checker-enforced (ADR-0013).
