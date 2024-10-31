# Development notes for nanonis-xarray

## ToDo

* Evaluate [`pint_xarray`](https://xarray.dev/blog/introducing-pint-xarray).
* Use `example.py` to evaluate the user experience.
    * Plot.
    * Calculate averages.
    * Rotate lock-in x and y.
* Readme

## Ideas

* Do we want to normalize the header keys?
* Do we want to have the header to be accessible like `data.attrs.key.subkey`?
* Xarray [accessors](https://docs.xarray.dev/en/stable/internals/extending-xarray.html).

## Prio 2

* Enum instead of fw/bw (?)
* CategoricalIndex for direction (?)
* Which text encoding does Nanonis actually use?

## Notes

* It seems Nanonis ships Python routines <https://www.specs-group.com/nanonis/products/mimea/mimea-software/#c1315>
* Nanonis has two packages on PyPI:
    * <https://pypi.org/project/nanonis-tramea/>
    * <https://pypi.org/project/nanonis-spm/>
