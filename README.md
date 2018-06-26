# RPi Ramdisk

Builds a raspbian-based ramdisk environment for Raspberry Pi.

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
                     multistrap fakeroot fakechroot proot cpio \
                     qemu-user binfmt-support makedev \
                     gtk-doc-tools valac

Some build dependencies need to be fairly new:

Git >= 2.12 is needed for "rev-parse --absolute-git-dir". It is available in
Ubuntu 17.10 and newer, or from this PPA if you are on an older release:

  https://launchpad.net/~git-core/+archive/ubuntu/ppa

Qemu >= 2.7 is needed for the getrandom() syscall. It is available in Ubuntu
17.10 and newer, or from the Ubuntu Cloud Archive:

  https://wiki.ubuntu.com/OpenStack/CloudArchive

## Keys

Multistrap/apt needs public keys to verify the repositories. You must import
the required keys into your local gpg keyring with the following commands:

    gpg --recv-key 9165938D90FDDD2E # raspbian-archive-keyring
    gpg --recv-key 82B129927FA3303E # raspberrypi-archive-keyring

You should take necessary steps to ensure that you have authentic versions of
these keys. Once received, rpi-ramdisk will export them as and when required.

On Ubuntu 16.04 you will also need to import these keys into the host apt
trusted keys with the following commands:

    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 9165938D90FDDD2E
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 82B129927FA3303E

You may also need to do this on Ubuntu 16.10, 17.04, 17.10.

## Submodules

This repository uses git submodules. After cloning the repository run:

    git submodule update --init

To pull changes from upstream run:

    git submodule update --remote
    git commit ...

You can also update individual repos manually:

    cd <repo> && git fetch && git checkout origin/master && cd ..
    git commit <repo>

## Compiling

Before compiling you need to select which image to build. The available configs
are in the `configs/` subdirectory. A good one to start with is rssread.config.
Select it by running `make rssreader.config` in the root of the repository.

Running `make` will now build everything. Parallel make e.g. `make -j8` is
supported and will greatly decrease the kernel build times.

The submodule build output is redirected to `/dev/null` by default. To show it
for the kernel:

    make VERBOSE_KERNEL_BUILD=1

You can also substitute "KERNEL" with "QT", "GSTREAMER", "RYGEL" etc for those
packages.

For faster kernel builds, ccache can be used. Install it first, then:

    make USE_CCACHE=1

To speed up initrd building, you can use apt-cacher-ng. Install it, and then:

    export APT_HTTP_PROXY=http://localhost:3142
    make

### Docker

Check the `Dockerfile` and `build-docker` scripts which automate the entire
build process.


## Booting

The build produces a boot/ directory containing everything needed to boot.
A boot.zip is also created. This is just a zipped copy of the boot directory.

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

Copy `bootcode.bin` to the fat partition on your SD card. Generate a dnsmasq
configuration with the correct paths:

    make dnsmasq.conf

Now run dnsmasq:

    sudo dnsmasq -C dnsmasq.conf

Now put the SD card in the Pi and boot. Wired ethernet must be connected.
You can leave dnsmasq running across rebuilds as the boot directory is
not deleted and recreated.

**Note**: TFTP booting is unreliable due to:

https://github.com/raspberrypi/firmware/issues/764

### USB device boot

Build rpiboot from:

https://github.com/raspberrypi/usbboot

Connect a Pi Zero or similar using a USB cable. Then run:

    sudo rpiboot -d boot

**Note**: Raspbian image may be too big to boot using this method, see:

https://github.com/raspberrypi/usbboot/issues/14

