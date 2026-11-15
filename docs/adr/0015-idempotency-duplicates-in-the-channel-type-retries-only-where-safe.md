# ADR-0015: Idempotency: duplicates in the channel type, retries only where safe

**Status:** Accepted  
**Date:** 2026-11-15  
**Deciders:** Yuri

## Context

Outputs are dispatched at least once (ADR-0013), and a sender that times out cannot know whether its message arrived. Retrying is only safe when a duplicate does no harm. Today that is a convention: handlers are hoped to be idempotent and retries are added by hand.

## Decision

- **Possible duplication is a delivery tag.** Alongside `lossy` and `unordered`, a channel may be tagged `duplicates`. A channel without that tag never delivers the same message ID twice; across a network the runtime implements this as at-least-once delivery plus deduplication.
- **A receiver on a `duplicates` channel must be safe against duplicates**, in one of two declared ways:
  - **`idempotent` handler:** the handler for that event is declared idempotent, meaning that handling the same message twice leaves the same state and has no further observable effect.
  - **`dedup` window:** the channel declares a deduplication window, as a count of message IDs. The runtime keeps seen message IDs in the receiver's durable state and discards repeats.
- **`idempotent` requires a proof.** The obligation, for the handler of event `e`: handling `e` a second time changes nothing.

```
∀ s e.  let (s₁, o₁) = step s e
            (s₂, o₂) = step s₁ e
        in  s₂ = s₁  ∧  o₂ ⊆ resends of o₁
```

  It is discharged in one of two ways:
  - **Automatically**, by composing the handler with itself and sending the result to the budgeted solver, when the handler stays inside the decidable fragment of ADR-0010.
  - **In Lean**, against the mechanized core, when it does not.

  A handler with no proof cannot be declared `idempotent`; its channel must use a `dedup` window instead. Deduplication is implemented once in the runtime and is part of the trusted base.
- **Simulation is the fast counterexample finder, not the guarantee.** `ari sim` injects duplicates on `duplicates` channels, which exercises dedup windows and finds failing cases before a proof is attempted.
- **Until the proof route exists, `idempotent` is unavailable** and every `duplicates` channel uses `dedup`. This is the state of milestone 1.
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

- Decided 2026-11-15: a simulation check is not enough; `idempotent` requires a proof.
- How much of real handler code falls inside the automatic route, and how the self-composed obligation is reported back as a counterexample.
- Decided 2026-11-15: the dedup window is a count of message IDs for now; a time-based window can be added later.
