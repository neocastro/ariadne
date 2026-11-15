# ADR-0007: Total functions by default; no cyclic data; ID-indexed graphs first

**Status:** Accepted  
**Date:** 2026-11-15  
**Deciders:** Yuri

## Context

Recursive functions raise termination questions; recursive values (cycles) defeat reference counting.

## Decision

Recursive functions are allowed and total by default: structural recursion, decreasing measures checked by SMT, explicit `Fuel`, or a `div` effect in the signature. Step functions may not carry `div`; unbounded behavior comes from machines receiving events. Cyclic data is not allowed: graphs are ID-indexed maps with refinement types guaranteeing IDs are present; zippers replace parent pointers; infinite structures are unfolds. A region-backed graph type is added only if the demo or a benchmark shows the need.

## Consequences

Graph-heavy code is more verbose (acceptable per ADR-0002); every step provably terminates; long computations become observable, cancellable machines.
