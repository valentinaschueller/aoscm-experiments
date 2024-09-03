# %% Setup
from pathlib import Path

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

from AOSCMcoupling.files import NEMOPreprocessor, OIFSPreprocessor
from plotting import set_style

set_style()

exp_id = "TOPS"
max_iters = 30
start_date = pd.Timestamp("2020-04-16")
time_shift = np.timedelta64(1, "h")
plot_folder = Path(f"plots/{exp_id}_4")


def load_iterates(
    file_name: str, preprocess: callable, max_iters: int, step: int
) -> xr.Dataset:
    swr_dim = xr.DataArray(np.arange(max_iters) + 1, dims="swr_iterate")
    iterates = [
        xr.open_mfdataset(f"output/{exp_id}_{iter}/{file_name}", preprocess=preprocess)
        for iter in range(1, max_iters + 1, step)
    ]
    iterates = xr.concat(iterates, swr_dim)
    return iterates


def plot_all_iterates(da: xr.DataArray, **kwargs):
    fig, ax = plt.subplots()
    da[0].plot(ax=ax, color="#9C6114")

    ax.set(**kwargs)
    for iter in range(1, max_iters):
        ax.plot(da.time, da[iter], alpha=alpha, color="k")

    return fig


def animate(da: xr.DataArray, **kwargs):
    fig, ax = plt.subplots()
    fig.set_figheight(5)
    fig.set_figwidth(8)
    fig.set_tight_layout(True)
    da[0].plot(ax=ax, color="#9C6114")

    ax.set(**kwargs)

    def update(frame):
        # update the line plot:
        ax.plot(
            da[frame + 1].time,
            da[frame + 1],
            color="k",
            alpha=alpha,
        )

    ani = animation.FuncAnimation(fig=fig, func=update, frames=da.shape[0] - 1)
    return ani


def create_plots(da: xr.DataArray, file_stem: str, axis_settings: dict):
    axis_settings["xlabel"] = "Time"
    axis_settings["xmargin"] = 0.0

    fig = plot_all_iterates(da, **axis_settings)
    fig.savefig(plot_folder / f"{file_stem}.pdf", bbox_inches="tight")
    fig.savefig(plot_folder / f"{file_stem}.png", bbox_inches="tight", dpi=300)

    # ani = animate(da, **axis_settings)
    # ani.save(plot_folder / f"{file_stem}.mp4", dpi=300)
    plt.close("all")


# %%

oifs_preprocessor = OIFSPreprocessor(start_date, time_shift)
nemo_preprocessor = NEMOPreprocessor(start_date, time_shift)

plot_folder.mkdir(exist_ok=True)
max_iters = 8
alpha = 0.25

sequential_swr = False
if sequential_swr:
    step = 2
else:
    step = 1

oifs_diagvars = load_iterates(
    "diagvar.nc", oifs_preprocessor.preprocess, max_iters, step
)
oifs_progvars = load_iterates(
    "progvar.nc", oifs_preprocessor.preprocess, max_iters, step
)
nemo_t_grids = load_iterates(
    f"*_T*.nc", nemo_preprocessor.preprocess, max_iters, step
)
# nemo_ice_grids = load_iterates(
#     f"*_icemod.nc", nemo_preprocessor.preprocess, max_iters, step
# )


# %% 10m Temperature

axis_settings = {
    "title": "Temperature at 10m (OIFS)",
    "ylabel": "Temperature [°C]",
}

create_plots(oifs_progvars.t[:, :, -1] - 273.15, "10t_oifs", axis_settings)

# %% 2m Temperature

axis_settings = {
    "title": "2m Temperature (OIFS)",
    "ylabel": "Temperature [°C]",
}

create_plots(oifs_diagvars.temperature_2m - 273.15, "2t_oifs", axis_settings)

# %% Surface Sensible Heat Flux
axis_settings = {
    "title": "Surface Sensible Heat Flux (OIFS)",
    "ylabel": "Heat Flux $[W m^{-2}]$",
}

create_plots(oifs_diagvars.sfc_sen_flx, "ssh_oifs", axis_settings)

# %% SST

axis_settings = {
    "title": "Sea Surface Temperature (NEMO)",
    "ylabel": "Temperature [°C]",
}

create_plots(nemo_t_grids.sosstsst, "sst_nemo", axis_settings)

# %% SSW

axis_settings = {
    "title": "Surface SW Radiation (OIFS)",
    "ylabel": "Radiative Flux $[W m^{-2}]$",
}

create_plots(oifs_diagvars.sfc_swrad, "ssw_oifs", axis_settings)

# %% Sea Ice Concentration


axis_settings = {
    "title": "Sea Ice Concentration (LIM3)",
    "ylabel": "Sea Ice Concentration [-]",
}

# create_plots(nemo_ice_grids.iceconc, "iceconc_lim3", axis_settings)

# %% Ice Surface Temperature

axis_settings = {
    "title": "Sea Ice Surface Temperature (LIM3)",
    "ylabel": "Temperature [°C]",
}

# create_plots(nemo_ice_grids.icest, "icest_lim3", axis_settings)

# %% Mean Ice Temperature

axis_settings = {
    "title": "Mean Sea Ice Temperature (LIM3)",
    "ylabel": "Temperature [°C]",
}

# create_plots(nemo_ice_grids.micet, "micet_lim3", axis_settings)

# %% Surface Energy Budget

oifs_seb = (
    oifs_diagvars.sfc_sen_flx
    + oifs_diagvars.sfc_lat_flx
    + oifs_diagvars.sfc_lwrad
    + oifs_diagvars.sfc_swrad
)
axis_settings = {
    "title": "Surface Energy Budget",
    "ylabel": "Energy Budget $[W m^{-2}]$",
}

create_plots(oifs_seb, "seb_oifs", axis_settings)


# %%

axis_settings = {
    "title": "Total Ice Heat Content (LIM3)",
    "ylabel": "Heat Content [J]",
}

# create_plots(nemo_ice_grids.icehc, "icehc_lim3", axis_settings)
