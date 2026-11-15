# ADR-0002: Agents write the code; explicit beats sugar

**Status:** Accepted  
**Date:** 2026-11-15  
**Deciders:** Yuri

## Context

Most code will be written by agents and rarely read by humans. Human ergonomics is no longer the main design pressure.

## Decision

Optimize for checkability and locality for the model. Humans review specs, machines and compiler-generated views. Verbosity is not a cost; when explicitness and sugar conflict, explicit wins.

## Consequences

Several conveniences (`await`, implicit instances, overloading) lose their main justification. Tooling must render readable views for humans, since source is not optimized for them.
