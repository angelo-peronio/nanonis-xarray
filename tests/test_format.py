"""Tests format_compact_pretty_scalar."""

import numpy as np
import pytest
from pint import UnitRegistry

from nanonis_xarray import unit_registry as u
from nanonis_xarray.format import format_compact_pretty_scalar


def test_format_compact_pretty_scalar():
    """Test format_compact_pretty_scalar."""
    quantity = 1.0e6 * u.meter**2

    formatted = format_compact_pretty_scalar(quantity)
    assert formatted == "1.0 km²"

    formatted = format_compact_pretty_scalar(quantity, width_and_precision=".2f")
    assert formatted == "1.00 km²"

    quantity_array = np.array([1.0e6, 2.0e6]) * u.meter**2
    with pytest.raises(
        ValueError, match="can only convert an array of size 1 to a Python scalar"
    ):
        formatted = format_compact_pretty_scalar(quantity_array)

    another_unit_registry = UnitRegistry()
    true_scalar_quantity = (
        1.0e6 * another_unit_registry.meter / another_unit_registry.second**2
    )
    with pytest.raises(ValueError, match=r"Quantity is not a 0-dimensional array."):
        formatted = format_compact_pretty_scalar(true_scalar_quantity)
