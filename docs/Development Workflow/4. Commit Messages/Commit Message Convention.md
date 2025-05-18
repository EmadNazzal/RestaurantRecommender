# Commit Message Convention

## Commit Message Format

```bash
<type>: short description

Longer description here if necessary.
```

## Summary

- The first line of the commit message.
- 72 characters or less.

### Type

Must be one of the following:

- **`feat`**: Introduces a new feature.
- **`fix`**: Resolves an identified issue or bug.
- **`docs`**: Updates or adds to the documentation.
- **`style`**: Changes that do not affect the meaning of the code (e.g. white-space, formatting, missing semi-colons, etc.).
- **`refactor`**: Reorganises or improves existing code without changing its external behaviour.
- **`test`**: Adding missing tests or correcting existing tests.
- **`chore`**: Maintenance tasks unrelated to the production codebase (e.g. build tasks, dependencies, configuration, etc.).

### Short Description

- Use the imperative, *present* tense.
    - For example, use "change" not "changed" or "changes".
- Do not capitalise the first letter.
- Do not add a dot (.) at the end.
- Example:
    - `feat: add new feature`
    - `fix: resolve issue`

## Body

### Longer Description

- Use the imperative, *present* tense.
    - For example, use "change" not "changed" or "changes".
- Explain the motivation for the change and contrast this with previous behaviour.
