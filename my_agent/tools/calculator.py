def calculator(operation: str, a: float, b: float) -> str:
    """Perform a math or financial operation on two numbers.

    Args:
        operation: One of '+', '-', '*', '/', '**', 'pct_change', 'margin', 'ratio'.
            pct_change: percentage change from a to b → ((b - a) / a) * 100
            margin: margin of a over b → (a / b) * 100 (e.g. net income / revenue)
            ratio: simple ratio a / b (e.g. debt-to-equity)
        a: First number.
        b: Second number.

    Returns:
        The result as a string.
    """
    ops = {
        '+': lambda: a + b,
        '-': lambda: a - b,
        '*': lambda: a * b,
        '**': lambda: a ** b,
    }
    if operation in ops:
        return str(ops[operation]())
    if operation in ('/', 'ratio'):
        if b == 0:
            return "Cannot divide by zero"
        return str(a / b)
    if operation == 'pct_change':
        if a == 0:
            return "Cannot compute pct_change from zero base"
        return f"{((b - a) / a) * 100:.2f}%"
    if operation == 'margin':
        if b == 0:
            return "Cannot compute margin with zero denominator"
        return f"{(a / b) * 100:.2f}%"
    return f"Unknown operation: {operation}"