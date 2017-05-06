# RPi Ramdisk

Builds two ramdisk environments for Raspberry Pi.

- **raspbian** is a full featured system based on Raspbian, including `apt`.

- **busybox-klibc** is a minimal tiny environment that is under 1MB.

The ramdisks are loaded fully into RAM at boot time, after which the SD card is
not touched. This means the SD card is extremely unlikely to become corrupted.
It also means any changes made on the live system are wiped after a reboot, so
the ramdisk must be customized for its task during the build process.


## Build Dependencies

### Debian-based systems

This dependency list may be incomplete. If so, please report a bug on github.

    sudo apt install libc6:i386 libstdc++6:i386 libgcc1:i386 \
                     libncurses5:i386 libtinfo5:i386 zlib1g:i386 \
                     build-essential git bc python zip wget gettext \
                     autoconf automake libtool pkg-config autopoint \
                     bison flex libglib2.0-dev gobject-introspection \
                     multistrap fakeroot fakechroot cpio \
                     qemu-user-static binfmt-support


### Docker

Check the `Dockerfile` and `build-docker` scripts which automate the entire
build process.

## Compiling

Running `make` will build everything. Parallel make e.g. `make -j8` is
supported and will greatly decrease the kernel build times.

The kernel build output is redirected to `/dev/null` by default. To show it:

    make VERBOSE_KERNEL_BUILD=1

For faster kernel builds, ccache can be used. Install it first, then:

    make USE_CCACHE=1

To speed up initrd building, you can use apt-cacher-ng. Install it, and then:

    export APT_HTTP_PROXY=http://localhost:3142
    make


## Booting

The build produces a boot directory for each environment. For example
`boot-raspbian/`. This directory contains everything needed to boot the
respective environment on any model of Raspberry Pi.

For each boot directory a boot zip is also created. For example
`boot-raspbian.zip`. This is just a zipped version of the boot directory.

### SD Card

The SD card first primary partition should be fat formatted. (This is the
default for new, blank SD cards.) Copy the contents of the boot directory onto
the fat partition on the SD card. Put the SD card in the Raspberry Pi and turn
it on.

### USB Mass Storage

USB mass storage booting must be enabled first:

https://www.raspberrypi.org/documentation/hardware/raspberrypi/bootmodes/msd.md

Then the procedure is the same as SD card booting: copy the contents of the
boot directory to the mass storage device, plug it in, and turn on.

### TFTP Boot

Copy `bootcode.bin` to the fat partition on your SD card. Edit `dnsmasq.conf`
and change the tftpboot path to contain the absolute path to the boot directory
and then run `sudo dnsmasq -C dnsmasq.conf`. Now put the SD card in the Pi and
boot. Wired ethernet must be connected.

**Note**: TFTP booting is unreliable due to:

https://github.com/raspberrypi/firmware/issues/764

### USB device boot

Build rpiboot from:

https://github.com/raspberrypi/usbboot

Connect a Pi Zero or similar using a USB cable. Then run:

    sudo rpiboot -d boot-busybox-klibc

**Note**: Raspbian image is too big to boot using this method, see:

https://github.com/raspberrypi/usbboot/issues/14

