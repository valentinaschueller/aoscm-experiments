from pathlib import Path

import pandas as pd
from AOSCMcoupling import (
    AOSCM,
    Context,
    Experiment,
    compute_nstrtini,
    get_ifs_forcing_info,
    render_config_xml,
)
from AOSCMtools import (
    compute_rstas,
    compute_rstos,
    ice_init_from_cmems,
    ocean_init_from_cmems,
)


def generate_rstas_files(
    context: Context, start_dates: pd.DatetimeIndex, ifs_forcing_file: Path
):
    exp_id = "TEMP"
    aoscm = AOSCM(context)

    out_dir = context.data_dir / "rstas_from_AMIP"
    out_dir.mkdir(exist_ok=True)

    simulation_time = pd.Timedelta(1, "h")

    for start_date in start_dates:
        start_date_string = f"{start_date.date()}_{start_date.hour:02}"

        ifs_forcing_start, ifs_forcing_freq, ifs_levels = get_ifs_forcing_info(
            ifs_forcing_file
        )
        nstrtini = compute_nstrtini(
            start_date, ifs_forcing_start, int(ifs_forcing_freq.seconds / 3600)
        )

        dummy_file = ifs_forcing_file  # needs to be a valid file path

        experiment = Experiment(
            dt_cpl=3600,
            dt_ifs=900,
            dt_nemo=900,
            ifs_leocwa=False,
            exp_id=exp_id,
            run_start_date=start_date,
            run_end_date=start_date + simulation_time,
            ifs_nstrtini=nstrtini,
            nem_input_file=dummy_file,
            ifs_input_file=ifs_forcing_file,
            oasis_rstas=dummy_file,
            oasis_rstos=dummy_file,
            ice_input_file=dummy_file,
            ifs_levels=ifs_levels,
        )

        render_config_xml(context, experiment)
        aoscm.run_atmosphere_only()

        compute_rstas(
            context.output_dir / exp_id,
            out_dir / f"rstas_{start_date_string}.nc",
        )


def generate_nemo_input(
    context: Context,
    start_dates: pd.DatetimeIndex,
    lat: float,
    lon: float,
    cmems_file: Path,
):
    out_dir = context.data_dir / "nemo_from_CMEMS"
    out_dir.mkdir(exist_ok=True)
    for date in start_dates:
        ocean_init_from_cmems(lat, lon, date, cmems_file, out_dir)
