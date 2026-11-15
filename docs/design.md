# Design notes

The living design notes are kept in a shared doc: https://claude.ai/artifact/C24sdEroHo1yTpQij2xAxc

Decisions are recorded here as ADRs in [docs/adr](adr/README.md); when the doc and an accepted ADR disagree, the ADR wins.

## Summary

- **Vision:** tools for AI-written code focused on safety, correctness and verifiability. Review moves from code to specs.
- **Reliability without code review:** humans review specs; a small trusted checker; independent oracles (spec-derived tests, differential testing, an adversarial agent); capabilities bound the blast radius.
- **Semantic simplicity:** small core, compositional meaning, orthogonality, nothing unspecified, nothing implicit, predictable checking, canonical forms.
- **Machines:** Mealy machines as values; composition; spawning; timers; relational specs; snapshots; explicit waiting states; no shared mutable state.
- **Memory:** strict, reference counted, no cycles, linear resources and machine state.
- **Recursion:** total by default (structural, measures, fuel, `div` outside steps); graphs as ID-indexed maps.
- **Visualization and DX:** compiler-derived capability graphs, assurance maps, behavioral diffs, trace replay; tracing, replay debugging and profiling built in.
