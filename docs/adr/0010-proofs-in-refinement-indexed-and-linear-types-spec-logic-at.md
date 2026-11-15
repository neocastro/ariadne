# ADR-0010: Proofs in refinement, indexed and linear types; spec logic at the spec layer

**Status:** Proposed  
**Date:** 2026-11-15  
**Deciders:** Yuri

## Context

Full dependent types maximize expressiveness but reintroduce the complexity ADR-0003 removes. Real programs mostly need bounds, invariants, protocols and system properties.

## Decision

In the language: refinement types checked by SMT, indexed types over simple sorts (naturals, booleans, enums), linear types. At the spec layer: a specification logic with model checking for concurrency and system properties. Types derived from schemas come from build-time generation, not dependent types.

## Options considered

| Option | Trade-off |
| --- | --- |
| Full dependent types (Lean, Idris) | States anything; manual proofs, complex core |
| Refinement types only | Automatic; no typestate without linearity |
| **Refinement + indexed + linear, spec logic above (proposed)** | Covers production bug classes with automatic proofs; no everyday full-correctness proofs |

## Consequences

SMT proof brittleness must be managed (pinned solver, small contexts, time budgets). Supersedes the original "dependently typed" framing of Ariadne if accepted.
