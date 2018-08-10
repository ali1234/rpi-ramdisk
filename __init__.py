from pydo import *

from . import firmware

@command(consumes=[firmware.target])
def all():
    pass
