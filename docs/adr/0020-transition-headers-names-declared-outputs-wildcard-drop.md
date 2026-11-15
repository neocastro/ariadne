# ADR-0020: Transition headers: names, declared outputs, and a wildcard for `drop`

**Status:** Accepted  
**Date:** 2026-11-15  
**Deciders:** Yuri

## Context

A machine's header declares its transitions (ADR-0012). The header is what humans review and what diagrams are drawn from, so the question is how much a transition may say while every check on it stays cheap and local. Writing the example system for ticket #1 also showed that most rows of a realistic header are `drop`.

## Decision

A transition header stays a finite table. Three things may appear in a row:

```
Open on Acquire -> Open | Exhausted sends reply
Open on WindowEnd -> Open starts WindowEnd
Done on _ -> drop
```

- **Names (level 0).** A source state, an event, and the allowed target states. An arm may only go to a declared target. Checks are syntactic and graph-based: unreachable states, waiting states with no timer exit.
- **Declared outputs (level 1).** `sends` lists the channels the transition may send on; `starts` lists the timers it may start. An arm may emit only what its row declares. The check is syntactic, and it is what later makes "every request gets exactly one reply" checkable.
- **A wildcard, for `drop` only.** `State on _ -> drop` stands for every event that has no explicit row for that state. It can never lead to a state. The compiler expands it before any check; diagrams and header views show the expansion; when a newly added event falls into a wildcard, the checker reports it.

Deferred:

- **Guards (level 2)**, such as `Open on Acquire when tokens > 1 -> Open`, to be considered once refinements exist (ticket #18). Guards must stay in ADR-0010's decidable fragment; the solver would check that the guards for a pair cover every case and that each arm goes where its guard says.

Not in headers:

- **State updates (level 3)**, such as `with tokens' = tokens - 1`. A header that states updates is as large as the code. That role belongs to reference machines (ADR-0017).
- **Nested or parallel states.** Already excluded by ADR-0004.

## The rule that keeps checks easy

The control skeleton is finite and made of names only. Anything added to a row must be either a set of names (checked syntactically) or a predicate in the decidable fragment (checked by the solver, one arm at a time). No quantifiers, no recursion.

## Consequences

- Every check on a header is local to one arm or a walk over a finite graph.
- The wildcard is a second way to write `drop` rows. This is accepted because it only abbreviates, cannot change behaviour, and its expansion is always visible.
- The header remains suitable as input to an external model checker later (ADR-0017), since it is finite by construction.
