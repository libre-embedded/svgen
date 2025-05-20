"""
svgen - A module for working with number primitives.
"""


def css_number_to_ratio(val: float | int | str) -> float:
    """
    Given a few possible types of input, return a ratio between 0.0 and 1.0.
    """

    float_val = 0.0

    # Expect: a ratio between 0.0 and 1.0.
    if isinstance(val, float):
        float_val = val

    # Expect: a string ending with '%' and starting with a number between 0
    # and 100.
    elif isinstance(val, str):
        val = val.strip()

        # Assume the value is a percentage.
        if val.endswith("%"):
            val = val.replace("%", "")
            float_val = float(int(val)) / 100.0

        # Assume the value is a float.
        elif "." in val:
            float_val = float(val)

        # Assume the value is a hex String.
        elif len(val) <= 2:
            float_val = float(int(val, 16)) / 255.0

    # Expect: an integer between 0 and 255.
    elif isinstance(val, int):
        float_val = float(val) / 255.0

    # Normalize the result to a ratio between 0.0 and 1.0.
    float_val = max(float_val, 0.0)
    return min(float_val, 1.0)


def parse_ctor(
    value: str, prefix: str, suffix: str = None, sep: str = ","
) -> list[str]:
    """Parse individual arguments out of some color constructor."""

    value = value.strip()
    if value.startswith(prefix):
        value = value[len(prefix) :]
        if suffix is not None and value.startswith(suffix):
            value = value[len(suffix) :]

    # Remove braces.
    if value.startswith("("):
        value = value[1:]
    if value.endswith(")"):
        value = value[:-1]

    return [x.strip() for x in value.split(sep)]
