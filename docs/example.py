# %%
# ! %reload_ext autoreload
# ! %autoreload complete
from pathlib import Path

from nanonis_xarray import read_dat

project_root = Path(__file__).parents[1]
data_path = project_root / "tests" / "data" / "z.dat"
data = read_dat(data_path)

# %%
data["current"].mean(dim=["sweep"]).sel(direction="fw").plot()
# %%
