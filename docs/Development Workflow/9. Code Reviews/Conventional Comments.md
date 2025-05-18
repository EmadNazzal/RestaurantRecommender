# Conventional Comments

[Conventional Comments] are used in the code review process to provide feedback in a structured and consistent manner. They are designed to be easy to understand, machine-readable, and to encourage collaboration between reviewers and authors.

## Format

```markdown
<label>: <subject>

[discussion]
```

- **`label`**: This is a single label that signifies what kind of comment is being left.
- **`subject`**: This is the main message of the comment.
- **`discussion` (optional)**: This contains supporting statements, context, reasoning, and anything else to help communicate the "why" and "next steps" for resolving the comment.

### Example

```markdown
suggestion: This is not worded correctly.

Can we change this to match the wording of the marketing page?
```

## Labels

- **`suggestion`**: Suggestions propose improvements to the current subject. It's important to be explicit and clear on what is being suggested and why it is an improvement.
- **`issue`**: Issues highlight specific problems with the subject under review. It is strongly recommended to pair this comment with a suggestion.
- **`praise`**: Praises highlight something positive. Do not leave false praise (which can actually be damaging). Do look for something to sincerely praise.
- **`nitpick`**: Nitpicks are trivial preference-based requests.
- **`question`**: Questions are appropriate if you have a potential concern but are not quite sure if it's relevant or not.
- **`thought`**: Thoughts represent an idea that popped up from reviewing.
- **`note`**: Notes simply highlight something the reader should take note of.
- **`chore`**: Chores are simple tasks that must be done before the PR can be "officially" accepted.

## Best Practices

- Leave actionable comments.
- Combine similar comments, e.g. multiple nitpicks can be combined into one comment.
- Replace "you" with "we" to foster a collaborative environment.
- Replace "should" with "could" to encourage discussion and exploration.

[Conventional Comments]: https://conventionalcomments.org/
