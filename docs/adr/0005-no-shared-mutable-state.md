# ADR-0005: No shared mutable state

**Status:** Accepted  
**Date:** 2026-11-15  
**Deciders:** Yuri

## Context

One machine per request means unbounded identical machines. Checking one representative is sound only if they never share mutable state.

## Decision

Machines never share mutable state. Caches, rate limiters, pools and databases are machines reached by messages. Immutable values are shared freely.

## Consequences

Data-race freedom by construction; deterministic simulation stays possible. Hot spots need sharding (a router over shard machines) or published immutable snapshots. Transactions become a session-typed protocol.
