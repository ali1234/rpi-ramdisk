from pydo import *

from . import kernel, firmware, sysroot, packages

@command(consumes=[firmware.target])
def all():
    pass
