# Syntax choices (draft for ticket #1)

Status: the owner reviewed this draft on 2026-11-15 and chose to keep its overall syntax (ML and Rust flavoured, braces, `fn`), after seeing OCaml-style, Elm-style and clause-style alternatives. Lark stays as the grammar notation. The open problems at the end are not settled. Each row is a choice, the reason, and the alternative.

The grammar is `grammar.lark`. `check_grammar.py` verifies it is LALR(1) with no conflicts, that the card's code blocks and every file in `examples/` parse, and that sixteen malformed inputs are rejected. Only the grammar is checked: no types, no exhaustiveness, no behaviour.

## Choices in the pure fragment

| # | Choice | Why | Alternative |
| --- | --- | --- | --- |
| 1 | ASCII, keyword-led, brace-delimited syntax close to Rust and Go; no significant whitespace | Models have seen far more of it than ML-style syntax, and braces make the grammar simple to constrain during generation | ML or Haskell style layout |
| 2 | Case is lexical: lowercase for values and type variables, uppercase for types and constructors | Removes whole classes of ambiguity from the grammar; a parser never needs a symbol table | Case-insensitive roles |
| 3 | `fn f(x: T) -> T { ... }`, annotations mandatory at top level, lambdas `fn(x) { ... }` unannotated | Matches ADR-0003 (annotated top-level definitions); lambdas stay short | Annotations everywhere, or nowhere |
| 4 | Type parameters and arguments in `[...]`, as in Go and Scala | `<` and `>` stay comparison operators only, so no lexer tricks | `<...>` |
| 5 | `if` exists and always has `else`, though `match` on `Bool` could replace it | Models write `if` constantly; forbidding it would fail the writability spike for no semantic gain. It desugars to `match`. | `match` only (stricter "one way") |
| 6 | A match arm ends with a comma, always | A terminator is more regular than a separator with an optional trailing comma | Separator, or newline-terminated arms |
| 7 | Constructor fields are all positional or all named, fixed by the declaration, and used the same way in construction and patterns; no field punning | One way per constructor; `Open(tokens: t)` is explicit about which field is bound (ADR-0002) | Punning (`Open(tokens)`), or mixing |
| 8 | Records are single-constructor types with named fields, built with parentheses: `Point(x: 1, y: 2)` | Braces then only ever mean a block, a match body or a declaration body, which keeps `if cond { ... }` unambiguous | `Point { x: 1 }` (needs Rust's special cases) |
| 9 | No record update syntax | Smaller grammar; rebuilding is verbose, which ADR-0002 accepts | `p with (x: 1)` |
| 10 | Comparisons do not chain, and no operator is user-definable | Nothing implicit (ADR-0003) | Chained comparisons |
| 11 | Only `let` takes a semicolon; a block is lets followed by exactly one expression | No statement and expression distinction to learn; no unit-valued statements, since nothing has effects | Semicolons everywhere |
| 12 | Lists have literal syntax `[a, b]` in expressions only; patterns use `Nil` and `Cons` | Needed for `emit [...]`; list patterns would add a second way to match | List patterns |
| 13 | `M::E` for a machine's event | `.` stays field access only, which avoids a shift/reduce conflict | `M.E` |

## Choices in machines

| # | Choice | Why | Alternative |
| --- | --- | --- | --- |
| 14 | `step(state, event, env)` is an ordinary block that matches on the pair `(state, event)` | Reuses the expression language; no separate handler syntax to learn or to specify | `on State, Event { ... }` handler blocks |
| 15 | Transitions are declared in the header; a `drop` pair is declared there and has no arm | The header is the human-reviewed part (ADR-0012); a dropped pair is a reviewable decision, not code | `drop` written as an arm |
| 15a | A row may declare its outputs: `sends` channel fields and `starts` timers (ADR-0020) | An arm may emit only what its row declares, a syntactic check | Outputs unconstrained by the header |
| 15b | `State on _ -> drop` drops every event with no explicit row for that state; a wildcard can only drop (ADR-0020) | Most rows of a real header are drops; the expansion is finite and always shown | Every drop row written out |
| 16 | Every arm ends in `next State(...) emit [...]`, and `emit` is mandatory even when empty | One shape for every step result; outputs can never be forgotten silently | Optional `emit` |
| 17 | `init(cfg, env)` uses the same `next ... emit` form | The first state and first outputs are produced the same way as all later ones | A separate initial-state declaration |
| 18 | Declaration keywords (`state`, `event`, `config`, `on`, ...) are contextual; only `fn let if else match next emit Chan` and `_` are reserved | `state` and `event` are the natural parameter names for `step`; reserving them would trip models constantly | Reserve everything (simpler lexer) |
| 19 | Time and randomness come from `env` (ADR-0016) | A step sees one instant | Built-in functions |

## Provisional (belongs to later tickets, shown so the example system could be written)

- **Refinement sugar** `{n: Int | n > 0}` (ticket 18).
- **Channel types** `Chan[Msg, cap 64, reject]` and their tags (ticket 08, ADR-0014, ADR-0015).
- **Timers** as `timer Name`, started with `start_timer(Name, duration)`; `waiting` as a state attribute (ticket 09).
- **Monitors** as `monitor Name { ... }` with `observes M::E` and `violation` states (ticket 10).
- **Invariants** as `invariant(s) { ... }` (ticket 29).

## Open problems the sketch exposed

1. **How a machine receives replies.** A reply channel is typed by its payload (`Chan[Decision]`), but a machine receives events. The sketch bridges them with `env.inbox(Decided)`, which makes a channel that wraps each payload in an event. This is invented here and needs a real decision, together with how a machine's inbound channels get their capacity and tags.
2. **`Rejected` is declared as an ordinary event** in the `Request` machine. ADR-0014 makes it a control event; whether it is declared, built in, or carries the rejected message is undecided.
3. **State context is repeated in full.** `Request` carries channel types of 40 characters in three places. There are no type aliases; adding them is cheap but is one more construct.
4. **Rebuilding a state to change one field is verbose.** Every `Open(...)` repeats `capacity` and `window`. Choice 9 is the cause.
5. **The monitor in the example is subtly wrong.** It counts admissions when the requester receives them, so an admission granted late in one window can be counted in the next. The monitor should observe what the limiter sends. What a monitor may observe (deliveries, sends, or both) is a ticket 10 decision.
6. **There is no wiring syntax.** Nothing yet says how the system is assembled: which machines are spawned first and how channels are created and handed out.
7. **Exhaustiveness over pairs** is defined against the expanded `transitions` table, not by the plain match rule, because dropped pairs have no arm. The type checker (ticket 04, ticket 06) needs this as a special rule.
8. **Whether models write this reliably** is exactly what the spike in ticket 03 measures. The riskiest items for that are choices 6, 7 and 16.
