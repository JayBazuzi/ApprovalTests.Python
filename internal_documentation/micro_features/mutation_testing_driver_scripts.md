# Mutation Testing Driver Scripts

Add Linux driver scripts so `ai_fixer_loop.py` can use mutation testing to find untested code and prompt an AI to write tests.

## Scope

- `internal_documentation/scripts/find_problems` – uses Cosmic Ray to find a surviving mutant.
- `internal_documentation/scripts/fix_problem` – asks an AI to write a test that kills the mutant.
- `internal_documentation/scripts/tcr` – tests the change and commits or reverts it.
- `internal_documentation/mutation_testing.process.md` – instructions for the AI.
- Add `cosmic-ray` to development dependencies.

## Acceptance

- `ai_fixer_loop.py` can run with these scripts.
- `find_problems` exits 0 when a surviving mutant is found and writes `.ignore/current_mutation.txt`.
- `tcr` exits 0 when tests pass and a commit can be made, otherwise reverts.
