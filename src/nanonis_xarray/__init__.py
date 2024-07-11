"""Read a Nanonis .dat file into an xarray Dataset."""

from importlib.metadata import version

from pint import UnitRegistry

unit_registry = UnitRegistry()

from .read_dat import read_dat  # noqa: E402

__version__ = version("nanonis-xarray")
__all__ = ["read_dat", "unit_registry"]
