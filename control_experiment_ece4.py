import pandas as pd

from AOSCMcoupling.context import Context
from AOSCMcoupling.schwarz_coupling import SchwarzCoupling
from AOSCMcoupling.experiment import Experiment
from AOSCMcoupling.helpers import AOSCM, reduce_output, compute_nstrtini
from AOSCMcoupling.templates import render_config_xml


cpl_schemes = [0, 1, 2]
max_iters = 20
exp_prefix = "CE4"

context = Context(
    platform="tetralith",
    model_version=4,
    model_dir="/home/x_valsc/aoscm",
    output_dir="/home/x_valsc/experiments/output",
    template_dir="/home/x_valsc/rundir/templates",
    plotting_dir="/home/x_valsc/experiments/plots",
    data_dir="/home/x_valsc/initial_data/control_experiment",
)

start_date = pd.Timestamp("2014-07-01")
simulation_duration = pd.Timedelta(4, "days")
ifs_input_start_date = pd.Timestamp("2014-07-01")
ifs_input_freq = pd.Timedelta(6, "hours")
nstrtini = compute_nstrtini(start_date, ifs_input_start_date, int(ifs_input_freq.seconds / 3600))

experiment = Experiment(
    dt_cpl=3600,
    dt_ifs=900,
    dt_nemo=900,
    exp_id="",
    ifs_leocwa=False,
    with_ice=False,
    nem_input_file=context.data_dir / "nemo_papa_2014-07-01.nc",
    ifs_input_file=context.data_dir / "oifs_papa_2014-07-01_30.nc",
    oasis_rstas=context.data_dir / "rstas_2014-07-01_00_era.nc",
    oasis_rstos=context.data_dir / "rstos_2014-07-01.nc",
    run_start_date=start_date,
    run_end_date=start_date + simulation_duration,
    ifs_nstrtini=nstrtini,
)

aoscm = AOSCM(context)


def run_naive_experiments():
    for cpl_scheme in cpl_schemes:
        experiment.exp_id = f"{exp_prefix}{cpl_scheme}"
        experiment.cpl_scheme = cpl_scheme
        render_config_xml(context, experiment)
        aoscm.run_coupled_model()
        reduce_output(
            context.output_dir / experiment.exp_id, keep_debug_output=False
        )


def run_schwarz_experiments():
    experiment.exp_id = f"{exp_prefix}S"
    experiment.cpl_scheme = 0
    schwarz_exp = SchwarzCoupling(experiment, context)
    schwarz_exp.run(max_iters)


def run_parallel_schwarz_without_cleanup():
    experiment.exp_id = f"{exp_prefix}S"
    experiment.cpl_scheme = 0
    schwarz_exp = SchwarzCoupling(experiment, context, False)
    schwarz_exp.run(max_iters)


if __name__ == "__main__":
    run_naive_experiments()

    run_schwarz_experiments()
