import pathlib

from pydo import *

this_dir = pathlib.Path(__file__).parent

package = {

    'requires': [],

    'sysroot_debs': ['libi2c-dev'],

    'root_debs': [],

    'target': this_dir / 'apds9960d.tar.gz',
    'install': ['{chroot} {stage} /bin/systemctl reenable apds9960d.service'],

}

from ... import sysroot, jobs

env = sysroot.env.copy()


prefix = '/opt/apds9960d'
stage = this_dir / 'stage'


repo = this_dir / 'apds9960d'
service = this_dir / 'apds9960d.service'
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


@command(produces=[package['target']], consumes=[service, sysroot.sysroot, sysroot.toolchain])
def build():
    call([
        f'rm -rf --one-file-system {stage} {builddir}',

        f'mkdir -p {builddir}',

        f'cd {builddir} && cmake {cmake_opts} {repo}',
        f'make -j{jobs} -C {builddir}',

        f'mkdir -p {stage}/etc/systemd/system',
        f'mkdir -p {stage}/{prefix}/bin',

        f'cp {service} {stage}/etc/systemd/system/',
        f'cp {builddir}/apds9960d {stage}/{prefix}/bin/',

        f'tar -C {stage} -czf {package["target"]} .',
    ], env=env, shell=True)


@command()
def clean():
    call([
        f'rm -rf --one-file-system {stage} {builddir} {package["target"]}',
    ])
