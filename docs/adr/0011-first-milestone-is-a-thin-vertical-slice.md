# ADR-0011: First milestone is a thin vertical slice

**Status:** Accepted  
**Date:** 2026-11-15  
**Deciders:** Yuri

## Context

Success is not yet defined; the novel claim is verifiability with agents, which needs every layer working at least minimally.

## Decision

One program (a rate-limited API with per-request machines, a limiter, timers and a fake database) through every layer: Lean-mechanized core with memory constraints; Rust reference interpreter with reference counting; checker (inference, Z3 refinement fragment, exhaustiveness, timeouts, step termination); fault-injecting simulation; visualizer with trace replay; agent loop writing and fixing step functions. Deferred: optimizing compiler, Perceus optimizations, FFI, standard library.

## Consequences

Breadth before depth; each layer is minimal and will be revisited. The demo shows bugs found and fixed with no human reading code.
