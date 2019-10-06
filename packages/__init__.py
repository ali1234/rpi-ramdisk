import importlib

from collections import OrderedDict

from pydo import *

from .. import config


def package_walk(name, result, seen):
    if name in seen:
        return
    seen.add(name)
    mod = importlib.import_module('.'+name, package=__package__)
    for r in mod.package['requires']:
        package_walk(r, result, seen)
    result[name] = mod


packages = OrderedDict()
for p in config.packages:
    package_walk(p, packages, set())


@command()
def list():
    print('Enabled packages:', ', '.join(packages.keys()))


@command()
def clean():
    for m in packages.values():
        m.clean()


@command()
def build():
    for m in packages.values():
        m.build()
