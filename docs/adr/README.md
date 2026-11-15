# Architecture decision records

One file per decision. Accepted means decided; Proposed means recommended, awaiting a decision. Supersede a decision with a new ADR rather than rewriting an accepted one.

| ADR | Decision | Status |
| --- | --- | --- |
| [0001](0001-build-a-new-language-backed-by-formal-methods.md) | Build a new language backed by formal methods | Accepted |
| [0002](0002-agents-write-the-code-explicit-beats-sugar.md) | Agents write the code; explicit beats sugar | Accepted |
| [0003](0003-go-sized-syntax-ml-strength-semantics-core-first.md) | Go-sized syntax, ML-strength semantics, core-first | Accepted |
| [0004](0004-programs-are-composed-state-machines.md) | Programs are composed state machines | Accepted |
| [0005](0005-no-shared-mutable-state.md) | No shared mutable state | Accepted |
| [0006](0006-gc-free-memory-constraints-in-the-core-reference-counting-in.md) | GC-free memory constraints in the core; reference-counting interpreter first | Accepted |
| [0007](0007-total-functions-by-default-no-cyclic-data-id-indexed-graphs.md) | Total functions by default; no cyclic data; ID-indexed graphs first | Accepted |
| [0008](0008-waiting-is-explicit-states-no-await-in-the-core.md) | Waiting is explicit states; no `await` in the core | Accepted |
| [0009](0009-run-to-completion-steps-over-session-typed-async-channels.md) | Run-to-completion steps over session-typed async channels | Accepted |
| [0010](0010-one-refinement-mechanism-in-a-decidable-fragment.md) | One refinement mechanism in a decidable fragment; Lean as the escape hatch | Accepted |
| [0011](0011-first-milestone-is-a-thin-vertical-slice.md) | First milestone is a thin vertical slice | Accepted |
| [0012](0012-milestone-1-scope-revised-after-review.md) | Milestone 1 scope revised after adversarial review | Accepted |
| [0013](0013-atomic-step-commit-the-outbox-is-the-runtime.md) | Atomic step commit: the outbox is the runtime | Accepted |
| [0014](0014-backpressure-bounded-mailboxes-overflow-policy-in-the-channel-type.md) | Backpressure: bounded mailboxes, overflow policy in the channel type | Accepted |
| [0015](0015-idempotency-duplicates-in-the-channel-type-retries-only-where-safe.md) | Idempotency: duplicates in the channel type, retries only where safe | Accepted |
| [0016](0016-expressions-are-pure-machines-are-the-only-effect.md) | Expressions are pure; machines are the only effect; channels are the capabilities | Accepted |
| [0017](0017-specs-in-ariadne-invariants-by-default-exploration-as-fallback.md) | Specs are written in Ariadne; invariants by default, exploration as the fallback | Accepted |
| [0018](0018-machine-combinators-are-fused-and-lawful-no-loop.md) | Machine combinators are fused and lawful; `loop` is removed | Accepted |
