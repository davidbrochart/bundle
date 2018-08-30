# Bundle

Bundle is a hardware architecture designed to accelerate array computing on
FPGA.

Right now, the goal is to map this hardware to the [PYNQ-Z1](http://www.pynq.io)
board. On the software side, it uses `asyncio` to parallelize NumPy
computations.

The whole system can be simulated entirely in Python. For that I have created a
small Hardware Description Language called
[PyClk](https://github.com/davidbrochart/pyclk).

# Architecture

The hardware is intentionally kept simple, and consists of:
- memories: they are used to cache parts of the host arrays in the FPGA before
  making operations on them, and write parts of the result of these operations
to the host DDR memory.
- controllers: they handle who writes/reads the FPGA memories. Data can come
  from/go to the host DDR memory, or the FPGA operators (i.e. iterators +
functions).
- iterators: they stream data from FPGA memories, feed it to functions, and
  stream the function's result to another FPGA memory.
- functions: they take data in and produce a result, e.g. the sum of two
  numbers.
- a crossbar: it is the central piece which connects iterators to memories and
  functions.

The software is responsible for orchestrating the evaluation of an expression,
e.g. `a * b + c`. It breaks down the expression into a sequence of operations
(here `tmp = a * b` then `tmp + c`. It allocates FPGA memory for the evaluation,
copies parts of the data on the host DDR memory to the FPGA memory, schedules
operations, and copies back the result to the host DDR memory. Since the FPGA
can execute many operations in parallel, the scheduler uses asynchronous
programming (i.e. `asyncio`).

# Install

You will need PyClk to simulate the hardware:

`pip install git+https://github.com/davidbrochart/pyclk`

Bundle can be installed directly through GitHub: `pip install
git+https://github.com/davidbrochart/bundle`

Or you can clone this repository and `pip install -e bundle`
