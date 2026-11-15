# ADR-0003: Go-sized syntax, ML-strength semantics, core-first

**Status:** Accepted  
**Date:** 2026-11-15  
**Deciders:** Yuri

## Context

A small grammar with one way to do things (from Go) helps, but syntactic simplicity alone leaves `nil`, conventions and races. What helps reasoning is semantic simplicity.

## Decision

The language desugars to a small, adopted core calculus (call-by-value lambda calculus, algebraic data types, algebraic effects), mechanized in Lean with a soundness proof. A feature enters only if it desugars to the core or extends it with an updated proof. A reference interpreter is the executable semantics. Spec plus standard-library signatures must fit a small fraction of a model's context.

## Options considered

| Option | Trade-off |
| --- | --- |
| Go-style: small syntax, loose semantics | Easy to read; complexity pushed into every program |
| Haskell/Rust-style: rich features | Expressive; large semantic surface, hard interactions |
| **Small syntax, small strong core (chosen)** | Provable and predictable; fewer abstraction features |

## Consequences

Adding features is slow by design; runtime checks for defined behavior unless proofs remove them; diagnostics must map from core back to source.
