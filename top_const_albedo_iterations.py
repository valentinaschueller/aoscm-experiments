from pathlib import Path

import numpy as np
import xarray as xr
from ruamel.yaml import YAML

ensemble_directory = Path("/home/vschuller/experiments/output/const_alb_ensemle")
schwarz_directories = []
yaml = YAML(typ="unsafe", pure=True)
for date_dir in ensemble_directory.glob("*"):
    if date_dir.is_dir():
        schwarz_directories.append(date_dir / "swr")
experiments = []
non_converged_counter = 0
for schwarz_dir in schwarz_directories:
    with open(schwarz_dir / "setup_dict.yaml") as yaml_file:
        experiment = yaml.load(yaml_file)
        converged = experiment.iterate_converged["inf-norm"]
        if converged:
            experiments.append(experiment)
        else:
            non_converged_counter += 1

iterations = np.array([experiment.iteration for experiment in experiments])
# start_dates = np.array([schwarz_dict["run_start_date"] for schwarz_dict in schwarz_dicts])
iterations = xr.DataArray(iterations, name="iterations")

print(f"Not converged: {non_converged_counter}")
print(f"Mean: {float(iterations.mean())}")
print(f"Median: {float(iterations.median())}")
print(f"Max: {float(iterations.max())}")
