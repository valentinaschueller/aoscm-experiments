# Experiment & Plotting Scripts for the AOSCM SWR Paper

Collection of Python scripts and Jupyter notebooks to run the EC-Earth AOSCM with different coupling algorithms and plot results.
Makes use of the [EC-Earth SCM tools package](https://github.com/valentinaschueller/ece-scm-coupling) to configure experiments and run the AOSCM with Schwarz waveform relaxation.

## 4d PAPA Experiments

- `control_experiment.py`: Run the 4d experiment with different model versions and choose whether to turn the mass flux scheme on or off
- `plot_control_experiment_convergence.ipynb`: Produces the convergence plot, Fig. 4 in the paper
- `plot_control_experiment.py`: Produces Figs. 6, 7 in the paper
- `plot_mass_flux_comparison.ipynb`: Produces Fig. 8 in the paper

## 2d PAPA Experiments

- `nwp_ensemble.py`: Runs the 112 2d experiments distributed throughout July 2014, using parallel, atmosphere-first, ocean-first, and SWR coupling schemes. For SWR: Termination criterion is used to stop the iterations. Only the last iteration is saved. Prints which experiments do not satisfy the criterion after 30 iterations.
- `nwp_nonconverged.py`: Modification of `nwp_ensemble.py` which only runs a subset of the above cases: Only SWR and only the dates where the termination criterion was not satisfied after 30 iterations. Now, 40 iterations are run and output from every iteration is saved to study the oscillations. 
- `plot_nwp_coupling_error.ipynb`: Produces Fig. 9 in the paper
- `plot_nwp_swr_iterations.ipynb`: Produces Fig. 3 in the paper
- `plot_nwp_oscillations.ipynb`: Produces plots showing oscillations for non-converged experiments (not part of the paper)
