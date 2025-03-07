# Experiment & Plotting Scripts for the AOSCM SWR Paper

Collection of Python scripts and Jupyter notebooks to run the EC-Earth AOSCM with different coupling algorithms and plot results.
Makes use of the [EC-Earth SCM tools package](https://github.com/valentinaschueller/ece-scm-coupling) to configure experiments and run the AOSCM with Schwarz waveform relaxation.

## 4d PAPA Experiments

- `papa_4d.py`: Run the 4d experiment with different model versions and choose whether to turn the mass flux scheme on or off
- `plot_papa_4d_convergence.ipynb`: Produces the convergence plot, Fig. 4 in the paper
- `plot_papa_4d.py`: Produces Fig. 6 in the paper
- `plot_papa_4d_mass_flux.ipynb`: Produces Fig. 7 in the paper

## 2d PAPA Experiments

- `papa_2d.py`: Runs the 112 2d experiments distributed throughout July 2014, using parallel, atmosphere-first, ocean-first, and SWR coupling schemes. For SWR: Termination criterion is used to stop the iterations. Only the last iteration is saved. Prints which experiments do not satisfy the criterion after 30 iterations.
- `papa_2d_nonconverged.py`: Modification of `nwp_ensemble.py` which only runs a subset of the above cases: Only SWR and only the dates where the termination criterion was not satisfied after 30 iterations. Now, 40 iterations are run and output from every iteration is saved to study the oscillations. 
- `plot_papa_2d_coupling_error.ipynb`: Produces Fig. 8 in the paper
- `plot_papa_2d_swr_iterations.ipynb`: Produces Fig. 3 in the paper
- `plot_papa_2d_oscillations.ipynb`: Produces plots showing oscillations for non-converged experiments (not part of the paper)

## 2d TOP Experiments

- `top_ensemble.py`: Runs the 84 2d experiments distributed throughout the YOPP targeted observation period, same principle as `nwp_ensemble.py`
- `plot_top_swr_iterations.ipynb`: Produces a figure similar to Fig. 3 for the TOP experiments
- `plot_top_version_comparison.ipynb`: Produces Figs. 9, 10 in the paper
- `plot_top_ensemble.ipynb`: Produces Fig. 11 in the paper
- `plot_top_coupling_error.ipynb`: Produces Fig. 12 in the paper
- `top_const_albedo_ensemble.py`: Runs the TOP ensemble for the case where the albedo parameterization returns a constant albedo and computes some simple statistics regarding the SWR termination


## Other files

- `helpers.py`: helper functions reused by different experiments
- `aoscm_runner.slurm`: slurm script to use when running the AOSCM on COSMOS
