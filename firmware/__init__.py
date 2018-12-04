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

sources = [this_dir / file for file in ['multistrap.conf', 'cmdline.txt', 'config.txt']]
copy = ' '.join(str(s) for s in sources)


@command(produces = [target], consumes = sources)
def build():
    call([
        f'rm -rf --one-file-system {stage}',

        f'mkdir -p {stage}/etc/apt/trusted.gpg.d/',
        f'gpg --export 82B129927FA3303E > {stage}/etc/apt/trusted.gpg.d/raspberrypi-archive-keyring.gpg',
        f'/usr/sbin/multistrap -d {stage} -f {sources[0]}',

        f'cp {copy} {stage}/boot/',

        f'tar -C {stage}/boot/ -czvf {target} .',
    ], env=env, shell=True)


@command()
def clean():
    call([
        f'rm -rf --one-file-system {stage} {target}'
    ])