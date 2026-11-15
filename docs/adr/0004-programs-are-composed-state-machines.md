# ADR-0004: Programs are composed state machines

**Status:** Accepted  
**Date:** 2026-11-15  
**Deciders:** Yuri

## Context

State machines are well understood and verifiable (TLA+, Event-B, P), but they describe control and concurrency, not data and computation. Replacing the calculus with them is not possible; using them as the architecture is.

## Decision

Two levels in one language: the core calculus computes values; machines structure programs. A machine is an ordinary value, a Mealy machine:

```
Machine i o = ∃s. (s, s → i → (s, List o))
lift  ∷ (a → b) → Machine a b
(>>>) ∷ Machine a b → Machine b c → Machine a c
(|||) ∷ Machine a b → Machine c d → Machine (a + c) (b + d)
loop  ∷ Machine (a + c) (b + c) → Machine a b
```

A pure function is a one-state machine. Composition is the only structuring mechanism. Extensions: dynamic spawning with channels as values; timers as an output plus an input event; spec machines as relations `s → i → Set (s, List o)` refined by implementations; state snapshots for durability. Hierarchy is a library pattern (sub-machines held as state data), not built-in statecharts.

## Options considered

| Option | Trade-off |
| --- | --- |
| Plain functional language, no machine layer | Simplest core; system structure invisible to tools |
| Built-in statecharts | Familiar; many incompatible semantics, large core |
| **Machines as values plus composition (chosen)** | Diagrams, model checking and simulation for free; machine semantics to design carefully |

## Consequences

Visualization and trace replay come from the compiler; spec and program share a shape; compilers and numerical code live mostly in pure functions with thin machine layers.
