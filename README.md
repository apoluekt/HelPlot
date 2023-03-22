# HelPlot

Toolkit to make diagrams of helicity angles definitions for multibody decays

![helplot](https://user-images.githubusercontent.com/31311235/226939991-f62ad6f8-96d2-4bb3-b490-8a06d3beb60d.png)

## Contents

* `helplot.py` - Python module with definition of primitives
* `b2dstmunu_hel.py` - Example of helicity angles diagram in B->Dstar mu nu decays
* `b2dstdspi_dstpi_hel.py` - Example of helicity angles diagram in B->Dstar Ds pi decays via the resonance in Dstar pi channel
* `b2dstdspi_dspi_hel.py` - Example of helicity angles diagram in B->Dstar Ds pi decays via the resonance in Ds pi channel

## Requirements 

`python`, `numpy`, `scipy` and `matplotlib`. 

`latex` for LaTeX labels.

The environment can be set up with [`conda`](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) by
```bash
conda env create -f environment.yml
```
