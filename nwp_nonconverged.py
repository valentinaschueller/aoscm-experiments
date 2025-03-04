import shutil
from pathlib import Path

import pandas as pd
from AOSCMcoupling import (
    AOSCM,
    Experiment,
    SchwarzCoupling,
    compute_nstrtini,
    get_ifs_forcing_info,
)

from helpers import AOSCMVersion, get_context


def get_nemo_file(data_dir: Path, start_date: pd.Timestamp):
    return data_dir / "nemo_from_CMEMS" / f"init_PAPASTATION_{start_date.date()}.nc"


def get_rstas_file(data_dir: Path, start_date: pd.Timestamp):
    date = start_date.date()
    hour = f"{start_date.time().hour:02}"
    rstas_name = f"rstas_{date}_{hour}_era.nc"
    return data_dir / "rstas_from_AMIP" / rstas_name


def get_rstos_file(data_dir: Path, start_date: pd.Timestamp):
    return data_dir / "rstos_from_CMEMS" / f"rstos_{start_date.date()}.nc"


model_version = AOSCMVersion.ECE3
mass_flux = True
context = get_context(model_version, "nwp")

if model_version == AOSCMVersion.ECE3:
    start_dates = [
        pd.Timestamp("2014-07-03 00:00:00"),
        pd.Timestamp("2014-07-12 18:00:00"),
        pd.Timestamp("2014-07-25 12:00:00"),
    ]
elif model_version == AOSCMVersion.ECE43:
    start_dates = [
        pd.Timestamp("2014-07-19 00:00"),
        pd.Timestamp("2014-07-07 06:00"),
        pd.Timestamp("2014-07-10 18:00"),
        pd.Timestamp("2014-07-24 18:00"),
        pd.Timestamp("2014-07-07 18:00"),
        pd.Timestamp("2014-07-28 18:00"),
        pd.Timestamp("2014-07-17 06:00"),
        pd.Timestamp("2014-07-26 12:00"),
        pd.Timestamp("2014-07-23 06:00"),
        pd.Timestamp("2014-07-11 18:00"),
        pd.Timestamp("2014-07-18 06:00"),
    ]
else:
    start_dates = [
        pd.Timestamp("2014-07-11 12:00"),
        pd.Timestamp("2014-07-02 12:00"),
        pd.Timestamp("2014-07-24 18:00"),
        pd.Timestamp("2014-07-23 12:00"),
        pd.Timestamp("2014-07-18 06:00"),
        pd.Timestamp("2014-07-14 18:00"),
        pd.Timestamp("2014-07-23 00:00"),
    ]

simulation_time = pd.Timedelta(2, "days")

max_iters = 40

exp_id = "ENNC"
ensemble_directory = context.output_dir / "ensemble_output_nc"
run_directory = context.output_dir / exp_id

non_converged_experiments = []

if __name__ == "__main__":
    ensemble_directory.mkdir(exist_ok=True)

    aoscm = AOSCM(context)

    ifs_input_file = context.data_dir / "ifs" / f"papa_2014-07_era.nc"
    ifs_forcing_start, ifs_forcing_freq, ifs_levels = get_ifs_forcing_info(
        ifs_input_file
    )

    for start_date in start_dates:
        start_date_string = f"{start_date.date()}_{start_date.hour:02}"
        start_date_directory = ensemble_directory / start_date_string
        start_date_directory.mkdir(exist_ok=True)

        nstrtini = compute_nstrtini(
            start_date, ifs_forcing_start, int(ifs_forcing_freq.seconds / 3600)
        )
        nemo_input_file = get_nemo_file(context.data_dir, start_date)
        rstos_file = get_rstos_file(context.data_dir, start_date)
        rstas_file = get_rstas_file(context.data_dir, start_date)

        experiment = Experiment(
            dt_cpl=3600,
            dt_ifs=900,
            dt_nemo=900,
            ifs_leocwa=False,
            ifs_lecumf=mass_flux,
            exp_id=exp_id,
            run_start_date=start_date,
            run_end_date=start_date + simulation_time,
            ifs_nstrtini=nstrtini,
            nem_input_file=nemo_input_file,
            ifs_input_file=ifs_input_file,
            oasis_rstas=rstas_file,
            oasis_rstos=rstos_file,
            ifs_levels=ifs_levels,
        )

        schwarz = SchwarzCoupling(experiment, context)
        schwarz.run(max_iters, stop_at_convergence=True, rel_tol=1e-5)
        assert schwarz.iter == max_iters
        for iter in range(1, schwarz.iter + 1):
            nonconverged_schwarz_dir = Path(f"{schwarz.run_directory}_{iter}")
            nonconverged_schwarz_dir.rename(start_date_directory / f"iter_{iter}")

    if run_directory.exists():
        shutil.rmtree(run_directory)
