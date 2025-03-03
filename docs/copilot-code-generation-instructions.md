# Code Style

- Use Python 3.12
- Use Python type hints/annotations.


# Documenting Code

- Add docstrings to Python modules, classes and functions. 
- Use the Google style guide for docstrings.
- Use the imperative mood in the subject line.
- Use the present tense.
- Ensure to include type annotations in the function signatures.
- For utility or helper functions/methods, include examples of usage in the docstrings as doctests.

## Example

```python

def add(a: int, b: int) -> int:
    """Add two numbers.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The sum of the two numbers.

    Examples:
        >>> add(1, 2)
        3
        >>> add(-1, 1)
        0
    """
    return a + b
```
