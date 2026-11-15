# Systems design patterns backlog

Reliability patterns Ariadne intends to own, so they stop being conventions. Recorded on 2026-11-15 so they are not forgotten. None has an ADR yet; each needs one before it is built.

## In the language or runtime (wanted)

| Pattern | How the language could own it | Where | Notes |
| --- | --- | --- | --- |
| Transactional outbox, exactly-once effects | A step returns state and outputs together, so the runtime persists both atomically | Runtime | Affects tickets 08 to 11; decide early |
| Backpressure and load shedding | Bounded mailboxes; the overflow policy (block, drop, reject with reply) is part of the channel type | Types | Affects tickets 08 to 11; decide early |
| Idempotency and safe retries | An at-least-once channel requires an idempotent handler or a dedup key; retry is only allowed on idempotent operations | Types | Affects tickets 08 to 11; decide early |
| Sagas and compensation | A compensable action returns a linear obligation that must be committed or compensated | Types (linear) | Builds on ticket 17 |
| Deadline propagation | Every request carries a deadline that children inherit; mandatory timeouts derive from it | Types | Builds on ticket 09 |
| Supervision | A child's failure is an event to its parent; restart policy is declared | Machines | Erlang-style |
| Schema evolution | Changing a state or message type requires a migration function and a compatibility check | Checker | Needed once snapshots exist |
| Staleness and fencing | Snapshot reads are typed as stale with a version; fencing tokens are monotonic indices | Types | Builds on ADR-0005 snapshots |
| Determinism boundaries | Clock and randomness are capabilities, so simulation controls them | Capabilities | Needs effect types and capabilities |
| Event sourcing and replay | A machine's state is a fold over its input log; the log is the trace | Runtime | Mostly falls out of ADR-0004 |
| Trace context | Propagated by the runtime on every message | Runtime | |

## Standard-library machines (wanted, later)

Each ships as a machine with a spec machine and simulation tests.

- Circuit breaker
- Retry with backoff and jitter
- Bulkhead (bounded pool of machines)
- Cache
- Rate limiter (the milestone 1 example, promoted)
- Leader election and consensus
- CRDTs, with their algebraic laws checked
