import pathlib

from pydo import *

from . import kernel, firmware, raspbian, sysroot, packages

this_dir = pathlib.Path(__file__).parent

kernel_boot_tarballs = [k.boot for k in kernel.kernels]
boot = this_dir / 'boot'
dnsmasq_conf_in = this_dir / 'dnsmasq.conf.in'
dnsmasq_conf = this_dir / 'dnsmasq.conf'


@command(produces=[dnsmasq_conf], consumes=[dnsmasq_conf_in])
def build_dnsmasq_conf():
    subst(dnsmasq_conf_in, dnsmasq_conf, {'@TFTP_ROOT@': str(boot)})


@command(produces=[boot], consumes=[firmware.target, raspbian.initrd, *kernel_boot_tarballs, dnsmasq_conf])
def build():
    call([
        f'mkdir -p {boot}',
        f'rm -rf --one-file-system {boot}/*',
        f'cp {raspbian.initrd} {boot}',
        f'tar -xf {firmware.target} -C {boot}',
        *list(f'tar -xf {kb} -C {boot}' for kb in kernel_boot_tarballs),
        #f'cd {boot} && zip -qr {boot} *',
        f'touch {boot}',
    ], shell=True)


@command()
def clean():
    sysroot.clean()
    firmware.clean()
    kernel.clean()
    raspbian.clean()
    packages.clean()
