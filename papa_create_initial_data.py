import pandas as pd
from AOSCMtools import compute_rstos

from helpers import AOSCMVersion, get_context
from initial_data import generate_nemo_input, generate_rstas_files

if __name__ == "__main__":
    context = get_context(AOSCMVersion.ECE3, "papa")

    ifs_start_dates = pd.date_range(
        pd.Timestamp("2014-07-01 00:00:00"),
        pd.Timestamp("2014-07-28 18:00:00"),
        freq="6h",
    )
    generate_rstas_files(
        context, ifs_start_dates, context.data_dir / "papa_2014-07_era.nc"
    )

    nemo_start_dates = pd.date_range(
        pd.Timestamp("2014-07-01 12:00"),
        pd.Timestamp("2014-07-28 12:00"),
        freq="1d",
    )
    generate_nemo_input(
        context,
        nemo_start_dates,
        50.0,
        -145.0,
        context.data_dir / "cmems_with_seaice.nc",
    )

    rstos_out_dir = context.data_dir / "rstos_from_CMEMS"
    rstos_out_dir.mkdir(exist_ok=True)
    for date in nemo_start_dates:
        compute_rstos(
            context.data_dir / "nemo_from_CMEMS" / f"nemo_restart_{date.date()}.nc",
            rstos_out_dir / f"rstos_{date.date()}.nc",
        )
