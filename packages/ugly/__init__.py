import pathlib

from pydo import *

this_dir = pathlib.Path(__file__).parent

package = {

    'requires': [],

    'sysroot_debs': [],

    'root_debs': ['python3'],

    'target': this_dir / 'ugly.tar.gz',
    'install': [],

}

from ... import sysroot

env = sysroot.env.copy()


prefix = '/opt/ugly'
stage = this_dir / 'stage'


repo = this_dir / 'ugly'
builddir = this_dir / 'build'


@command(produces=[package['target']], consumes=[sysroot.toolchain, sysroot.sysroot])
def build():
    call([
        f'rm -rf --one-file-system {stage}',

        f'cd {repo} && pip3 install --system --root={stage} --prefix={prefix} .',

        f'tar -C {stage} --exclude=.{prefix}/doc --exclude=.{prefix}/include -czf {package["target"]} .',
    ], env=env, shell=True)


@command()
def clean():
    call([
        f'rm -rf --one-file-system {stage} {package["target"]}',
    ])
