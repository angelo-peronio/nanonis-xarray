"""Read a Nanonis .dat file into an xarray Dataset."""

from pathlib import Path

import pandas as pd
import xarray as xr

from .header import parse_header_lines

_encoding = "utf-8"


def read_dat(path: Path | str) -> xr.Dataset:
    """Read a Nanonis .dat file into an xarray Dataset."""
    path = Path(path)
    tag_idx = find_tag(path, "[DATA]", encoding=_encoding)
    n_header_lines = tag_idx - 1
    with path.open(encoding=_encoding) as file:
        header_lines = [next(file) for _ in range(n_header_lines)]
    header = parse_header_lines(header_lines)
    data = pd.read_csv(path, sep="\t", header=tag_idx)
    return


def find_tag(path: Path, tag: str, encoding: str = "utf-8"):
    """Search for a tag within a text file.

    Return the 0-based line index of the first line containing the tag.
    Raise RuntimeError if the tag is not found.
    """
    with path.open(encoding=encoding) as file:
        for line_index, line in enumerate(file):
            if tag in line:
                return line_index
        raise RuntimeError(f"Tag {tag} not found in {path}")
