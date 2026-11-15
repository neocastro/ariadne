# Ariadne syntax card (draft)

Everything you need to write Ariadne for milestone 1. The formal grammar is `grammar.lark`. There is one way to write each construct.

## Rules

- A file is `module a.b`, then `import`s, then declarations: `type`, `fn`, `machine`, `monitor`.
- Names starting lowercase are values, functions, fields and type variables. Names starting uppercase are types, constructors, machines, states and events. `M::E` names event `E` of machine `M`.
- Every function is pure and total. There is no null, no exception, no mutation, no I/O.
- Top-level functions annotate every parameter and the return type. Type parameters go in `[...]`.
- A block is `{ let ...; let ...; expr }`. The last expression is the value. Only `let` takes a semicolon.
- `if` always has `else`. `match` arms each end with a comma and must cover every case.
- A constructor's fields are all positional (`Some(x)`) or all named (`Point(x: 1, y: 2)`), as declared, in construction and in patterns alike. Read a named field with `p.x`.
- Operators: `+ - * / %`, `== != < <= > >=` (not chainable), `&& || !`. Nothing is overloaded or converted implicitly.
- Reserved words: `fn let if else match next emit Chan` and `_`. Declaration keywords (`state`, `event`, `on`, ...) are only special inside declarations.
- Comments are `// to end of line`.

```ari
module card.pure

type Option[a] = None | Some(a)
type List[a] = Nil | Cons(a, List[a])
type Point = Point(x: Int, y: Int)

fn sum(xs: List[Int]) -> Int {
  match xs {
    Nil => 0,
    Cons(n, rest) => n + sum(rest),
  }
}

fn first_or[a](xs: List[a], fallback: a) -> a {
  match xs {
    Nil => fallback,
    Cons(x, _) => x,
  }
}

fn nudge(p: Point, by: Int) -> Point {
  let moved = p.x + by;
  if moved < 0 { Point(x: 0, y: p.y) } else { Point(x: moved, y: p.y) }
}
```

## Machines

A machine is the only thing that has effects. Its **header** (config, states, events, timers, transitions, invariant) is what humans review. Its **bodies** (`init`, `step`) are what you write.

- `transitions` lists every allowed `State on Event -> Target | Target`. A pair that should be ignored is declared `-> drop`. Every state and event pair must appear.
- `step(state, event, env)` is a pure function. It matches on `(state, event)` with one or more arms for every pair that is not `drop`, and none for pairs that are.
- Every arm, and `init`, ends in `next <State> emit [<outputs>]`. Use `emit []` for no outputs.
- Outputs: `send(channel, message)` and `start_timer(TimerName, duration)`. Nothing else reaches the outside.
- `env.now` is the logical time of this event. `env.inbox(Event)` is a channel that delivers to this machine as `Event`.
- A `waiting` state must have a transition on a timer.
- `invariant(s)` must hold in every reachable state.

```ari
module card.limiter

type Decision = Admit | Deny

machine Limiter {
  config(capacity: {n: Int | n > 0}, window: Time)

  state Open(tokens: Int, capacity: Int, window: Time)
  state Exhausted(capacity: Int, window: Time)

  event Acquire(reply: Chan[Decision, cap 1, lossy, drop_newest])
  timer WindowEnd

  transitions {
    Open on Acquire -> Open | Exhausted
    Open on WindowEnd -> Open
    Exhausted on Acquire -> Exhausted
    Exhausted on WindowEnd -> Open
  }

  invariant(s) {
    match s {
      Open(tokens: t, capacity: c, window: _) => 0 < t && t <= c,
      Exhausted(capacity: c, window: _) => 0 < c,
    }
  }

  init(cfg, env) {
    next Open(tokens: cfg.capacity, capacity: cfg.capacity, window: cfg.window)
    emit [start_timer(WindowEnd, cfg.window)]
  }

  step(state, event, env) {
    match (state, event) {
      (Open(tokens: t, capacity: c, window: w), Acquire(reply: r)) =>
        if t > 1 {
          next Open(tokens: t - 1, capacity: c, window: w) emit [send(r, Admit)]
        } else {
          next Exhausted(capacity: c, window: w) emit [send(r, Admit)]
        },
      (Open(tokens: _, capacity: c, window: w), WindowEnd) =>
        next Open(tokens: c, capacity: c, window: w) emit [start_timer(WindowEnd, w)],
      (Exhausted(capacity: c, window: w), Acquire(reply: r)) =>
        next Exhausted(capacity: c, window: w) emit [send(r, Deny)],
      (Exhausted(capacity: c, window: w), WindowEnd) =>
        next Open(tokens: c, capacity: c, window: w) emit [start_timer(WindowEnd, w)],
    }
  }
}
```

Channel types are `Chan[Message, tags]` with tags `cap N`, one overflow policy (`reject`, `drop_newest`, `drop_oldest`), and the faults the channel may show (`lossy`, `unordered`, `duplicates`, with `dedup N`).
