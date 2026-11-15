# ADR-0019: Storage contract: an append-only log per machine, plus snapshots

**Status:** Accepted  
**Date:** 2026-11-15  
**Deciders:** Yuri

## Context

ADR-0013 commits each step of a durable machine as one record: the input consumed, the new state, and the outputs. The dedup window (ADR-0015) and live timers are part of the state, so that one record holds everything a recovery needs. The question is what the runtime requires from the store underneath. Milestone 1 keeps the log in memory.

## Decision

The runtime requires a minimal contract and nothing more:

```
append   ∷ MachineId → Seq → Record → Result ()       -- atomic; fails if Seq is not the next one
read     ∷ MachineId → Seq → Stream Record            -- records from a sequence number onward
truncate ∷ MachineId → Seq → Result ()                -- drop records before a snapshot
putSnap  ∷ MachineId → Seq → State → Result ()
getSnap  ∷ MachineId → Result (Option (Seq, State))
```

- **One log per machine**, addressed by a sequence number. An append is atomic and durable when it returns.
- **No multi-key transactions are required.** A step is one record.
- **Backends are pluggable** behind this contract. Order of implementation: the in-memory store of milestone 1, then a single-file write-ahead log.
- **Storage faults are simulable.** The simulator can implement the contract with injected torn writes, lost flushes and slow appends.
- **A purpose-built storage engine may come later** as one implementation of this contract. It is not ruled out and not planned.

## Options considered

| Option | Trade-off |
| --- | --- |
| **A. Append-only log per machine plus snapshots (chosen)** | Small contract to trust and to simulate; batching commits across machines must be built in the runtime above it |
| B. Transactional key-value store | Simpler recovery and batching; a much stronger requirement on the backend, harder to simulate faithfully |
| C. The runtime owns one purpose-built engine | Full control over determinism and performance; a storage engine is a project of its own |
| D. Defer | No work now; the durability design would stay vague |

## Consequences

- Group commit (batching several machines' appends into one durable write) is a runtime optimization that must keep each machine's append atomic.
- Replication and high availability are outside this contract and undecided.
- The contract is written in the notation of this ADR, not in Ariadne: the store is part of the runtime, below the language.
