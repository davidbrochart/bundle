import sys
sys.path.append('..')

from bundle import fpgapy as fp

a0 = fp.arange(10)
a1 = fp.ones_like(a0)
c = a0 + a1

print(c)
