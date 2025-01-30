import shutil
from pathlib import Path

from helpers import get_context, AOSCMVersion

import pandas as pd
from AOSCMcoupling import (
    Experiment,
    SchwarzCoupling,
    compute_nstrtini,
)


def get_nemo_file(data_dir: Path, start_date: pd.Timestamp):
    return data_dir / "nemo_from_CMEMS" / f"nemo_restart_{start_date.date()}.nc"


def get_ice_file(data_dir: Path, start_date: pd.Timestamp):
    ice_model = "si3"
    return data_dir / "nemo_from_CMEMS" / f"{ice_model}_restart_{start_date.date()}.nc"


def get_rstas_file(data_dir: Path, start_date: pd.Timestamp):
    start_date_string = f"{start_date.date()}_{start_date.hour:02}"
    rstas_name = f"rstas_{start_date_string}.nc"
    return data_dir / "rstas_from_AMIP" / rstas_name


def get_rstos_file(data_dir: Path, start_date: pd.Timestamp):
    return data_dir / "rstos_from_CMEMS" / f"rstos_{start_date.date()}.nc"


def get_oifs_input_file(data_dir: Path):
    return data_dir / "MOS6merged.nc"

context = get_context(AOSCMVersion.ECE4, "top_case")
start_dates = pd.date_range(
    pd.Timestamp("2020-04-12 00:00:00"), pd.Timestamp("2020-04-18 22:00:00"), freq="2h"
)
simulation_time = pd.Timedelta(2, "days")

forcing_file_start_date = pd.Timestamp("2020-04-12")
forcing_file_freq = pd.Timedelta(1, "hours")

max_iters = 30

exp_id = "CALB"
ensemble_directory = context.output_dir / "const_alb_ensemle"
run_directory = context.output_dir / exp_id

non_converged_experiments = []

def run_ensemble():
    ensemble_directory.mkdir(exist_ok=True)

    for start_date in start_dates[24:]:
        start_date_string = f"{start_date.date()}_{start_date.hour:02}"
        start_date_directory = ensemble_directory / start_date_string
        start_date_directory.mkdir(exist_ok=True)

        nstrtini = compute_nstrtini(
            start_date, forcing_file_start_date, int(forcing_file_freq.seconds / 3600)
        )
        nemo_input_file = get_nemo_file(context.data_dir, start_date)
        rstos_file = get_rstos_file(context.data_dir, start_date)
        ifs_input_file = get_oifs_input_file(context.data_dir)
        rstas_file = get_rstas_file(context.data_dir, start_date)
        ice_file = get_ice_file(context.data_dir, start_date)

        experiment = Experiment(
            dt_cpl=3600,
            dt_ifs=900,
            dt_nemo=900,
            dt_ice=900,
            ifs_leocwa=False,
            exp_id=exp_id,
            run_start_date=start_date,
            run_end_date=start_date + simulation_time,
            ifs_nstrtini=nstrtini,
            nem_input_file=nemo_input_file,
            ifs_input_file=ifs_input_file,
            oasis_rstas=rstas_file,
            oasis_rstos=rstos_file,
            with_ice=True,
            ice_input_file=ice_file,
            ifs_levels=137,
            ice_alb_idry=0.79, # constant albedo value used in SI3
        )

        experiment.cpl_scheme = 0
        schwarz = SchwarzCoupling(experiment, context)
        schwarz.run(max_iters, stop_at_convergence=True, rel_tol=1e-5)

        first_iter_dir = Path(f"{schwarz.run_directory}_1")
        new_directory = start_date_directory / "parallel"
        first_iter_dir.rename(new_directory)

        last_iter_dir = Path(f"{schwarz.run_directory}_{schwarz.iter}")
        new_directory = start_date_directory / "swr"
        last_iter_dir.rename(new_directory)

        for iter in range(2, schwarz.iter):
            iter_dir = Path(f"{schwarz.run_directory}_{iter}")
            shutil.rmtree(iter_dir)
        
        if not schwarz.converged:
            non_converged_experiments.append(experiment.run_start_date)

    print("Experiments which did not converge:")
    print(non_converged_experiments)

    if run_directory.exists():
        shutil.rmtree(run_directory)

if __name__ == "__main__":
    run_ensemble()
