# Pull Request Convention

## Title

```bash
<issue type>: short description (<closing type> ID-<number>)
```

### Issue Type

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

### Closing Type

Must be one of the following:

- **`fix`**: If the issue is a bug and is fully resolved.
- **`close`**: If the issue is not a bug and is fully resolved.
- **`ref`**: If the issue is not fully resolved.

### ID Number

- This is the ID of the Linear issue.
- Only one issue should be addressed in a single pull request.
    - If there are multiple issues, create separate pull requests for each issue.
    - If this is not possible, list all the issue numbers separated by commas, e.g. `fix ID-123, ID-124, ID-125` or `close ID-123, ref ID-124`.

## Checklist

Ensure that the pull request fulfils the following requirements, where applicable. Leave the items that are not applicable unchecked.

- [ ] PR title is the right issue type.
- [ ] PR title references the issue in the title.
- [ ] Tests have been added if necessary.
- [ ] Passes all existing tests.
- [ ] Code comments have been added, updated, or removed.
- [ ] Documentation has been updated.

## Description

Below are guidelines for writing a description for a pull request but are not required to be followed. The description should be detailed enough to provide context for the changes made in the PR, but it is up to the author to decide how much detail to include. These are suggestions to help guide the author in writing a description that is clear and informative.

- Use the imperative, *present* tense.
    - For example, use "change" not "changed" or "changes".
- Provide a detailed description of the changes made in the PR.
- Explain how the changes address the issue(s) mentioned in the title.
- If there are any additional notes or context that the reviewer should be aware of, include them in the description.
- If the PR is related to another issue, reference the issue(s) in the description using the format `ref ID-<number>`.

### Additions

- List the new features, functions, or content added in the PR.
- Provide a brief description of each addition.
- Explain why these items were added.

### Removals

- List any features, functions, or content that were removed in the PR.
- Provide a brief description of each removal.
- Explain why these items were removed.

### Changes

- List the changes made to existing features, functions, or content in the PR.
- Provide a brief description of each change.
- Explain why these changes were made.

### Testing

- Describe the testing process used to verify the changes in the PR.
- List the tests that were run and the results of each test.
- If the changes were tested manually, describe the steps taken to test the changes.
- If new tests were added, describe the purpose of each test and how it verifies the changes.
