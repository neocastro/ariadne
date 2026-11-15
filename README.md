# Ariadne

A verifiable language for AI-written code.

Agents write the code; humans review specs, machines and compiler-generated views; a small trusted checker, independent oracles and capabilities keep the code honest.

- **Core:** a small, mechanized, pure, strict calculus with algebraic data types and effects. No GC: reference counting, no cyclic data, linear resources.
- **Structure:** programs are composed state machines that share no mutable state and talk over session-typed channels.
- **Proofs:** refinement, indexed and linear types in the language; a specification logic with model checking above it (ADR-0010, under discussion).
- **Tooling:** deterministic simulation with fault injection, compiler-generated diagrams and trace replay, structured diagnostics for agents.

## Documents

- [Decisions (ADRs)](docs/adr/README.md)
- [Design notes](docs/design.md)
- First milestone tickets: GitHub issues labelled `milestone-1`

## Status

Design phase. First milestone (ADR-0011): a thin vertical slice through every layer, built around one rate-limited API.
