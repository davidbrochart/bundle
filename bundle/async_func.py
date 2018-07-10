from .fpga_func import *

def set_fpga(f):
    set_fpga_(f)

event_loop = None
def set_event_loop(loop):
    global event_loop
    event_loop = loop

def async_add(a0, a1, res):
    op = set_add(a0, a1)
    return event_loop.create_task(get_add(op, res))
