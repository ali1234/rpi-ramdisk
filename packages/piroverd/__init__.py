import pathlib

from pydo import *

this_dir = pathlib.Path(__file__).parent

package = {

    'requires': ['gstreamer'],

    'sysroot_debs': ['libi2c-dev'],

    'root_debs': [],

    'target': this_dir / 'piroverd.tar.gz',
    'install': ['{chroot} {stage} /bin/systemctl reenable piroverd.service'],

}

from ... import sysroot
from .. import gstreamer

env = gstreamer.env.copy()


prefix = '/opt/piroverd'
stage = this_dir / 'stage'


# add stage to the paths. every package which uses this env should do this (ie rygel).
env['PKG_CONFIG_LIBDIR'] += ':' + str(stage / prefix[1:] / 'lib/pkgconfig')
env['XDG_DATA_DIRS'] += ':' + str(stage / prefix[1:] / 'share')

repo = this_dir / 'piroverd'
service = this_dir / 'piroverd.service'
builddir = this_dir / 'build'


cmake_opts = ' '.join([
    '-DCMAKE_SYSTEM_NAME=Linux',
    f'-DCMAKE_C_COMPILER=arm-linux-gnueabihf-gcc',
    f'-DCMAKE_CXX_COMPILER=arm-linux-gnueabihf-g++',
    f'-DCMAKE_SYSROOT={sysroot.sysroot}',
    '-DCMAKE_FIND_ROOT_PATH_MODE_PROGRAM=NEVER',
    '-DCMAKE_FIND_ROOT_PATH_MODE_INCLUDE=ONLY',
    '-DCMAKE_FIND_ROOT_PATH_MODE_LIBRARY=ONLY',
])


@command(produces=[package['target']], consumes=[service, gstreamer.package['target']])
def build():
    call([
        f'rm -rf --one-file-system {stage} {builddir}',

        f'mkdir -p {builddir}',

        f'cd {builddir} && cmake {cmake_opts} {repo}',
        f'make -j8 -C {builddir}',

        f'mkdir -p {stage}/etc/systemd/system',
        f'mkdir -p {stage}/{prefix}/bin',

        f'cp {service} {stage}/etc/systemd/system/',
        f'cp {builddir}/piroverd {stage}/{prefix}/bin/',

        f'tar -C {stage} -czf {package["target"]} .',
    ], env=env, shell=True)


@command()
def clean():
    call([
        f'rm -rf --one-file-system {stage} {builddir} {package["target"]}',
    ])
