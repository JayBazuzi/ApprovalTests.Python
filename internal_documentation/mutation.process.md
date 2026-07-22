Read the `.ignore/mutant.txt` file. It contains a unified diff describing a single surviving mutant: a change to production code that the current test suite does NOT detect.

Add or strengthen a test in `tests/` so that this mutant is killed - that is, so the test suite fails when the mutated line is applied, and passes on the unmutated code.

Rules:
- Only change files under `tests/`. **NEVER** modify the production code that is being mutated.
- **NEVER** add `# pragma: no mutate` or otherwise suppress the mutant. Only write a test that detects the behavior change.
- Follow the existing test style in `tests/`, including using approvals where appropriate.
- If the mutant is an equivalent mutant (there is no observable behavior difference, so no test can kill it), do not write a test. Instead tell me "This looks like an equivalent mutant: <short_explanation>".

Write a git commit message that describes the test you added to `.ignore/commit-message.txt`.

Here's an example of what the commit message should look like:

```
- r Kill mutant in scrubbers.py: assert templates_regex_scrubber replaces matches
```
