import pandas as pd
from AOSCMcoupling import (
    AOSCM,
    Experiment,
    SchwarzCoupling,
    compute_nstrtini,
    reduce_output,
    render_config_xml,
)

from helpers import AOSCMVersion, get_context, get_ifs_forcing_metadata

context = get_context(AOSCMVersion.ECE3, "control_experiment")
mass_flux = True
exp_prefix = "CEX"  # use C43 for 'ECE43' configuration, MFN and M43 for mass flux-off experiments

cpl_schemes = [0, 1, 2]
max_iters = 30

start_date = pd.Timestamp("2014-07-01")
simulation_duration = pd.Timedelta(4, "days")

ifs_forcing_file = context.data_dir / "oifs_papa_2014-07-01_30.nc"
ifs_forcing_start, ifs_forcing_freq = get_ifs_forcing_metadata(ifs_forcing_file)
nstrtini = compute_nstrtini(
    start_date, ifs_forcing_start, int(ifs_forcing_freq.seconds / 3600)
)

experiment = Experiment(
    dt_cpl=3600,
    dt_ifs=900,
    dt_nemo=900,
    exp_id="",
    ifs_leocwa=False,
    with_ice=False,
    nem_input_file=context.data_dir / "nemo_papa_2014-07-01.nc",
    ifs_input_file=ifs_forcing_file,
    oasis_rstas=context.data_dir / "rstas_2014-07-01_00_era.nc",
    oasis_rstos=context.data_dir / "rstos_2014-07-01.nc",
    run_start_date=start_date,
    run_end_date=start_date + simulation_duration,
    ifs_nstrtini=nstrtini,
    ifs_levels=60,
    ifs_lecumf=mass_flux,
)

aoscm = AOSCM(context)


def run_naive_experiments():
    for cpl_scheme in cpl_schemes:
        experiment.exp_id = f"{exp_prefix}{cpl_scheme}"
        experiment.cpl_scheme = cpl_scheme
        render_config_xml(context, experiment)
        aoscm.run_coupled_model()
        reduce_output(context.output_dir / experiment.exp_id, keep_debug_output=False)


def run_swr_experiments():
    experiment.exp_id = f"{exp_prefix}S"
    experiment.cpl_scheme = 0
    swr = SchwarzCoupling(experiment, context)
    swr.run(max_iters, rel_tol=1e-5)


if __name__ == "__main__":
    run_naive_experiments()

    run_swr_experiments()
