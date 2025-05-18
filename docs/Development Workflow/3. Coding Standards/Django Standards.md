# Django Standards

## Overview

We follow the [Django Coding Style] for Django standards. The [Python Standards] are also followed for Python code within Django projects. Only the key documentation formatting rules are listed below. Please refer to the guides for more detailed information.

## General Formatting Rules

### Comments

```python
# This is a comment.
```

### Documentation Comments

Documentation comments are written in the Google Style Python Docstrings format, found [here][Google Style Python Docstrings].

### TODO

- Mark todos and action items with `TODO`.
- Append the GitHub username in parentheses as with the format `TODO(username)`.
- Append action items after a colon as in `TODO: action item`.

```python
# TODO(johndoe): Refactor this code.
```

```python
"""Docstring single line summary.

Docstring description.

Args:
    arg1: Description of arg1.
    arg2: Description of arg2.

TODO(johndoe):
    - Refactor this code.
    - Add more functionality.
"""
```

[Django Coding Style]: https://docs.djangoproject.com/en/5.0/internals/contributing/writing-code/coding-style/
[Google Style Python Docstrings]: https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
[Python Standards]: Python%20Standards.md
