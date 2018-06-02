# MPA*
Multi-Path A*

A path-planning algorithm for multiple nonintersecting paths.

## Install requirements:
```pip install -r requirements.txt```

## Run MPA*
```python fluid_multirouter.py```

Input new coordinates by modifying `fluid_multirouter.py` or by importing it and using appropriately - read the `test` function in `fluid_multirouter.py` for example usage.

## Profile MPA*
```python -m cProfile -o results.prof fluid_multirouter.py```

## View profiling results
Note that existing profiling results were taken in an Ubuntu VM on a system running a 4.0GHz i7 4790k. Discrepancies will exist for other setups.

```snakeviz results.prof```

See the writeup: lycarter.com/2018-06-02/meng-thesis