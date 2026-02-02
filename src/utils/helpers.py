def format_money(val: float) -> str:
    """
    Format large monetary values with Chinese units (亿/万).

    Args:
        val: Value in base currency (assumed Yuan or whatever API returns)

    Returns:
        str: Formatted string (e.g. "1.23亿")
    """
    if val is None:
        return "-"

    abs_val = abs(val)
    if abs_val > 100000000:
        return f"{val / 100000000:.2f}亿"
    elif abs_val > 10000:
        return f"{val / 10000:.2f}万"
    return f"{val:.2f}"
