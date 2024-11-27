import shutil
from pathlib import Path

import pandas as pd
from AOSCMcoupling import (
    Context,
    Experiment,
    SchwarzCoupling,
    compute_nstrtini,
    render_config_xml,
)
from AOSCMcoupling.helpers import AOSCM, reduce_output, serialize_experiment_setup


def get_nemo_file(data_dir: Path, start_date: pd.Timestamp):
    return data_dir / "nemo_from_CMEMS" / f"nemo_restart_{start_date.date()}.nc"


def get_ice_file(data_dir: Path, start_date: pd.Timestamp, model_version: int = 3):
    if model_version == 3:
        ice_model = "lim"
    elif model_version == 4:
        ice_model = "si3"
    else:
        raise ValueError("Model version not supported")
    return data_dir / "nemo_from_CMEMS" / f"{ice_model}_restart_{start_date.date()}.nc"


def get_rstas_file(data_dir: Path, start_date: pd.Timestamp):
    date = start_date.date()
    hour = f"{start_date.time().hour:02}"
    rstas_name = f"rstas_{date}_{hour}_era.nc"
    return data_dir / "rstas_from_AMIP" / rstas_name


def get_rstos_file(data_dir: Path, start_date: pd.Timestamp):
    return data_dir / "rstos_from_CMEMS" / f"rstos_{start_date.date()}.nc"


def get_oifs_input_file(data_dir: Path):
    return data_dir / "MOS6merged.nc"


# context = Context(
#     platform="pc-gcc-openmpi",
#     model_version=3,
#     model_dir="/home/valentina/dev/aoscm/ece3-scm",
#     output_dir="/home/valentina/dev/aoscm/experiments/PAPA",
#     template_dir="/home/valentina/dev/aoscm/scm-coupling/templates",
#     data_dir="/home/valentina/dev/aoscm/initial_data/top_case",
#     ifs_version="40r1v1.1.ref",
# )
context = Context(
    platform="cosmos",
    model_version=4,
    model_dir="/home/vschuller/aoscm",
    output_dir="/home/vschuller/experiments/output",
    template_dir="/home/vschuller/ece-scm-coupling/templates",
    data_dir="/home/vschuller/initial_data/top_case",
)

start_dates = pd.date_range(
    pd.Timestamp("2020-04-12 00:00:00"), pd.Timestamp("2020-04-18 22:00:00"), freq="2h"
)
simulation_time = pd.Timedelta(2, "days")

forcing_file_start_date = pd.Timestamp("2020-04-12")
forcing_file_freq = pd.Timedelta(1, "hours")

coupling_scheme_to_name = {
    0: "parallel",
    1: "atm-first",
    2: "oce-first",
}

max_iters = 30

exp_id = "TNSB"
ensemble_directory = context.output_dir / "top_ensemble"
run_directory = context.output_dir / exp_id

non_converged_experiments = []

if __name__ == "__main__":
    ensemble_directory.mkdir(exist_ok=True)

    aoscm = AOSCM(context)

    for start_date in start_dates:
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
        ice_file = get_ice_file(context.data_dir, start_date, context.model_version)

        experiment = Experiment(
            dt_cpl=3600,
            dt_ifs=720,
            dt_nemo=1200,
            dt_ice=3600,
            ifs_nradfr=-1,
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
        )

        for coupling_scheme, cpl_scheme_name in coupling_scheme_to_name.items():
            experiment.cpl_scheme = coupling_scheme
            render_config_xml(context, experiment)
            aoscm.run_coupled_model()
            reduce_output(run_directory, keep_debug_output=False)
            serialize_experiment_setup(experiment, run_directory)
            new_directory = start_date_directory / cpl_scheme_name
            run_directory.rename(new_directory)

        experiment.cpl_scheme = 0
        schwarz = SchwarzCoupling(experiment, context)
        schwarz.run(max_iters, stop_at_convergence=True, rel_tol=1e-5)
        new_directory = start_date_directory / "schwarz"
        converged_schwarz_dir = Path(f"{schwarz.run_directory}_{schwarz.iter}")
        converged_schwarz_dir.rename(new_directory)
        for iter in range(1, schwarz.iter):
            nonconverged_schwarz_dir = Path(f"{schwarz.run_directory}_{iter}")
            shutil.rmtree(nonconverged_schwarz_dir)
        if not schwarz.converged:
            non_converged_experiments.append(experiment.run_start_date)

    print("Experiments which did not converge:")
    print(non_converged_experiments)

    if run_directory.exists():
        shutil.rmtree(run_directory)
