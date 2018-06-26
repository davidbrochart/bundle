Bundle is a hardware architecture designed to accelerate array computing.

Right now, the goal is to map this hardware to the [PYNQ-Z1](http://www.pynq.io) board. On the software side, it uses [Dask](https://dask.pydata.org) to parallelize and schedule NumPy computations.

The whole system can be simulated entirely in Python. For that I have created a small Hardware Description Language called [PyClk](https://github.com/davidbrochart/pyclk).
