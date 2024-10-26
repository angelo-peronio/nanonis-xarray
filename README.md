# Read a Nanonis spectroscopy `.dat` file into a xarray Dataset

[![SPEC 0 — Minimum Supported Dependencies](https://img.shields.io/badge/SPEC-0-green?labelColor=%23004811&color=%235CA038)](https://scientific-python.org/specs/spec-0000/)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/format.json)](https://github.com/astral-sh/ruff)

`nanonis_xarray` is a Python module to read spectroscopy measurements saved in ASCII
format (.dat) by a [Nanonis Mimea](https://www.specs-group.com/nanonis/products/mimea/)
SPM control system from [SPECS Surface Nano Analysis GmbH](https://www.specs-group.com/).

The data is read into a [`xarray.Dataset`](https://docs.xarray.dev/en/stable/getting-started-guide/why-xarray.html#core-data-structures)
