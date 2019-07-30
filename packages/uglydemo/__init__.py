import pathlib

from pydo import *

this_dir = pathlib.Path(__file__).parent

package = {

    'requires': ['ugly'],

    'sysroot_debs': [],

    'root_debs': [],

    'target': this_dir / 'uglydemo.tar.gz',
    'install': ['{chroot} {stage} /bin/systemctl reenable uglydemo.service'],

}

from ... import sysroot

env = sysroot.env.copy()


prefix = '/opt/ugly'
stage = this_dir / 'stage'


service = this_dir / 'uglydemo.service'


@command(produces=[package['target']], consumes=[service])
def build():
    call([
        f'rm -rf --one-file-system {stage}',

        f'pip3 install --system --root={stage} --prefix={prefix} unicornhathd',

        f'mkdir -p {stage}/etc/systemd/system',
        f'cp {service} {stage}/etc/systemd/system/',

        f'tar -C {stage} --exclude=.{prefix}/doc --exclude=.{prefix}/include -czf {package["target"]} .',
    ], env=env, shell=True)


@command()
def clean():
    call([
        f'rm -rf --one-file-system {stage} {package["target"]}',
    ])
