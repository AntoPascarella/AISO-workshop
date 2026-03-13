def calculator(operation: str, a: float, b: float) -> str:
    """Perform a basic arithmetic calculation.

    Use this tool for ANY math operation — addition, subtraction,
    multiplication, division, exponentiation, or square roots.

    Args:
        operation: The math operation to perform. One of:
            "add", "subtract", "multiply", "divide", "power", "sqrt"
        a: The first number.
        b: The second number. For sqrt, this is ignored — only 'a' is used.

    Returns:
        The result as a string.
    """
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            return "Error: Division by zero."
        result = a / b
    elif operation == "power":
        result = a ** b
    elif operation == "sqrt":
        result = a ** 0.5
    else:
        return f"Error: Unknown operation '{operation}'."
    return str(result)