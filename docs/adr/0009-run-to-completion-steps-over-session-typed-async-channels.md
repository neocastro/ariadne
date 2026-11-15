# ADR-0009: Run-to-completion steps over session-typed async channels

**Status:** Accepted  
**Date:** 2026-11-15  
**Deciders:** Yuri

## Context

How machines communicate decides what is provable and how big the state space gets.

## Decision

Each step runs to completion. Machines talk over typed asynchronous channels whose protocols are session types, with delivery guarantees in the type (`Chan ⟨reliable, fifo⟩ Msg` vs `Chan ⟨lossy⟩ Msg`). The simulation harness injects exactly the faults each type allows. Verification is per machine against its channel protocols (assume-guarantee).

## Options considered

| Option | Trade-off |
| --- | --- |
| Synchronous (Esterel, Lustre) | Deterministic, verifiable; doesn't model networks |
| Untyped async mailboxes (Erlang) | Realistic; interleavings explode |
| **Async with session types and typed guarantees (chosen)** | Realistic and checkable per component; more type machinery |

## Consequences

Faults in simulation match reality as declared. Open: optional synchronous groups for control and numerical code.
