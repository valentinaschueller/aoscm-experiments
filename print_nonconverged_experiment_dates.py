from pathlib import Path

from ruamel.yaml import YAML

output_dir = Path("output/ensemble_output")

experiment_directories = []
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
    for experiment_dir in date_dir.glob("*"):
        experiment_directories.append(experiment_dir)

print(f"Number of Experiments: {int(len(experiment_directories) / 4)}")

print([str(dir)[23:36] for dir in experiment_directories[::4]])
