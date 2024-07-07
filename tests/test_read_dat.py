"""Test read_dat."""

from pathlib import Path

from nanonis_xarray import read_dat

data_folder = Path(__file__).parent / "data"


def test_read_dat():
    """Test read_dat."""
    _ = read_dat(data_folder / "z-001.dat")
