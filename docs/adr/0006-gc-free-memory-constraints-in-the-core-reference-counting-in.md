# ADR-0006: GC-free memory constraints in the core; reference-counting interpreter first

**Status:** Accepted  
**Date:** 2026-11-15  
**Deciders:** Yuri

## Context

The memory model constrains semantics, so retrofitting it later could break programs. Its optimized implementation is not the project's novel part.

## Decision

Fix now: strict evaluation, no cyclic data, linear resource handles, linear machine state (`step ∷ s ⊸ i → (s, List o)`, guaranteeing in-place state updates). The first interpreter uses plain reference counting. Defer Perceus-style elision and reuse, atomic counts across threads, and performance work.

## Options considered

| Option | Trade-off |
| --- | --- |
| Tracing GC now, decide later | Fastest start; later constraints may break code |
| Full Perceus implementation first | Complete; delays the novel demo |
| **Constraints now, simple RC now, optimizations later (chosen)** | Semantics settled early; performance deferred |

## Consequences

The Lean soundness proof covers the memory constraints from the start; "no GC, no leaks" is real on the demo program.

## Amendments

- ADR-0012: the Lean proof is staged (pure core first, machines and linearity later) rather than covering the memory constraints from the start.
