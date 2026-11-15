# ADR-0018: Machine combinators are fused and lawful; `loop` is removed

**Status:** Accepted  
**Date:** 2026-11-15  
**Deciders:** Yuri

## Context

ADR-0004 introduced four combinators: `lift`, `>>>`, `|||` and `loop`. A review from the viewpoint of category theory found three things.

- `loop ∷ Machine (a + c) (b + c) → Machine a b` feeds outputs back as inputs within one step. Feedback over a sum type is iteration, `iter ∷ (x → y + x) → x → y`, which is not total. That contradicts "every step terminates" (ADR-0007).
- The remaining combinators satisfy the laws of a category with a coproduct-like parallel composition, but only if a combined machine is one machine with one commit. A forwarder built from two machines and a channel adds a buffer and a fault surface, so the identity law fails for it.
- `lift ∷ (a → b) → Machine a b` cannot express filtering or fan-out.

## Decision

- **`loop` is removed.** Feedback is a machine sending to its own inbox: one step per message, bounded by the channel's capacity. If a synchronous feedback combinator is needed later, it will be reconsidered with a decreasing measure.
- **Combinators are fused.** A machine built with combinators is a single machine: one state, one step, one atomic commit (ADR-0013). Connecting separately spawned machines through channels is a different kind of composition, with no identity law.
- **`lift` takes a function to a list**, so that filtering and fan-out are lifts:

```
lift  ∷ (a → List b) → Machine a b
(>>>) ∷ Machine a b → Machine b c → Machine a c
(|||) ∷ Machine a b → Machine c d → Machine (a + c) (b + d)
```

- **The laws are named obligations.** Each is proved once in Lean for the core and run as a conformance test with `ari explore`:

```
lift pure >>> m  ≈  m  ≈  m >>> lift pure                     -- identity; pure x = [x]
(m >>> n) >>> p  ≈  m >>> (n >>> p)                            -- associativity
lift f >>> lift g  ≈  lift (f >=> g)                           -- fusion of lifts
(m ||| n) >>> (p ||| q)  ≈  (m >>> p) ||| (n >>> q)            -- interchange
lift f ||| lift g  ≈  lift (f ⊕ g)                             -- parallel lifts
```

  Here `f >=> g` applies `g` to each output of `f` and concatenates, and `f ⊕ g` applies `f` to left inputs and `g` to right inputs.
- **`≈` is behavioural equivalence (bisimilarity), not equality.** `lift pure >>> m` has state `(Unit, s)`, not `s`. Two machines are equivalent when a simulation relation holds in both directions (ADR-0017).
- **No product parallelism.** There is no combinator that waits for two inputs to arrive together; asynchronous events never do.
- **No abstraction hierarchy is exposed.** There is exactly one `Machine` type, so the laws need no typeclasses or higher-kinded types.

## Options considered

| Option | Trade-off |
| --- | --- |
| Combinators as sugar for spawned machines and channels | Uniform with the rest of the runtime; the laws fail, so nothing can be simplified or proved from them |
| **Combinators as fusion into one machine (chosen)** | Laws hold and are checkable; a fused machine cannot be distributed or fail in parts |
| Keep `loop` with a decreasing measure | Synchronous feedback stays available; one more proof obligation and a second way to get feedback |
| **Remove `loop` (chosen)** | One way to get feedback, and totality is preserved; self-messaging costs a step per round |

## Consequences

- Amends ADR-0004: its combinator list is replaced by the one above.
- The laws justify compiler simplifications later (fusing chains of lifts, canonical forms for diagrams), but they are tests and proofs first.
- Partly answers open question 15. Still open: which further standard-library machines exist (retry, scatter-gather, routing) and how they are typed.
