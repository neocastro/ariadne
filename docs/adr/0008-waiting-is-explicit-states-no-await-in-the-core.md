# ADR-0008: Waiting is explicit states; no `await` in the core

**Status:** Accepted  
**Date:** 2026-11-15  
**Deciders:** Yuri

## Context

Effects leave machines only as outputs, so a handler that needs a reply must wait between steps. That can be written by hand or generated from `await`.

## Decision

Every waiting point is an explicit state in the source. A request is an output; its reply is an input event. Each state carries a typed record of exactly its context; every (state, event) pair is handled or explicitly dropped; every waiting state has a timeout; concurrent requests are child machines; mailboxes are bounded in the channel type. Straight-line reading is a rendered view, not syntax.

## Options considered

| Option | Trade-off |
| --- | --- |
| `await` desugared into generated states | Concise; generated states must map diagnostics back to source |
| **Explicit states (chosen)** | Everything checkable and visible; verbose, which ADR-0002 accepts |

## Consequences

Most async bugs (late replies, cancellation, hangs, lost context) become compile-time errors. Open: whether `await` should exist even as sugar.
