# Mutation Testing

Mutation testing measures how good our tests are. A tool (`mutmut`) makes small
changes to production code - "mutants" - such as flipping `>` to `>=` or `+` to
`-`, then re-runs the test suite. If some test fails, the mutant is **killed**
(good - our tests detect the change). If every test still passes, the mutant
**survives**, which means there is a gap in the test suite.

The goal of the process is to drive the number of surviving mutants to zero by
adding tests, without changing production code.

## The loop

This reuses the [AI Fixer Loop](ai_fixer_loop.md). A "problem" is a surviving
mutant, and a "fix" is a new or strengthened test. The three phases map onto the
abstract sequence like this:

1. **Select a thing to fix (deterministic, no AI) - `find_mutant`**
   Run `mutmut` and pick one surviving mutant. Its diff is written to
   `.ignore/mutant.txt` and its id to `.ignore/mutant_id.txt`. Exit code `0`
   means a survivor was found; `1` means none remain.

2. **Create a fix (via AI) - `fix_mutant`**
   The AI reads `.ignore/mutant.txt` and writes a test in `tests/` that would
   detect the mutated behavior. See `mutation.process.md` for the exact prompt.
   The AI changes **test code only** - never the production code being mutated.

3. **Verify and commit (deterministic, no AI) - `tcr_mutant`**
   First discard any production-code edits (the fix must be tests-only), then
   verify that (a) the full suite is green, and (b) the selected mutant is now
   killed - by re-running `mutmut` against just that mutant. If both hold it
   commits; otherwise it reverts.

The loop repeats until `find_mutant` reports no surviving mutants.

## Running it

```bash
./build_and_test.sh   # installs mutmut and confirms a green baseline
cd internal_documentation/scripts
python ai_fixer_loop.py --find find_mutant --fix fix_mutant --tcr tcr_mutant
```

Configuration for `mutmut` (which code to mutate, which tests to run) lives in
the `[mutmut]` section of `setup.cfg`.

## Equivalent mutants

Some mutants cannot be killed because they do not change observable behavior
(for example, mutating a type-alias assignment that is only used for
annotations). These are **equivalent mutants**. `fix_mutant` will not write a
test for them, so the loop would otherwise select the same mutant forever. When
that happens, resolve it by hand rather than by suppressing it, then re-run.
