# ADR-0014: Backpressure: bounded mailboxes, overflow policy in the channel type

**Status:** Proposed  
**Date:** 2026-11-15  
**Deciders:** Yuri

## Context

Mailboxes are bounded and the bound is in the channel type (ADR-0008). What happens when a mailbox is full is not yet defined. Unbounded queues hide overload until memory runs out; blocking sends cause deadlocks and do not fit run-to-completion steps (ADR-0009), because a step cannot pause halfway.

## Decision

- **No unbounded channels and no blocking sends.** A send is an output of a step; its outcome, when it matters, comes back as an input event.
- **The overflow policy is part of the channel type**, next to capacity and delivery tags:

```
Chan ⟨cap 64, reject⟩ Msg            -- sender is told
Chan ⟨cap 64, lossy, dropNewest⟩ Msg  -- the new message is discarded
Chan ⟨cap 64, lossy, dropOldest⟩ Msg  -- the oldest queued message is discarded
```

- **`reject` is the only policy allowed on a channel that is not `lossy`.** The sender receives a `Rejected msg` event carrying the message back. The existing rule that every (state, event) pair is handled or explicitly dropped (ADR-0008) forces the sender to decide what overload means: retry later, shed, or fail its own caller.
- **`dropNewest` and `dropOldest` require the `lossy` tag**, so silent loss is always visible in the type.
- **System boundaries declare a policy too.** An ingress channel from the outside world has a capacity and a policy like any other; this is where load shedding lives.
- **Credit-based flow control is a library protocol**, written with protocol automata (ADR-0010) where the receiver grants credits. It is not a core primitive.
- **Simulation exercises overflow.** `ari sim` can run with reduced capacities so overflow paths are tested, and reports channels whose overflow path was never taken.

## Options considered

| Option | Trade-off |
| --- | --- |
| Unbounded mailboxes (Erlang default) | Never rejects; overload shows up as latency and memory exhaustion |
| Blocking sends on bounded channels (Go) | Natural backpressure; deadlocks, and incompatible with run-to-completion steps |
| **Bounded, non-blocking, policy in the type (chosen)** | Overload is explicit and checked; every sender on a reliable channel must handle rejection |
| Credit-based flow control as the only mechanism | Principled; heavy for simple request and reply |

## Consequences

- No deadlock can arise from full mailboxes.
- Code gets more verbose (acceptable per ADR-0002): every reliable send has an overload path.
- Capacity numbers become part of interfaces and need tuning; simulation and metrics must make them observable.

## Open questions

- Delivery of `Rejected` events and timer firings must not itself be rejectable. Proposed: reserved capacity, bounded by the machine's outstanding sends and timers. Needs a precise rule.
- Whether capacity is a literal or may be an index refined elsewhere.
