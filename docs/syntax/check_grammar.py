"""Mechanical check of the draft grammar (ticket #1 sketch).

Throwaway tooling: the Rust parser of ticket #2 replaces it. It verifies that
  1. the grammar is LALR(1) with no shift/reduce or reduce/reduce conflicts,
  2. every file in examples/ and every ```ari block in card.md parses,
  3. a set of strings that must be rejected is rejected.

Run:  python3 docs/syntax/check_grammar.py     (needs: pip install lark)
"""
import io, logging, pathlib, re, sys
from lark import Lark, logger
from lark.exceptions import LarkError

HERE = pathlib.Path(__file__).parent

MUST_FAIL = {
    "if without else": "module m\nfn f(n: Int) -> Int { if n > 0 { n } }",
    "match arm without trailing comma": "module m\nfn f(n: Int) -> Int { match n { 0 => 1, _ => 2 } }",
    "record literal with braces": "module m\ntype P = P(x: Int)\nfn f() -> P { P { x: 1 } }",
    "let without semicolon": "module m\nfn f() -> Int { let x = 1 x }",
    "block ending in a let": "module m\nfn f() -> Int { let x = 1; }",
    "unannotated top-level parameter": "module m\nfn f(n) -> Int { n }",
    "missing return type": "module m\nfn f(n: Int) { n }",
    "mixed positional and named fields": "module m\ntype T = T(Int, y: Int)",
    "next without emit": "module m\nmachine M { state A init(c, e) { next A } }",
    "chained comparison": "module m\nfn f(a: Int) -> Bool { 0 < a < 10 }",
    "reserved word as a variable": "module m\nfn f(next: Int) -> Int { next }",
    "lowercase type name": "module m\ntype point = P(Int)",
    "wildcard transition to a state": "module m\nmachine M { state A event E transitions { A on _ -> A } }",
    "sends without a channel name": "module m\nmachine M { state A event E transitions { A on E -> A sends } }",
    "transition without target": "module m\nmachine M { state A event E transitions { A on E -> } }",
}


def main() -> int:
    log = io.StringIO()
    handler = logging.StreamHandler(log)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    try:
        parser = Lark((HERE / "grammar.lark").read_text(encoding="utf-8"), parser="lalr", debug=True)
    except LarkError as err:
        print("GRAMMAR ERROR:", err)
        return 1
    conflicts = [line for line in log.getvalue().splitlines() if "conflict" in line.lower()]
    failures = 0
    if conflicts:
        failures += 1
        print(f"FAIL  {len(conflicts)} LALR conflict(s):")
        for line in conflicts[:10]:
            print("      ", line)
    else:
        print("ok    grammar is LALR(1) with no conflicts")

    sources = {p.name: p.read_text(encoding="utf-8") for p in sorted((HERE / "examples").glob("*.ari"))}
    card = (HERE / "card.md").read_text(encoding="utf-8") if (HERE / "card.md").exists() else ""
    for i, block in enumerate(re.findall(r"```ari\n(.*?)```", card, flags=re.S), 1):
        sources[f"card.md block {i}"] = block
    for name, text in sources.items():
        try:
            parser.parse(text)
            print(f"ok    parses: {name}")
        except LarkError as err:
            failures += 1
            print(f"FAIL  does not parse: {name}\n       {str(err).splitlines()[0]}")

    for name, text in MUST_FAIL.items():
        try:
            parser.parse(text)
            failures += 1
            print(f"FAIL  wrongly accepted: {name}")
        except LarkError:
            print(f"ok    rejected: {name}")

    print("\nRESULT:", "all checks passed" if failures == 0 else f"{failures} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
