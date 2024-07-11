"""Parse the data."""

import re
from typing import Any

import pandas as pd
import xarray as xr

from . import unit_registry


def parse_data(data: pd.DataFrame) -> xr.Dataset:
    """Parse the data."""
    # Drop the averages, they will be recomputed.
    data = data.drop(columns=[name for name in data.columns if "[AVG]" in name])
    column_info = [parse_column_label(label) for label in data.columns]
    # Create a multi-index for the columns.
    multi_label_keys = ("name", "repetition", "direction")
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


_column_label_regexp = re.compile(
    r"^(?P<name>[^\[\(]+) "
    r"(?:\[(?P<repetition>\d{5})\] )?"
    r"(?:\[(?P<backward>bwd)\] )"
    r"?\((?P<units>.*)\)"
)


def parse_column_label(label: str) -> dict[str, Any]:
    """Parse a Nanonis column label."""
    if matched := _column_label_regexp.match(label):
        if matched.group("repetition"):
            repetition = int(matched.group("repetition"))
        else:
            repetition = 1
        return {
            "name": normalize(matched.group("name")),
            "long_name": matched.group("name"),
            "repetition": repetition,
            "direction": "bw" if matched.group("backward") else "fw",
            "units": unit_registry.Unit(matched.group("units")),
        }
    msg = f"Column label '{label}' not in the expected format."
    raise ValueError(msg)


def normalize(name: str) -> str:
    """Normalize a channel name."""
    return name.lower().replace(" ", "_")
