# ADR-0010: One refinement mechanism in a decidable fragment; Lean as the escape hatch

**Status:** Accepted (revised after adversarial review)  
**Date:** 2026-11-15  
**Deciders:** Yuri

## Context

Full dependent types maximize expressiveness but reintroduce the complexity ADR-0003 removes. The first draft of this ADR proposed refinement types and DML-style indexed types side by side. An adversarial review found that:

- the two overlap (typestate is a phantom enum index; length indices are refinements), which breaks the one-way rule;
- "the checker never times out" contradicted the draft's own "time budgets";
- the typestate example assumed operations succeed and ignored timeouts;
- session types were an unacknowledged third mechanism;
- ADR-0007's "every ID is present" needs a finite-set sort the draft excluded.

## Decision

**One mechanism: index refinements.**

- Types carry index fields over fixed sorts: `Int`, `Bool`, declared enums, finite sets. `{i : Int | p}` is sugar for an indexed `Int`. Measures such as `len` are index fields, not axiomatized functions.
- Predicates are quantifier-free linear integer arithmetic with uninterpreted functions. Multiplication is allowed by literals only; other products are uninterpreted.
- Enum indices are solved by unification, with no solver. This is typestate.
- Everything else goes to a pinned solver under a deterministic step budget (not wall-clock time). `unknown` is a hard error: restructure, or insert a runtime check. Checking is "deterministic and budgeted", which replaces "never times out".
- Every refinement predicate is executable. Validators are derived automatically and run at trust boundaries: channel receive, parsing, snapshot restore.

**Linear handles and typestate.**

```
send      ∷ Conn Open ⊸ Bytes → Result (Conn Open) (Conn Broken, NetErr)
onTimeout ∷ Conn Pending ⊸ Conn Broken
```

- Fallible operations return the handle in every branch.
- A handle held across a waiting state has an explicit index for it, and the timeout transition gives it a definite index.
- Effect handlers are one-shot while a linear value is live.

**Protocols are automata.** Each channel protocol is a declared finite automaton; the linear endpoint is indexed by its state. Session types are therefore typestate, and the protocol is a spec machine.

```
recv ∷ Chan P s ⊸ ∃s'. {step P s s'} (Msg s s', Chan P s')
```

**Inference.** Full index signatures on every top-level definition; no index generalization at `let`; no indices in effect rows; explicit existential unpacking.

**Outside the fragment.** No full dependent types and no in-language proof terms. Properties the fragment cannot state are proved in Lean against the mechanized core, or checked at the spec layer (monitor machines in simulation first, model checking later). Types derived from schemas come from build-time generation.

**Mechanization.** The Lean soundness proof is parameterized over an abstract entailment relation; the solver is in the trusted base.

## Options considered

| Option | Trade-off |
| --- | --- |
| Full dependent types (Lean, Idris) | States anything; manual proofs, complex core |
| Refinement types and indexed types as two mechanisms (first draft) | Familiar from DML and Liquid Haskell; redundant, two ways to write bounds |
| **One index-refinement mechanism, Lean escape hatch (chosen)** | Decidable and predictable; a real expressiveness cliff |

## Consequences

- Out of reach in the language: nonlinear arithmetic (`Mat n m a → Vec (n * m) a`), payload types that depend on a tag value, generic schema projections, units of measure, encode/decode round-trip proofs. These go to Lean, the spec layer, code generation, or runtime checks.
- Supersedes the original "dependently typed" framing of Ariadne.
- Amends ADR-0009: "session types" there means protocol automata as defined here.

## Open questions

- Are multi-shot effect handlers needed at all? If so, linear values cannot cross effect operations.
- Are row-polymorphic records worth adding, given effect rows already exist?
- Who maintains the core-to-Lean export, and when does the Lean escape hatch become usable in practice?
- Which nonlinear cases (rates, matrix dimensions) matter enough to need a dedicated sort?
