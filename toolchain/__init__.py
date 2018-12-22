import pathlib

from pydo import *

this_dir = pathlib.Path(__file__).parent

ctng_src = this_dir / 'crosstool-ng'
ctng_prefix = this_dir / 'ctng'
ctng = ctng_prefix / 'bin' / 'ct-ng'
config = this_dir / 'x64-gcc-linaro-6.4-2018.05.config'
src = this_dir / 'src'
builddir = this_dir / 'build'
toolchain = this_dir / 'toolchain'

env = {
    'CT_LOCAL_TARBALLS_DIR': str(src),
    'CT_PREFIX_DIR': str(toolchain),
}


@command(produces=[ctng])
def build_ctng():
    call([
        f'git -C {ctng_src} clean -dfxq',
        f'cd {ctng_src} && ./bootstrap && ./configure --prefix={ctng_prefix}',
        f'make -j8 -C {ctng_src}',
        f'make -C {ctng_src} install',
    ], shell=True)


@command(produces=[toolchain], consumes=[ctng, config])
def build():
    call([
        f'mkdir -p {src}',
        f'mkdir -p {builddir}',
        f'cp {config} {builddir}/.config',
        f'cd {builddir} && {ctng} -e build',
    ], env=env, shell=True)


@command()
def clean():
    call([
        f'git -C {ctng_src} clean -dfxq',
        f'rm -rf --one-file-system {ctng_prefix} {builddir} {toolchain}',
    ])
