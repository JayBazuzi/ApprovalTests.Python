Read the surviving mutant description in `.ignore/current_mutation.txt` and, if present, the JSON in `.ignore/current_mutation.json`.

Identify the behavioral change the mutant makes (the diff in the description). Write the smallest test that fails when that mutant is applied and passes on the unmutated code.

Add the test to the existing test file that covers the mutated module. Use the existing test style and imports. Do not modify production code. Do not approve any `.received.` files; the human will approve them.

Run the test command from `MUTATION_TEST_COMMAND` (or the default in the driver scripts) without `-x` to confirm the new test passes on the current code.

Write a concise git commit message describing the new test to `.ignore/commit-message.txt`. Use this format:

```
- t Added test for <module> <operator> mutant
```

If the mutant is not meaningfully testable (for example, removing a typing-only decorator with no runtime effect), do not modify any files. Instead, write "I don't know how to fix this".
