# ADR-0015: Idempotency: duplicates in the channel type, retries only where safe

**Status:** Proposed  
**Date:** 2026-11-15  
**Deciders:** Yuri

## Context

Outputs are dispatched at least once (ADR-0013), and a sender that times out cannot know whether its message arrived. Retrying is only safe when a duplicate does no harm. Today that is a convention: handlers are hoped to be idempotent and retries are added by hand.

## Decision

- **Possible duplication is a delivery tag.** Alongside `lossy` and `unordered`, a channel may be tagged `duplicates`. A channel without that tag never delivers the same message ID twice; across a network the runtime implements this as at-least-once delivery plus deduplication.
- **A receiver on a `duplicates` channel must be safe against duplicates**, in one of two declared ways:
  - **`idempotent` handler:** the handler for that event is declared idempotent, meaning that handling the same message twice leaves the same state and has no further observable effect.
  - **`dedup` window:** the channel declares a deduplication window (a count or a time). The runtime keeps seen message IDs in the receiver's durable state and discards repeats.
- **`idempotent` is checked by simulation, not trusted.** `ari sim` injects duplicates on `duplicates` channels and attaches a generated monitor that compares state and outputs with and without the duplicate. A proof is possible later through the Lean escape hatch (ADR-0010).
- **`resend` is the retry primitive.** It re-emits an earlier output with the same message ID. It is only allowed when the target is duplicate-safe: the channel deduplicates or the handler is idempotent. Emitting a fresh message after a timeout is still possible, but it has a new ID and is a new request by definition.
- **External effects take the message ID as an idempotency key** (ADR-0013 adapters).
- **Retry policies are library machines**: backoff, jitter and attempt limits are built on `resend` and timers.

```
Chan ⟨cap 16, lossy, duplicates, dedup 1024, reject⟩ Charge
```

## Options considered

| Option | Trade-off |
| --- | --- |
| Convention, as in mainstream languages | No machinery; duplicate bugs found in production |
| Runtime deduplicates everything, always | Simple model; unbounded dedup state, and impossible for external systems |
| **Duplication typed; receiver declares idempotent or dedup; retry gated (chosen)** | Duplicate safety is visible and tested; more declarations per channel |

## Consequences

- Simulation gains a duplicate-injection fault, allowed only where the type says duplicates can happen.
- A dedup window is a correctness parameter: a duplicate arriving after the window slips through. Simulation should include late duplicates.
- "Exactly-once" is stated honestly: exactly-once state transitions (ADR-0013), effectively-once delivery inside the dedup window, at-least-once toward the outside world with an idempotency key.

## Open questions

- Is an observational check in simulation a strong enough meaning for `idempotent`, or should some handlers require a proof?
- Should the dedup window be a count, a time, or both?
