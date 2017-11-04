Abelian sandpile
================

This code allows to create, grow and visualize Abelian sandpiles.

![Example sandplie](https://www.pawelmandera.com/assets/sandpile/sandpile-000009995000.png)

Setup
-----

```bash
pip install -r requirements.txt
```

Usage
-----

Pour sand on the sandpile.

```bash
./sandpile_main.py pour --verbose \
  --grid_size 200 --n_steps 1e5 --checkpoint_every 1e3 \
  --checkpoint_dir ./checkpoints  --store_avalanche_sizes
```
Plot the sandpile.

```bash
./sandpile_main.py plot \
  ./checkpoints/sandpile-000007470000.pckl.gz ./data/plots/ 
```
