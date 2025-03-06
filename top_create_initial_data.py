import pandas as pd
from AOSCMcoupling.helpers import compute_nstrtini, get_ifs_forcing_info
from AOSCMtools import compute_rstos

from helpers import AOSCMVersion, get_context
from initial_data import generate_ice_input, generate_nemo_input, generate_rstas_files

if __name__ == "__main__":
    context = get_context(AOSCMVersion.ECE3, "top")

    ifs_forcing_file = context.data_dir / "MOS6merged.nc"
    start_date, frequency, _ = get_ifs_forcing_info(ifs_forcing_file)

    ifs_start_dates = pd.date_range(
        pd.Timestamp("2020-04-12 00:00:00"),
        pd.Timestamp("2020-04-18 22:00:00"),
        freq="2h",
    )
    generate_rstas_files(context, ifs_start_dates, ifs_forcing_file)

    nemo_start_dates = pd.date_range(
        pd.Timestamp("2020-04-12 00:00:00"),
        pd.Timestamp("2020-04-18 00:00:00"),
        freq="1d",
    )
    generate_nemo_input(
        context,
        nemo_start_dates,
        84.375,
        16.0,
        context.data_dir / "cmems_output.nc",
    )
    generate_ice_input(
        context,
        nemo_start_dates,
        84.375,
        16.0,
        context.data_dir / "cmems_output_ice.nc",
        ifs_forcing_file,
    )

    rstos_out_dir = context.data_dir / "rstos_from_CMEMS"
    rstos_out_dir.mkdir(exist_ok=True)
    for date in nemo_start_dates:
        nstrtini = compute_nstrtini(date, start_date, int(frequency.seconds / 3600))
        compute_rstos(
            context.data_dir / "nemo_from_CMEMS" / f"nemo_restart_{date.date()}.nc",
            rstos_out_dir / f"rstos_{date.date()}.nc",
            context.data_dir / "nemo_from_CMEMS" / f"si3_restart_{date.date()}.nc",
            ifs_forcing_file,
            nstrtini,
        )
