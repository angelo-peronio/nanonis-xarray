# Read Nanonis spectroscopy `.dat` files into xarray Datasets

[![SPEC 0 — Minimum Supported Dependencies](https://img.shields.io/badge/SPEC-0-green?labelColor=%23004811&color=%235CA038)](https://scientific-python.org/specs/spec-0000/)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/format.json)](https://github.com/astral-sh/ruff)

`nanonis_xarray` is a Python module to read spectroscopy measurements saved in text
format (`.dat`) by a [Nanonis Mimea](https://www.specs-group.com/nanonis/products/mimea/)
SPM control system from [SPECS Surface Nano Analysis GmbH](https://www.specs-group.com/).

The data is read into a [`xarray.Dataset`](https://docs.xarray.dev/en/stable/getting-started-guide/why-xarray.html#core-data-structures), where each measured quantity, such as tunnelling current or AFM oscillation amplitude, is a [`xarray.DataArray`](https://docs.xarray.dev/en/stable/user-guide/data-structures.html#dataarray) with up to three dimensions:

* The independent variable of the measurement, such as bias voltage or tip $z$ position;
* The sweep number, if the measurement has been repeated multiple times;
* The sweep direction (forward or backward), if the independent variable has been swept in both directions.

It becomes then easy to e.g. plot the average of one measured channel in the forward direction:

```python
from matplotlib import pyplot as plt

from nanonis_xarray import read_dat

data = read_dat("tests/data/z.dat")
fig, ax = plt.subplots()
data["current"].mean(dim=["sweep"]).sel(direction="fw").plot()
```

## Work in progress

This library is under development: expect breaking changes. I do not plan to support the Nanonis binary formats (`.sxm`, `.3ds`), which can be read by similar projects:

* [`nanonispy2`](https://github.com/ceds92/nanonispy2)
* [`xarray-nanonis`](https://github.com/John3859/xarray-nanonis)
* ... and [many more](https://pypi.org/search/?q=nanonis).
