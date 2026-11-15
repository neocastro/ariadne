# ADR-0013: Atomic step commit: the outbox is the runtime

**Status:** Accepted  
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

## How `ephemeral` interacts with the other guarantees

An ephemeral machine can vanish with everything it holds. Each guarantee needs a rule for that:

| Guarantee | What a vanishing machine breaks | Rule that restores it |
| --- | --- | --- |
| Linear values (ADR-0006, ADR-0010) | Handles and obligations it held are dropped, never used | Loss is an event to the durable parent, which holds or re-acquires the resource; an ephemeral machine may not be the sole owner of a saga obligation |
| Delivery guarantees (ADR-0009) | A message it consumed but did not finish is lost, so delivery to it is at most once | A channel into an ephemeral machine must be tagged `lossy`, or the sender must handle a `PeerLost` event |
| Deduplication (ADR-0015) | Its dedup window is gone | A `duplicates` channel into an ephemeral machine needs a proved `idempotent` handler |
| Protocol typestate (ADR-0010) | The peer is stuck mid-protocol | Every protocol state has a `PeerLost` transition when the peer is ephemeral |
| Atomic outputs (this ADR) | It may crash after sending only some of a step's outputs | Receivers of an ephemeral machine's outputs see a prefix; the type of its channels says so |
| Replay and post-mortem | No log to replay | Tracing is optional and best-effort for ephemeral machines |

Mandatory timeouts (ADR-0008), "check one representative machine" (ADR-0005) and simulation are unaffected; simulation gains a crash fault that loses ephemeral state and recovers durable state.

Agreed direction (2026-11-15): there is no default. Every machine declares `durable` or `ephemeral` (ADR-0002), and the checker rejects `ephemeral` wherever the rules above are not met.

## Open questions

- The storage interface: what the runtime requires from a log store.
- The precise checker rules for `ephemeral`, to be written when the storage interface is designed. Nothing in milestone 1 depends on them: the log is in memory and every machine behaves the same way.
