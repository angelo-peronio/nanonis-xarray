# Development notes for nanonis-xarray

## Ideas

* Evaluate `pint-xarray`. Maybe `attrs.units` is enough?
* Try to plot, to see how the units look like.
* Do we want to normalize the header keys?
* Do we want to have the header to be accessible like `data.attrs.key.subkey`?
* Which text encoding does Nanonis actually use?

## Notes

* It seems Nanonis ships Python routines <https://www.specs-group.com/nanonis/products/mimea/mimea-software/#c1315>
* Indeed, they have two packages on PyPI:
    * <https://pypi.org/project/nanonis-tramea/>
    * <https://pypi.org/project/nanonis-spm/>
* [Rescipy](https://github.com/rescipy-project)
