import os
import pathlib

from pydo import *

env = os.environ.copy()

try:
    env['http_proxy'] = os.environ['APT_HTTP_PROXY']
except KeyError:
    print("Don't forget to set up apt-cacher-ng")

this_dir = pathlib.Path(__file__).parent

stage = this_dir / 'stage'
target = this_dir / 'firmware.tar.gz'

firmware = this_dir / 'firmware'

sources = [this_dir / file for file in ['cmdline.txt', 'config.txt']]
sources.extend([f for f in (firmware / 'boot').glob('*') if not f.name.endswith('.dtb') and not f.name == 'overlays'])

msd = this_dir / 'usbboot' / 'msd' / 'start.elf'


@command(produces = [target], consumes = sources + [msd])
def build():
    call([
        f'rm -rf --one-file-system {stage}',
        f'mkdir -p {stage}/boot',

        f'cp {" ".join(str(s) for s in sources)} {stage}/boot/',

        f'cp {msd} {stage}/boot/msd.elf',
        f'touch {stage}/boot/UART',

        f'tar -C {stage}/boot/ -czvf {target} .',
    ], env=env)


@command()
def clean():
    call([
        f'rm -rf --one-file-system {stage} {target}'
    ])
