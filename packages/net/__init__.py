import pathlib

from pydo import *

this_dir = pathlib.Path(__file__).parent

package = {

    'requires': [],

    'sysroot_debs': [],

    'root_debs': [
        'net-tools', 'wpasupplicant', 'crda', 'firmware-brcm80211', 'ca-certificates', 'openssl',
    ],

    'target': this_dir / 'net.tar.gz',
    'install': [
        # /etc/resolv.conf symlink
        'ln -sf /run/systemd/resolve/resolv.conf {stage}/etc/resolv.conf',

        # enable network services
        '{chroot} {stage} /bin/systemctl reenable systemd-networkd',
        '{chroot} {stage} /bin/systemctl reenable systemd-resolved',
        '{chroot} {stage} /bin/systemctl reenable systemd-timesyncd',
        '{chroot} {stage} /bin/systemctl reenable systemd-networkd-wait-online.service',
        '{chroot} {stage} /bin/systemctl reenable wpa_supplicant@wlan0.service',
    ],

}

stage = this_dir / 'stage'

en = this_dir / 'en.network'
wl = this_dir / 'wlan0.network'
wpa = this_dir / 'wpa_supplicant@.service'


@command(produces=[package['target']], consumes=[en, wl, wpa])
def build():
    call([
        f'rm -rf --one-file-system {stage}',

        f'mkdir -p {stage}/etc/systemd/network',
        f'mkdir -p {stage}/etc/systemd/system',

        f'cp {en} {wl} {stage}/etc/systemd/network/',
        f'cp {wpa} {stage}/etc/systemd/system/',

        f'tar -C {stage} -czf {package["target"]} .'
    ])


@command()
def clean():
    call([f'rm -rf --one-file-system {stage} {package["target"]}'])
