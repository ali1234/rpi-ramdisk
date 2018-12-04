import os
import pathlib

from pydo import *


class Kernel(object):

    def __init__(self, name, dir, env):
        self.name = name
        self.dir = dir
        self.env = env
        self.build = command(
            produces=[self.boot, self.root],
            consumes=[self.config, *git_repo_scan(self.repo, self.dir / 'tools')]
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
            f'make -j8 -C {self.repo} zImage modules dtbs',

            f'mkdir -p {self.stage}/root {self.stage}/boot/overlays',
            f'make -j8 -C {self.repo} INSTALL_MOD_PATH={self.stage}/root modules_install',

            f'cp {self.repo}/arch/arm/boot/zImage {self.stage}/boot/{self.name}.img',
            f'cp {self.repo}/arch/arm/boot/dts/*.dtb {self.stage}/boot/',
            f'cp {self.repo}/arch/arm/boot/dts/overlays/*.dtb* {self.stage}/boot/overlays/',
            f'cp {self.repo}/arch/arm/boot/dts/overlays/README {self.stage}/boot/overlays/',

            f'tar -C {self.stage}/root/ -czf {self.root} .',
            f'tar -C {self.stage}/boot/ -czf {self.boot} .',

        ], env=self.env, shell=True)


env = os.environ.copy()
env['ARCH'] = 'arm'
env['CROSS_COMPILE'] = '../tools/arm-bcm2708/gcc-linaro-arm-linux-gnueabihf-raspbian/bin/arm-linux-gnueabihf-'

this_dir = pathlib.Path(__file__).parent


kernels = [Kernel(k, this_dir, env) for k in ['kernel', 'kernel7']]


@command()
def build():
    for k in kernels:
        k.build()


@command()
def clean():
    for k in kernels:
        call([
            f'rm -rf --one-file-system {k.stage} {k.root} {k.boot}'
        ])
