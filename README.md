# Experiment & Plotting Scripts for the AOSCM SWR Paper

Collection of Python scripts and Jupyter notebooks to run the EC-Earth AOSCM with different coupling algorithms and plot results.
Makes use of the [EC-Earth SCM tools package](https://github.com/valentinaschueller/ece-scm-coupling) to configure experiments and run the AOSCM with Schwarz waveform relaxation.

## 4d PAPA Experiments

- `control_experiment.py`: Run the 4d experiment with different model versions and choose whether to turn the mass flux scheme on or off
- `plot_control_experiment_convergence.ipynb`: Produces the convergence plot, Fig. 4 in the paper
- `plot_control_experiment.py`: Produces Figs. 6, 7 in the paper
- `plot_mass_flux_comparison.ipynb`: Produces Fig. 8 in the paper
