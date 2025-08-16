"""Test read_dat."""

from datetime import datetime
from pathlib import Path

import xarray as xr
from pint_xarray import unit_registry as u

data_folder = Path(__file__).parent / "data"


def test_a() -> None:
    """Test opening a .dat file."""
    data_path = data_folder / "a.dat"
    data = xr.open_dataset(data_path)

    assert "sweep" not in data.data_vars
    assert "direction" not in data.data_vars
    assert data.attrs["Bias Spectroscopy"]["MultiLine Settings"][
        "Integration"
    ] == 0.1 * u("ms")
    assert isinstance(data.attrs["NanonisMain"]["Session Path"], Path)
    assert isinstance(data.attrs["Date"], datetime)


def test_df_v() -> None:
    """Test opening a .dat file."""
    data_path = data_folder / "df_v.dat"
    data = xr.open_dataset(data_path)

    assert "sweep" not in data.data_vars
    assert data.direction.size == 2
    assert isinstance(data.attrs["NanonisMain"]["Session Path"], Path)
    assert isinstance(data.attrs["Date"], datetime)


def test_z() -> None:
    """Test opening a .dat file."""
    data_path = data_folder / "z.dat"
    data = xr.open_dataset(data_path)

    assert data.attrs["Bias Spectroscopy"]["backward sweep"] is True
    assert data.sweep.size == 3
    assert data.direction.size == 2
    assert isinstance(data.attrs["NanonisMain"]["Session Path"], Path)
    assert isinstance(data.attrs["Date"], datetime)


def test_drop_variables() -> None:
    """Test drop_variables parameter."""
    data_path = data_folder / "a.dat"
    data_1 = xr.open_dataset(data_path)
    data_2 = xr.open_dataset(data_path, drop_variables="phase")

    assert "phase" in data_1
    assert "phase" not in data_2
