# ADR-0001: Build a new language backed by formal methods

**Status:** Accepted  
**Date:** 2026-11-15  
**Deciders:** Yuri

## Context

The goal is to push what tools for AI-written code look like: safety, correctness, verifiability. Verification can be layered onto an existing language or designed in.

## Decision

Design a new language whose semantics are formal from the start.

## Options considered

| Option | Trade-off |
| --- | --- |
| Verification layer on an existing language (Verus on Rust, Liquid Haskell) | Immediate ecosystem; inherits the host's semantic complexity and implicit authority |
| **New language (chosen)** | Full control over semantics, effects, tooling; no ecosystem, cold start for models |

## Consequences

Every tool must be built. A compact spec in context and a strict checker must compensate for little training data.
