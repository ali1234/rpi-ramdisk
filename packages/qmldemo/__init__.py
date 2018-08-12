import pathlib

from pydo import *

this_dir = pathlib.Path(__file__).parent

package = {
    'requires': ['qt'],
    'sysroot_debs': [],
    'root_debs': [],
    'target': this_dir / 'qmldemo.tar.gz',
    'install': ['{chroot} {stage} /bin/systemctl reenable qmldemo.service'],
}

from .. import qt

stage = this_dir / 'stage'
service = this_dir / 'qmldemo.service'
qml = this_dir / 'qmldemo.qml'

@command(produces=[package['target']], consumes=[service, qt.qmake])
def build():
    call([
        f'rm -rf --one-file-system {stage}',

        f'mkdir -p {stage}/etc/systemd/system',
        f'mkdir -p {stage}/{qt.prefix}/bin/',
        f'cp {service} {stage}/etc/systemd/system/',
        f'cp {qml} {stage}/{qt.prefix}/bin/',

        f'tar -C {stage} -czf {package["target"]} .',
    ])
