# ADR-0012: Milestone 1 scope revised after adversarial review

**Status:** Accepted  
**Date:** 2026-11-15  
**Deciders:** Yuri

## Context

An adversarial review of the first ticket breakdown for ADR-0011 found that it was a layer inventory, not a thin slice: nothing built the spec layer the demo depends on, the riskiest unknowns came last, the Lean work was oversized, and several tickets bundled unrelated work.

## Decision

ADR-0011's goal and demo stand. Its scope changes as follows.

- **Spec for this milestone is a monitor machine.** An invariant is a machine that observes the trace and is checked during simulation. No model checker in this milestone.
- **Syntax and LLM-writability come first.** A one-page syntax card with a grammar, then a spike in which an LLM writes step bodies that must parse, before the layers above the parser are built.
- **Transitions are declared in the machine header.** Humans review the header; agents write the step bodies; diagrams come from the header, not from analysis of step code.
- **Channels carry a message type, delivery tags and a capacity.** Protocol automata (ADR-0010) are built off the demo's critical path.
- **Lean is staged**, amending ADR-0006's "from the start": (1) definitions, an executable evaluator and differential CI against the Rust interpreter; (2) soundness for a monomorphic pure core; (3) machine step and linearity, as a stretch.
- **Differential testing is concrete.** `ari --emit-core` writes elaborated core as JSON; the Lean evaluator runs it; CI compares results. Rust type inference stays in the trusted base and this is stated openly.
- **`ariadne.diag/1` and `ariadne.trace/1` are owned contracts**, each defined by one ticket and consumed by others.
- **Refinements, termination checks, linearity checks and trace shrinking run in parallel**, off the critical path to the demo.

Deferred beyond this milestone: effect types and capabilities, relational spec machines and refinement checking against them, snapshots, constrained decoding, composition combinators, `Fuel`, model checking.

## Consequences

- The demo is reachable through a 15-ticket critical path; verification depth grows on parallel tracks.
- The first working demo will not have effect types or capabilities, so its safety story is narrower than the full design.
- A failed LLM-writability spike changes the syntax before anything is built on it.
