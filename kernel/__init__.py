import os
import pathlib

from pydo import *

from ..sysroot import toolchain
from .. import jobs


class Kernel(object):

    def __init__(self, name, dir, env):
        self.name = name
        self.dir = dir
        self.env = env
        self.build = command(
            produces=[self.boot, self.root],
            consumes=[toolchain, self.config]
        )(self._build)

    @property
    def repo(self):
        return self.dir / 'linux'

    @property
    def stage(self):
        return self.dir / 'stage'

    @property
    def root(self):
        return self.dir / (self.name + '-root.tar.gz')

    @property
    def boot(self):
        return self.dir / (self.name + '-boot.tar.gz')

    @property
    def config(self):
        return self.dir / (self.name + '.config')

    def _build(self):
        call([

            f'git -C {self.repo} clean -dfxq',
            f'rm -rf --one-file-system {self.stage}',

            f'cp {self.config} {self.repo}/.config',
            f'make -j{jobs} -C {self.repo} zImage modules dtbs',

            f'mkdir -p {self.stage}/root {self.stage}/boot/overlays',
            f'make -j{jobs} -C {self.repo} INSTALL_MOD_PATH={self.stage}/root modules_install',

            f'cp {self.repo}/arch/arm/boot/zImage {self.stage}/boot/{self.name}.img',
            f'cp {self.repo}/arch/arm/boot/dts/*.dtb {self.stage}/boot/',
            f'cp {self.repo}/arch/arm/boot/dts/overlays/*.dtb* {self.stage}/boot/overlays/',
            f'cp {self.repo}/arch/arm/boot/dts/overlays/README {self.stage}/boot/overlays/',

            f'tar -C {self.stage}/root/ -czf {self.root} .',
            f'tar -C {self.stage}/boot/ -czf {self.boot} .',

        ], env=self.env, shell=True)

    def update_config(self):
        call([
            f'make -C {self.repo} mrproper',
            f'cp {self.config} {self.repo}/.config',
            f'make -C {self.repo} oldconfig',
            f'cp {self.repo}/.config {self.config}',
        ], env=self.env, interactive=True)


    def update_config(self):
        call([
            f'make -C {self.repo} mrproper',
            f'cp {self.config} {self.repo}/.config',
            f'make -C {self.repo} menuconfig',
            f'cp {self.repo}/.config {self.config}',
        ], env=self.env, interactive=True)


env = os.environ.copy()
env['ARCH'] = 'arm'
env['CROSS_COMPILE'] = f'{toolchain}/bin/arm-linux-gnueabihf-'

this_dir = pathlib.Path(__file__).parent


kernels = [Kernel(k, this_dir, env) for k in ['kernel', 'kernel7', 'kernel7l']]


@command()
def build():
    for k in kernels:
        k.build()


@command()
def update_configs():
    for k in kernels:
        k.update_config()


@command()
def menu_configs():
    for k in kernels:
        k.update_config()


@command()
def clean():
    for k in kernels:
        call([
            f'rm -rf --one-file-system {k.stage} {k.root} {k.boot}'
        ])
