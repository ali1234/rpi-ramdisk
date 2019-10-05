import os
import pathlib

from pydo import *

env = os.environ.copy()

try:
    env['http_proxy'] = os.environ['APT_HTTP_PROXY']
except KeyError:
    print("Don't forget to set up apt-cacher-ng")

this_dir = pathlib.Path(__file__).parent

firmware_rev = '1.20190620'
firmware_dir = this_dir / 'firmware'
firmware = download(firmware_dir, f'https://github.com/raspberrypi/firmware/archive/{firmware_rev}.zip')

stage = this_dir / 'stage'
target = this_dir / 'firmware.tar.gz'
sources = [this_dir / file for file in ['cmdline.txt', 'config.txt']]
msd = this_dir / 'usbboot' / 'msd' / 'start.elf'


@command(produces = [target], consumes = [*sources, msd, firmware])
def build():
    call([
        f'rm -rf --one-file-system {stage}',
        f'mkdir -p {stage}/boot',

        f'unzip -oj {firmware} */boot/* -x */boot/*.dtb */boot/kernel*.img */boot/overlays/* -d {stage}/boot/',

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
