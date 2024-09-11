import pandas as pd
from AOSCMcoupling.context import Context
from AOSCMcoupling.experiment import Experiment
from AOSCMcoupling.helpers import AOSCM, compute_nstrtini, reduce_output
from AOSCMcoupling.schwarz_coupling import SchwarzCoupling
from AOSCMcoupling.templates import render_config_xml

# context = Context(
#     platform="tetralith",
#     model_version=4,
#     model_dir="/home/x_valsc/aoscm",
#     output_dir="/home/x_valsc/experiments/output",
#     template_dir="/home/x_valsc/rundir/templates",
#     data_dir="/home/x_valsc/initial_data/mosaic_spring",
# )
context = Context(
    platform="cosmos",
    model_version=4,
    model_dir="/home/vschuller/aoscm",
    output_dir="/home/vschuller/experiments/output",
    template_dir="/home/vschuller/ece-scm-coupling/templates",
    data_dir="/home/vschuller/initial_data/mosaic_spring",
)

cpl_schemes = [0, 1, 2]
max_iters = 30
exp_prefix = "MOS"

start_date = pd.Timestamp("2020-05-15")
simulation_duration = pd.Timedelta(3, "days")
ifs_input_start_date = pd.Timestamp("2020-05-15")
ifs_input_freq = pd.Timedelta(1, "hours")
nstrtini = compute_nstrtini(
    start_date, ifs_input_start_date, int(ifs_input_freq.seconds / 3600)
)

experiment = Experiment(
    dt_cpl=3600,
    dt_ifs=900,
    dt_nemo=900,
    exp_id="",
    ifs_leocwa=False,
    with_ice=True,
    nem_input_file=context.data_dir / "nemo_restart_2020-05-15.nc",
    ice_input_file=context.data_dir / "si3_restart_2020-05-15.nc",
    ifs_input_file=context.data_dir / "scm_in_20200515_era5.nc",
    oasis_rstas=context.data_dir / "rstas_2020-05-15.nc",
    oasis_rstos=context.data_dir / "rstos_2020-05-15.nc",
    run_start_date=start_date,
    run_end_date=start_date + simulation_duration,
    ifs_nstrtini=nstrtini,
    ifs_levels=137,
)

aoscm = AOSCM(context)


def run_naive_experiments():
    for cpl_scheme in cpl_schemes:
        experiment.exp_id = f"{exp_prefix}{cpl_scheme}"
        experiment.cpl_scheme = cpl_scheme
        render_config_xml(context, experiment)
        aoscm.run_coupled_model()
        reduce_output(context.output_dir / experiment.exp_id, keep_debug_output=False)


def run_parallel_schwarz():
    experiment.exp_id = f"{exp_prefix}S"
    experiment.cpl_scheme = 0
    schwarz_exp = SchwarzCoupling(experiment, context)
    schwarz_exp.run(max_iters)


def run_atmosphere_only():
    cpl_scheme = 0
    experiment.exp_id = f"{exp_prefix}{cpl_scheme}"
    experiment.cpl_scheme = cpl_scheme
    render_config_xml(context, experiment)
    aoscm.run_atmosphere_only()
    reduce_output(context.output_dir / experiment.exp_id, keep_debug_output=False)


if __name__ == "__main__":
    # run_atmosphere_only()
    run_naive_experiments()

    run_parallel_schwarz()
