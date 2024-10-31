"""Parse the data."""

import re
from dataclasses import dataclass
from typing import Literal

import pandas as pd
import xarray as xr
from pint import Unit

from . import unit_registry


def parse_data(data: pd.DataFrame) -> xr.Dataset:
    """Parse the data."""
    # Drop the averages, they will be recomputed.
    data = data.drop(columns=[name for name in data.columns if "[AVG]" in name])
    column_info = [parse_column_label(label) for label in data.columns]
    # Create a multi-index for the columns.
    multi_label_keys = ("name", "sweep", "direction")
    multi_labels = [
        {key: info[key] for key in (multi_label_keys)} for info in column_info
    ]
    col_index = pd.MultiIndex.from_frame(pd.DataFrame(multi_labels))
    data.columns = col_index
    # The first column is the independent variable of the measurement,
    # we use it as row index.
    data = data.set_index(col_index[0])
    data.index.name = data.index.name[0]
    # Convert DataFrame -> Dataset
    data = data.stack(level=(1, 2), future_stack=True)  # noqa: PD013
    dataset = xr.Dataset.from_dataframe(data)
    dataarray_attrs = {
        info["name"]: {key: info[key] for key in ("long_name", "units")}
        for info in column_info
    }
    for name in dataset.data_vars:
        dataset[name].attrs |= dataarray_attrs[name]
    return dataset


@dataclass(frozen=True)
class ColumnInfo:
    """Properties of a saved data column.

    Attributes
    ----------
    name: str
        Channel name, normalized.
    long_name: str
        Channel name, not normalized.
    sweep: int
        Sweep (repetition) index, 1-based.
    direction: Literal["fw", "bw"]
        Sweep direction, forward ("fw") or backward ("bw")
    units: Unit
        Channel physical units.
    """

    name: str
    long_name: str
    sweep: int
    direction: Literal["fw", "bw"]
    units: Unit

    def __getitem__(self, item: str) -> str | int | Unit:
        """Get an attribute, dict-like."""
        # https://stackoverflow.com/a/62561069
        return getattr(self, item)


_column_label_regexp = re.compile(
    r"^(?P<name>[^\[\(]+) "
    r"(?:\[(?P<sweep>\d{5})\] )?"
    r"(?:\[(?P<backward>bwd)\] )"
    r"?\((?P<units>.*)\)"
)


def parse_column_label(label: str) -> ColumnInfo:
    """Parse a Nanonis column label."""
    if matched := _column_label_regexp.match(label):
        sweep = int(matched.group("sweep")) if matched.group("sweep") else 1
        return ColumnInfo(
            name=normalize(matched.group("name")),
            long_name=matched.group("name"),
            sweep=sweep,
            direction="bw" if matched.group("backward") else "fw",
            units=unit_registry.Unit(matched.group("units")),
        )
    msg = f"Column label '{label}' not in the expected format."
    raise ValueError(msg)


def normalize(name: str) -> str:
    """Normalize a channel name."""
    return name.lower().replace(" ", "_")
