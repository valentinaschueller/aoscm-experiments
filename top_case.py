import pandas as pd
from AOSCMcoupling.experiment import Experiment
from AOSCMcoupling.helpers import AOSCM, compute_nstrtini
from AOSCMcoupling.schwarz_coupling import SchwarzCoupling

from helpers import AOSCMVersion, get_context

context = get_context(AOSCMVersion.ECE43, "top_case")

max_iters = 30
exp_id = "TC43"

start_date = pd.Timestamp("2020-04-12")
simulation_duration = pd.Timedelta(2, "days")
ifs_input_start_date = pd.Timestamp("2020-04-12")
ifs_input_freq = pd.Timedelta(1, "hours")
nstrtini = compute_nstrtini(
    start_date, ifs_input_start_date, int(ifs_input_freq.seconds / 3600)
)

if context.model_version == 3:
    ice_model = "lim"
else:
    ice_model = "si3"

experiment = Experiment(
    dt_cpl=3600,
    dt_ifs=900,
    dt_nemo=900,
    dt_ice=900,
    exp_id="",
    ifs_leocwa=False,
    with_ice=True,
    nem_input_file=context.data_dir
    / "nemo_from_CMEMS"
    / f"nemo_restart_{start_date.date()}.nc",
    ice_input_file=context.data_dir
    / "nemo_from_CMEMS"
    / f"{ice_model}_restart_{start_date.date()}.nc",
    ifs_input_file=context.data_dir / "MOS6merged.nc",
    oasis_rstas=context.data_dir
    / "rstas_from_AMIP"
    / f"rstas_{start_date.date()}_{start_date.time().hour:02}.nc",
    oasis_rstos=context.data_dir / "rstos_from_CMEMS" / f"rstos_{start_date.date()}.nc",
    run_start_date=start_date,
    run_end_date=start_date + simulation_duration,
    ifs_nstrtini=nstrtini,
    ifs_levels=137,
)


def run_parallel_schwarz():
    experiment.exp_id = exp_id
    experiment.cpl_scheme = 0
    schwarz_exp = SchwarzCoupling(experiment, context)
    schwarz_exp.run(max_iters, rel_tol=1e-5)


if __name__ == "__main__":

    run_parallel_schwarz()
