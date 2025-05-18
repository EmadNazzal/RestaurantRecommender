# Python Standards

## Overview

We follow the [Google Python Style Guide] and [PEP 8 Style Guide] for Python standards. Only the key documentation formatting rules are listed below. Please refer to the guides for more detailed information.

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

[Google Python Style Guide]: https://google.github.io/styleguide/pyguide.html
[Google Style Python Docstrings]: https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
[PEP 8 Style Guide]: https://peps.python.org/pep-0008/
