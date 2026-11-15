# ADR-0013: Atomic step commit: the outbox is the runtime

**Status:** Proposed  
**Date:** 2026-11-15  
**Deciders:** Yuri

## Context

A step returns its next state and its outputs together (`step ∷ s ⊸ i → (s, List o)`, ADR-0004, ADR-0006). If a runtime applies the state and sends the outputs as two separate actions, a crash between them either loses outputs or, after a retry, sends them twice. Mainstream systems fix this by convention with the transactional outbox pattern. Here the language already has the right shape to make it automatic.

## Decision

- **A step commits as one record.** For a durable machine the runtime appends one atomic record per step to that machine's log: the input consumed, the new state (or a delta), and the outputs. Nothing is visible outside the machine until the record is committed.
- **Outputs are dispatched after commit**, by the runtime, at least once. After a crash, committed but undispatched outputs are sent again.
- **Every output has a deterministic message ID**: (machine ID, step sequence number, output index). A re-sent output carries the same ID. Deduplication and idempotency (ADR-0015) build on it.
- **Recovery is replay.** A machine restarts from its last snapshot plus its log. Snapshots (ADR-0004) are log compaction.
- **Durability is declared per machine**: `durable` or `ephemeral`. An ephemeral machine keeps no log and dies with its process; its parent learns of the loss as an event.
- **Effects on the outside world go through adapters** that receive the message ID as an idempotency key. The runtime cannot make an external system exactly-once; it can only make the retry safe to recognize.
- **No cross-machine transactions.** There is no two-phase commit between machines; multi-machine consistency is built from messages (sagas, protocols).

## Options considered

| Option | Trade-off |
| --- | --- |
| Apply state, then send outputs, separately | Simplest runtime; lost or duplicated effects on a crash |
| **One atomic record per step, dispatch after commit (chosen)** | Exactly-once state transitions and at-least-once outputs by construction; a storage write per step |
| Distributed transactions across machines | Strongest guarantee; couples machines, blocks under failure, breaks ADR-0005's independence |

## Consequences

- The trace (`ariadne.trace/1`) and the durable log are the same data at two retention levels.
- A new fault class becomes simulable: crash after commit and before dispatch, and crash before commit.
- A durable step costs a storage write. Batching several machines' commits is a runtime optimization that must preserve per-machine atomicity.
- Milestone 1 keeps the log in memory but uses the same commit-then-dispatch semantics and message IDs, so nothing changes shape later.

## Open questions

- The storage interface: what the runtime requires from a log store.
- Whether per-request machines default to `ephemeral`.
