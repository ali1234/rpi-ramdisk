import pathlib

from pydo import *

this_dir = pathlib.Path(__file__).parent

services = ['piratepython.service', 'pp-restart.service', 'pp-restart.path']

package = {

    'requires': ['pymtpd'],

    'sysroot_debs': [],

    'root_debs': [

        'python3',

        # support
        'pigpio', 'python3-pigpio', 'python3-w3lib', 'python3-serial', 'python3-tweepy', 'python3-spur',
        'python3-netifaces', 'python3-zeroconf', 'python3-six',
        'python3-gpiozero', 'python3-flask', 'python3-pil', 'python3-picamera',

        # pimoroni
        'python3-blinkt', 'python3-phatbeat', 'python3-scrollphat', 'python3-scrollphathd', 'python3-unicornhathd',
        'python3-automationhat', 'python3-explorerhat', 'python3-envirophat', 'python3-motephat',
        'python3-touchphat', 'python3-pianohat', 'python3-drumhat', 'python3-rainbowhat', 'python3-fourletterphat',
        'python3-pantilthat', 'python3-buttonshim', 'python3-microdotphat',

    ],

    'target': this_dir / 'piratepython.tar.gz',
    'install': [f'{{chroot}} {{stage}} /bin/systemctl reenable {service}' for service in services],

}

from ... import sysroot

env = sysroot.env.copy()

stage = this_dir / 'stage'
main = this_dir / 'main.py'
service_files = [this_dir / s for s in services]

@command(produces=[package['target']], consumes=service_files + [main, sysroot.toolchain, sysroot.sysroot])
def build():
    call([
        f'rm -rf --one-file-system {stage}',
        f'mkdir -p {stage}/mtp',
        f'cp {main} {stage}/mtp',
        f'mkdir -p {stage}/etc/systemd/system',
        f'cp {" ".join(str(s) for s in service_files)} {stage}/etc/systemd/system/',
        f'tar -C {stage} -czf {package["target"]} .',
    ], env=env, shell=True)


@command()
def clean():
    call([
        f'rm -rf --one-file-system {stage} {package["target"]}',
    ])
