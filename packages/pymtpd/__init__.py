import pathlib

from pydo import *

this_dir = pathlib.Path(__file__).parent

package = {

    'requires': [],

    'sysroot_debs': [],

    'root_debs': ['python3', 'libaio1'],

    'target': this_dir / 'pymtpd.tar.gz',
    'install': ['{chroot} {stage} /bin/systemctl reenable pymtpd.service'],

}

from ... import sysroot

env = sysroot.env.copy()


prefix = '/opt/pymtpd'
stage = this_dir / 'stage'


repo = this_dir / 'pymtpd'
service = this_dir / 'pymtpd.service'
builddir = this_dir / 'build'


@command(produces=[package['target']], consumes=[service, sysroot.toolchain, sysroot.sysroot])
def build():
    call([
        f'rm -rf --one-file-system {stage}',

        f'cd {repo} && python3.7 -m pip install --system --root={stage} --prefix={prefix} .',

        f'mkdir -p {stage}/etc/systemd/system',
        f'cp {service} {stage}/etc/systemd/system/',

        f'tar -C {stage} --exclude=.{prefix}/doc --exclude=.{prefix}/include -czf {package["target"]} .',
    ], env=env, shell=True)


@command()
def clean():
    call([
        f'rm -rf --one-file-system {stage} {package["target"]}',
    ])
