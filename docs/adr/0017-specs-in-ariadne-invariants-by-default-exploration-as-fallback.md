# ADR-0017: Specs are written in Ariadne; invariants by default, exploration as the fallback

**Status:** Accepted  
**Date:** 2026-11-15  
**Deciders:** Yuri

## Context

A spec states invariants, allowed behaviours and, eventually, liveness. Milestone 1 writes invariants as monitor machines checked in simulation (ADR-0012). Three options were first considered: specs in Ariadne with its own model checker, a separate spec language, or Ariadne specs translated to an external model checker. An adversarial review found that the translation option has no sound source for its "abstracted implementation", does not deliver liveness, and adds a large unchecked translation; it also surfaced options that use the language's own runtime and solver.

Because agents write the code, two things that were expensive for people are cheap here: inventing inductive invariants (a search with an exact, automatic check) and following restrictive coding styles.

## Decision

**Specs are written in Ariadne, and checked by Ariadne's own runtime and solver.**

- **Monitors are the single specification mechanism.** A monitor observes the trace and can enter a violation state. It cannot send to, or hold endpoints of, the system it observes.
- **Spec machines use an explicit choice input** instead of returning sets, so they stay executable, enumerable and inside the mechanized core:

```
specStep ∷ s → i → Choice → (s, List o)     -- Choice is finite
```

- **Spec code is a declaration mode.** Spec machines and monitors cannot be spawned by, or leak into, executable code.

**Invariants by default.**

- Every machine states an inductive invariant, written by the agent and checked by the budgeted solver (ADR-0010):

```
inv ∷ s → Bool
∀ s i.  inv s ∧ valid i  ⇒  inv (fst (step s i))
```

- This is the guarantee, and it is unbounded: it holds for every run of that machine, of any length.
- A machine whose invariant cannot be established falls back to bounded exploration, and is shown as such on the assurance map. The claim is never overstated.

**Exploration is the counterexample finder and the fallback.**

- `ari explore` enumerates every scheduler and fault choice up to a bound, instead of sampling by seed. Steps are pure and state is a value, so states are hashed and deduplicated: it is an explicit-state model checker running the real program.
- Counterexamples are `ariadne.trace/1` traces and replay in the visualizer.
- The same monitors can run over the durable log in production (ADR-0013).

**Prove against a simple network; lift with verified wrappers.**

- Agents prove machine properties assuming reliable, ordered, exactly-once channels.
- Standard-library wrappers (deduplication, retry, reorder buffer) are proved once, in Lean, to carry those properties over to `lossy`, `unordered` and `duplicates` channels (ADR-0015).

**Data independence comes from polymorphism.** A step polymorphic in its payload cannot inspect it, so checking with a small payload domain covers every payload. This rests on a parametricity theorem for the core, to be mechanized.

**Deferred.**

- An external model checker, restricted to machine headers and protocol automata, which are finite by construction. This is where fairness-based liveness would come from.
- Full refinement proofs in Lean for selected library machines.
- Recognized machine kinds that unlock further unbounded guarantees: replicated machines that interact only through shared machines, monotone machines, topology restrictions for deadlock freedom, deterministic pipeline regions.

## Options considered

| Option | Trade-off |
| --- | --- |
| Ariadne specs with relational spec machines and a purpose-built model checker | One language; non-executable spec fragment, refinement mappings to find, a model checker to build |
| A separate spec language with trace validation | Mature tools; two languages, and the link to code is only as strong as recorded traces |
| Ariadne specs translated to an external model checker | One language; no sound abstraction, weak liveness, large unchecked translation |
| **Monitors, native exploration and solver-checked invariants (chosen)** | Smallest trusted base, native counterexamples, unbounded per-machine guarantees; invariants must be found, and system-wide properties are harder |

## Consequences

- Finding invariants becomes part of every implementation ticket's work.
- System-wide properties over all replicas need either quantified invariants (a second solver fragment, straining ADR-0010) or composition from per-machine invariants and channel contracts.
- The solver and the runtime are the trusted base for specs; no external model checker is in the toolchain.
- Supersedes ADR-0004's sketch of spec machines as relations returning sets.

## Open questions

- Liveness: deadlines over logical time with explicit fault and scheduling budgets (proposed), or true "eventually" properties.
- Whether reference machines, run as monitors over a system's boundary events and approved by a human, are used alongside "never" monitors (proposed).
- Quantified invariants versus compositional reasoning for system-wide properties.
