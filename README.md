Abelian sandpile
================

This code allows to create, grow and visualize Abelian sandpiles.

![Example sandplie](https://www.pawelmandera.com/assets/sandpile/sandpile-000009995000.png)

For the description of the model see
[wiki](https://en.wikipedia.org/wiki/Abelian_sandpile_model) or p. 52-53 in Bak
(1996).

Setup
-----

Install requirenemtns and build Cython code to make it run signingicantly
faster.

```bash
pip install -r requirements.txt
python setup.py build_ext --inplace
```
Usage
-----

Pour sand on the sandpile and save the sandpile after each 1000 grains.

```bash
./sandpile_main.py pour --verbose \
  --grid_size 200 --n_steps 1e5 --checkpoint_every 1e3 \
  --checkpoint_dir ./checkpoints  --store_avalanche_sizes
```
Plot the sandpile grid.

```bash
./sandpile_main.py plot \
  ./checkpoints/sandpile-000007470000.pckl.gz ./data/plots/ 
```

References
----------

Bak, P. (1996). How Nature Works: The Science of Self-Organized Criticality. New
York: Copernicus.
