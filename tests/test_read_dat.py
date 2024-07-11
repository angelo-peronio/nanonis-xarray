"""Test read_dat."""

from datetime import datetime
from pathlib import Path

from nanonis_xarray import read_dat
from nanonis_xarray import unit_registry as u

data_folder = Path(__file__).parent / "data"


def test_read_dat():
    """Test read_dat."""
    all_paths = data_folder.glob("*.dat")
    all_data = {path.stem: read_dat(path) for path in all_paths}

    assert "repetiton" not in all_data["a"].data_vars
    assert "direction" not in all_data["a"].data_vars
    assert all_data["a"].attrs["Bias Spectroscopy"]["MultiLine Settings"][
        "Integration"
    ] == 0.1 * u("ms")

    assert "repetiton" not in all_data["df_v"].data_vars
    assert all_data["df_v"].direction.size == 2

    assert all_data["z"].attrs["Bias Spectroscopy"]["backward sweep"] is True

    assert all_data["z"].repetition.size == 3
    assert all_data["z"].direction.size == 2

    for data in all_data.values():
        assert isinstance(data.attrs["NanonisMain"]["Session Path"], Path)
        assert isinstance(data.attrs["Date"], datetime)
