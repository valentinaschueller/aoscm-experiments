# PAPA 2d ensemble results, `LECUMF=.false.`

Question: What results do we get for the coupling error when turning off the mass flux scheme?
Answer: 
- The maximum observed coupling errors for $T^a$ and SST are significantly lower. 
- If `LECUMF=.false.`, it looks like both sequential algorithms are better than the parallel algorithm even for atmospheric variables. 
- Depending on how one interprets the plots, one might even conclude that atmosphere-first could be a better choice than ocean-first algorithm. However, this result is not clear in the way it is clear for the SST that atmosphere-first is the obvious best choice.

Experiment description:
Run `nwp_ensemble(with_mass_flux=False)` in `nwp_ensemble.py`. We have only tested this for the EC-Earth 3 AOSCM (OpenIFS SCM cy40r1 coupled to NEMO 3.6).

Then, use `papa_2d_ensemble_nomf_plots.ipynb` to compute maximum coupling errors and create the plot `papa_2d_ensemble_nomf_relative_error_bar.png`.

|              | Maximum errors | (values with `LECUMF=.true.`) |
|--------------|----------------|-------------------------------|
| e_max(SST):  | 0.20 °C        | (0.58 °C)                     |
| e_max(T^a):  | 0.81 °C        | (3.66 °C)                     |
| e_max(q):    | 1.81 g/kg      | (1.99 g/kg)                   |
