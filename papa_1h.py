import shutil
from pathlib import Path

import pandas as pd
from AOSCMcoupling import (
    Experiment,
    SchwarzCoupling,
    compute_nstrtini,
    get_ifs_forcing_info,
    render_config_xml,
)
from AOSCMcoupling.helpers import AOSCM, reduce_output
from ruamel.yaml import YAML

from helpers import AOSCMVersion, get_context


def get_nemo_file(data_dir: Path, start_date: pd.Timestamp):
    return data_dir / "nemo_from_CMEMS" / f"nemo_restart_{start_date.date()}.nc"


def get_rstas_file(data_dir: Path, start_date: pd.Timestamp):
    date = start_date.date()
    hour = f"{start_date.time().hour:02}"
    rstas_name = f"rstas_{date}_{hour}.nc"
    return data_dir / "rstas_from_AMIP" / rstas_name


def get_rstos_file(data_dir: Path, start_date: pd.Timestamp):
    return data_dir / "rstos_from_CMEMS" / f"rstos_{start_date.date()}.nc"


def print_nonconverged_dates(dir_or_experiments):
    try:
        dir_or_experiments.is_dir()
    except AttributeError:  # list of experiments was passed
        for experiment in dir_or_experiments:
            print(experiment.run_start_date)
        return

    output_dir = dir_or_experiments

    start_dates = []
    yaml = YAML(typ="unsafe", pure=True)
    for date_dir in output_dir.glob("*"):
        if not date_dir.is_dir():
            continue
        with open(date_dir / "schwarz" / "setup_dict.yaml") as yaml_file:
            experiment = yaml.load(yaml_file)
            converged = (
                experiment.iterate_converged["2-norm"]
                and experiment.iterate_converged["inf-norm"]
            )
            if converged:
                continue
            start_dates.append(experiment.run_start_date)

    print([date for date in start_dates])


def run_nwp_ensemble(with_mass_flux: bool = True):
    context = get_context(AOSCMVersion.ECE3, "papa")

    start_dates = pd.date_range(
        pd.Timestamp("2014-07-01 00:00:00"),
        pd.Timestamp("2014-07-28 18:00:00"),
        freq="6h",
    )
    simulation_time = pd.Timedelta(1, "h")

    ifs_input_file = context.data_dir / f"papa_2014-07_era.nc"
    ifs_forcing_start, ifs_forcing_freq, ifs_levels = get_ifs_forcing_info(
        ifs_input_file
    )

    max_iters = 15

    non_converged_experiments = []

    output_dir = context.output_dir / "papa_1H_L31"
    output_dir.mkdir(exist_ok=True)

    for start_date in start_dates:
        exp_id = "PAPA"
        start_date_string = f"{start_date.date()}_{start_date.hour:02}"
        start_date_directory = output_dir / start_date_string
        start_date_directory.mkdir(exist_ok=True)
        context.output_dir = start_date_directory

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
            exp_id=exp_id,
            run_start_date=start_date,
            run_end_date=start_date + simulation_time,
            ifs_nstrtini=nstrtini,
            nem_input_file=nemo_input_file,
            ifs_input_file=ifs_input_file,
            oasis_rstas=rstas_file,
            oasis_rstos=rstos_file,
            ifs_levels=ifs_levels,
            ifs_lecumf=with_mass_flux,
        )

        schwarz = SchwarzCoupling(experiment, context)
        schwarz.run(max_iters, stop_at_convergence=False, rel_tol=1e-5)

        if not schwarz.converged:
            non_converged_experiments.append(experiment)

    print_nonconverged_dates(non_converged_experiments)


if __name__ == "__main__":
    run_nwp_ensemble(with_mass_flux=True)
