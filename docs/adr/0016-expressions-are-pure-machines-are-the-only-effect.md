# ADR-0016: Expressions are pure; machines are the only effect; channels are the capabilities

**Status:** Accepted  
**Date:** 2026-11-15  
**Deciders:** Yuri

## Context

Early notes assumed effect types in function signatures (`fetch ∷ Url → ⟨net, exn⟩ String`), and ADR-0003 named algebraic effects as part of the core. Later decisions changed the picture: effects already leave a machine only as outputs of a step (ADR-0004, ADR-0008), steps commit atomically (ADR-0013), and every safety argument so far assumes steps are pure functions.

## Decision

- **No expression performs an effect.** Functions compute values and nothing else. There are no effect rows, no effect handlers and no ambient I/O.
- **The only effect is a step's outputs.** `step ∷ s ⊸ i → (s, List o)` is the single place where anything reaches the outside.
- **Channels are the capabilities.** A machine can affect only what it holds an endpoint for. Endpoints are handed over at spawn or received in messages. Attenuation and revocation are proxy machines.
- **Real I/O lives in adapter machines at the edge** (network, disk, clock sources). Foreign code runs only there, or as explicitly trusted `foreign pure` functions.
- **Time and randomness arrive with the event.** The runtime stamps each input with a logical time and a seed. A step sees one instant.
- **Errors are values** (`Result`). Divergence is already excluded from steps (ADR-0007).
- **Logging and metrics inside a computation are returned as data** and emitted by the step. Exact replay of any step from its recorded input is the primary debugging tool.

## Options considered

| Option | Trade-off |
| --- | --- |
| A. Algebraic effects with handlers and effect rows (Koka) | Most expressive; a second control mechanism beside machines, a larger core and proof, and a clash between linear values and handlers |
| B. Capability values passed to functions, no effect rows | Simple types; functions still do I/O mid-step, which gives two ways to do I/O and contradicts ADR-0008 |
| **C. Pure expressions, machines as the only effect (chosen)** | Smallest core, exact simulation and replay, proofs only about pure functions; verbose for chatty I/O, and effectful abstractions must be machines |

## Consequences

- Amends ADR-0003: the core is call-by-value lambda calculus with algebraic data types and machines; algebraic effects are dropped.
- The question of multi-shot effect handlers no longer arises, nor does the conflict between linear values and handlers (ADR-0010).
- A library of pure functions provably cannot perform I/O. A library that ships machines reaches only what it is handed.
- The capability graph is the channel topology. Because endpoints can travel in messages, the static guarantee is a bound (the channel types a machine can ever hold); the exact graph comes from traces.
- Sequential I/O costs one waiting state per call. Batch requests and iterative machines are the patterns for chatty I/O.
- Abstractions that effect handlers would have carried (retry, scatter-gather, pipelines) become machine combinators. Their design is now a first-class task.
- Moving to option A later would be additive; the reverse would not. This is the reversible choice.

## Open questions

- The design and typing of machine combinators.
- Whether a propagation shorthand for `Result` is worth adding as pure sugar.
