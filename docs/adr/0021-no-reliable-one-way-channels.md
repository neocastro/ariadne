# ADR-0021: No reliable one-way channels

**Status:** Accepted  
**Date:** 2026-11-15  
**Deciders:** Yuri

## Context

ADR-0014 gives every machine a control queue whose size is derived from what can produce a control event. On a request-and-reply channel the bound is free: an endpoint awaiting a reply cannot send again. On a one-way `reject` channel there is no reply, so ADR-0014 proposed a `window k` in the type and left open how a slot in the window is released: by an explicit acceptance event, or by credits passed into the step.

## Decision

- **A one-way channel is always `lossy`**, with a drop policy (`drop_newest` or `drop_oldest`). It never rejects, so it produces no control events and needs no window.
- **A channel that is not `lossy` must carry a protocol** (ADR-0010) in which every send is followed by a reply, an acknowledgement or a rejection before the same endpoint may send again. `reject` is available only on such channels.
- **The `window k` tag is removed.**
- **Streaming with backpressure is a library protocol** in which the receiver grants credits. It is built from protocol automata, not from a core primitive (as ADR-0014 already said of credit-based flow control).

## Options considered

| Option | Trade-off |
| --- | --- |
| A. An acceptance event for every enqueued message | Fully static; doubles traffic on one-way channels and adds a notice every sender must handle |
| B. Credits passed into each step | No extra events; runtime bookkeeping enters step inputs and every one-way send needs a guard |
| **C. No reliable one-way channels (chosen)** | Removes a mechanism; fire-and-forget messages that matter must be modelled with an acknowledgement |

## Consequences

- Amends ADR-0014: the control queue's size is one slot per protocol endpoint awaiting an outcome, per live timer and per peer.
- The type says the truth: without an acknowledgement a sender cannot know that a one-way message arrived.
- Enforcement needs protocol automata, which arrive with ticket #20. Until then the rule holds by construction in the example system, where every `reject` channel is used for request and reply.
