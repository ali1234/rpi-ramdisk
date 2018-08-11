import os
import pathlib

from pydo import *

from .. import packages, kernel

env = os.environ.copy()

this_dir = pathlib.Path(__file__).parent

try:
    env['http_proxy'] = os.environ['APT_HTTP_PROXY']
except KeyError:
    print("Don't forget to set up apt-cacher-ng")


multistrap_conf = this_dir / 'multistrap.conf'
multistrap_conf_in = this_dir / 'multistrap.conf.in'
overlay = this_dir / 'overlay'
stage = this_dir / 'stage'
initrd = this_dir / 'initrd'
excludes = this_dir / 'excludes.conf'
cleanup = this_dir / 'cleanup'
chroot = 'proot -0 -q qemu-arm -w / -r'
kernel_root_tarballs = [k.root for k in kernel.kernels]
package_tarballs = [p.package['target'] for p in packages.packages.values()]

def package_install_actions():
    for p in packages.packages.values():
        for a in p.package['install']:
            yield a.format(**locals(), **globals())


@command(produces=[multistrap_conf], consumes=[multistrap_conf_in], always=True)
def build_multistrap_conf():
    all_root_debs = sorted(set.union(*(set(p.package['root_debs']) for p in packages.packages.values()), set()))
    multistrap_packages = textwrap(all_root_debs, prefix='packages=')
    subst(multistrap_conf_in, multistrap_conf, {'@PACKAGES@': multistrap_packages})


@command(
    produces=[initrd],
    consumes=[
        multistrap_conf,
        *dir_scan(overlay),
        *kernel_root_tarballs,
        *package_tarballs,
        excludes,
    ])
def build():
    call([
        f'rm -rf --one-file-system {stage}',

        f'mkdir -p {stage}/etc/apt/trusted.gpg.d/',
        f'gpg --export 82B129927FA3303E > {stage}/etc/apt/trusted.gpg.d/raspberrypi-archive-keyring.gpg',
        f'gpg --export 9165938D90FDDD2E > {stage}/etc/apt/trusted.gpg.d/raspbian-archive-keyring.gpg',
        f'/usr/sbin/multistrap -d {stage} -f {multistrap_conf}',

        # run preinst scripts
        f'for script in {stage}/var/lib/dpkg/info/*.preinst; do \
            [ "$script" = "{stage}/var/lib/dpkg/info/vpnc.preinst" ] && continue; \
            echo "I: run preinst script ${{script##{stage}}}"; \
            DPKG_MAINTSCRIPT_NAME=preinst \
            DPKG_MAINTSCRIPT_PACKAGE="`basename $script .preinst`" \
            {chroot} {stage} ${{script##{stage}}} install; \
            done',

        # don't run makedev
        # we will create device nodes later, after we are done with the system dev
        f'rm -f {stage}/var/lib/dpkg/info/makedev.postinst',

        # work around https://pad.lv/1727874
        f'rm -f {stage}/var/lib/dpkg/info/raspbian-archive-keyring.postinst',
        f'ln -sf /usr/share/keyrings/raspbian-archive-keyring.gpg {stage}/etc/apt/trusted.gpg.d/',

        # work around PAM error
        f'ln -s -f /bin/true {stage}/usr/bin/chfn',

        # configure packages
        f'DEBIAN_FRONTEND=noninteractive DEBCONF_NONINTERACTIVE_SEEN=true \
            LC_ALL=C LANGUAGE=C LANG=C {chroot} {stage} /usr/bin/dpkg --configure -a || true',

        # initialize /etc/fstab
        f'echo proc /proc proc defaults 0 0 > {stage}/etc/fstab',

        # hostname
        f'echo rpi-ramdisk > {stage}/etc/hostname',

        # delete root password
        f'{chroot} {stage} passwd -d root',

        # remove excluded files that multistrap missed
        f'{cleanup} {stage} {excludes}',
        f'mkdir -p {stage}/etc/dpkg/dpkg.conf.d/',
        f'cp {excludes} {stage}/etc/dpkg/dpkg.conf.d/',

        # update hwdb after cleaning
        f'{chroot} {stage} udevadm hwdb --update --usr',

        # modules
        *list(f'tar -xf {kr} -C {stage}' for kr in kernel_root_tarballs),

        # packages
        *list(f'tar -xf {pkg} -C {stage}' for pkg in package_tarballs),
        *list(package_install_actions()),

        # overlay
        f'cp -r {overlay}/* {stage}',

        # ldconfig
        f'{stage}/sbin/ldconfig -r {stage}',

        # network setup

        # reset default udev persistent-net rule
        f'rm -f {stage}/etc/udev/rules.d/*_persistent-net.rules',

        # /etc/resolv.conf symlink
        f'ln -sf /run/systemd/resolve/resolv.conf {stage}/etc/resolv.conf',

        # enable network services
        f'{chroot} {stage} /bin/systemctl reenable systemd-networkd',
        f'{chroot} {stage} /bin/systemctl reenable systemd-resolved',
        f'{chroot} {stage} /bin/systemctl reenable systemd-timesyncd',
        f'{chroot} {stage} /bin/systemctl reenable systemd-networkd-wait-online.service',
        f'{chroot} {stage} /bin/systemctl reenable wpa_supplicant@wlan0.service',

        # time used by timesyncd if no other is available
        f'touch {stage}/var/lib/systemd/clock',

        # mtab
        f'ln -sf /proc/mounts {stage}/etc/mtab',

        # this must be done last. if the fakeroot devices exist on the system,
        # chroot wont be able to read from them, which breaks systemd setup.
        f'cd {stage}/dev && fakeroot /sbin/MAKEDEV std',

        # pack rootfs into initrd
        f'{chroot} {stage} sh -c "cd / && find * -xdev -not \( \
                  -path host-rootfs -prune \
                  -path run -prune \
                  -path proc -prune \
                  -path sys -prune \
                  -path boot -prune \
               \) | cpio --create -H newc" | xz -C crc32 -9 > {initrd}'

    ], shell=True)