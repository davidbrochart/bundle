# Bundle

Bundle is a hardware architecture designed to accelerate array computing on
FPGA.

Right now, the goal is to map this hardware to the [PYNQ-Z1](http://www.pynq.io)
board. On the software side, it uses `asyncio` to parallelize NumPy
computations.

The whole system can be simulated entirely in Python. For that I have created a
small Hardware Description Language called
[PyClk](https://github.com/davidbrochart/pyclk).

# Install

You will need PyClk to simulate the hardware:

`pip install git+https://github.com/davidbrochart/pyclk`

Bundle can be installed directly through GitHub: `pip install
git+https://github.com/davidbrochart/bundle`

Or you can clone this repository and `pip install -e bundle`
