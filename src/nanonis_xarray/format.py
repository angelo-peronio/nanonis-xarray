"""Format workaround for pint-xarray scalars."""

import pint
from pint import UnitRegistry

format_unit_registry = UnitRegistry()


def format_compact_pretty_scalar(
    quantity: pint.Quantity, width_and_precision: str = "", *, short: bool = True
) -> str:
    """Format a scalar quantity to pint's "compact, pretty" format.

    Work around pint-xarray not supporting the "compact" format specifier "#".
    The pint-xarray's unit registry, used by nanonis-xarray,
    [converts](https://github.com/xarray-contrib/pint-xarray/issues/216) all magnitudes
    to arrays, and «to_compact applied to non numerical types has an undefined
    behavior.»
    """
    # Pint formatting docs:
    # https://pint.readthedocs.io/en/stable/user/formatting.html#string-formatting-specification
    format_specifier = f"{width_and_precision}{'~' if short else ''}#P"

    try:
        # Convert to a Python scalar.
        # This raises ValueError if quantity is not 0-dimensional.
        magnitude = quantity.magnitude.item()
    except AttributeError as exception:
        msg = "Quantity is not a 0-dimensional array. "
        "format_compact_short_pretty_scalar is redundnat in this case, "
        "use the pint format specifiers directly."
        raise ValueError(msg) from exception
    scalar_quantity = format_unit_registry.Quantity(magnitude, str(quantity.units))

    return f"{scalar_quantity:{format_specifier}}"
