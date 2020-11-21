# RPi Ramdisk

Builds a raspbian-based ramdisk environment for Raspberry Pi.

The ramdisks are loaded fully into RAM at boot time, after which the SD card is
not touched. This means the SD card is extremely unlikely to become corrupted.
It also means any changes made on the live system are wiped after a reboot, so
the ramdisk must be customized for its task during the build process.


## Build Dependencies

### Pydo

rpi-ramdisk uses a build tool called pydo which has been developed specifically
to handle complex builds which don't produce executables and libraries. You must
first download and install it:

    git clone git://github.com/ali1234/pydo
    cd pydo && pip3 install .

### System packages

rpi-ramdisk uses multistrap to collect packages. multistrap requires apt and
as such is only supported on Debian based systems. It may be possible to use
it on other distributions, but this has not been tested.

In addition you need the following packages to build rpi-ramdisk:

For Ubuntu 18.04:

    sudo apt install libc6:i386 libstdc++6:i386 libgcc1:i386 \
                     libncurses5:i386 libtinfo5:i386 zlib1g:i386 \
                     build-essential git bc python zip wget gettext \
                     autoconf automake libtool pkg-config autopoint \
                     bison flex libglib2.0-dev gobject-introspection \
                     multistrap fakeroot fakechroot proot cpio \
                     qemu-user binfmt-support makedev \
                     gtk-doc-tools valac python3.7-minimal

This dependency list may be incomplete. If so, please report a bug on github.

Some build dependencies need to be fairly new:

Git >= 2.12 is needed for "rev-parse --absolute-git-dir". It is available in
Ubuntu 17.10 and newer, or from this PPA if you are on an older release:

  https://launchpad.net/~git-core/+archive/ubuntu/ppa

Qemu >= 3.1 is needed for the getrandom() syscall. It is available in Ubuntu
19.04 and newer. You can get it from the Ubuntu Cloud Archive, Stein repository
for Ubuntu 18.04:

  https://wiki.ubuntu.com/OpenStack/CloudArchive

Proot >= 5.1.0-1.3 is needed for the renameat2() syscall. It is available in
Ubuntu 19.04 and newer. It is available in this PPA for Ubuntu 18.04:

  https://launchpad.net/~a-j-buxton/+archive/ubuntu/backports/

## Keys

Multistrap/apt needs public keys to verify the repositories. You must import
the required keys into your local gpg keyring with the following commands:

    gpg --keyserver hkps://keyserver.ubuntu.com --recv-key 9165938D90FDDD2E # raspbian-archive-keyring
    gpg --keyserver hkps://keyserver.ubuntu.com --recv-key 82B129927FA3303E # raspberrypi-archive-keyring

You should take necessary steps to ensure that you have authentic versions of
these keys. Once received, rpi-ramdisk will export them as and when required.

On Ubuntu 16.04 you will also need to import these keys into the host apt
trusted keys with the following commands:

    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 9165938D90FDDD2E
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 82B129927FA3303E

You may also need to do this on Ubuntu 16.10, 17.04, 17.10 but it is not necessary
on 18.04 and later.

## Submodules

This repository uses git submodules. Clone with `--recursive` or after cloning
the repository run:

    git submodule update --init --recursive

Note that shallow cloning usually won't be possible because most of the upstream
repositories do not allow shallow cloning arbitrary commits, only the tips of
branches and tags.

## Compiling

To build rpi-ramdisk the [pydo build tool](https://github.com/ali1234/pydo) is used.
First initialize the project:

    cd rpi-ramdisk
    pydo --init

Set up the project configuration by copying one of the defaults:

    cp configs/qmldemo.config.py config.py

To build the whole project run:

    pydo :build

To clean the whole project run:

    pydo :clean

Pydo commands can be run at any level of the rpi-ramdisk tree after it has been
initialized by prefixing them with ":". Without the prefix, pydo will execute the
corresponding command for the current directory along with required dependencies.
You can also explicitly run a command from a different subdirectory eg:

    pydo packages.gstreamer:build

You can see a list of all available commands for the current project with:

    pydo -l

## Booting

The build produces a boot/ directory containing everything needed to boot.

### Booting from SD Card

The SD card first primary partition should be fat formatted. (This is the
default for new, blank SD cards.) Copy the contents of the boot directory onto
the fat partition on the SD card. Put the SD card in the Raspberry Pi and turn
it on.

### Booting from USB Mass Storage

USB mass storage booting must be enabled first:

https://www.raspberrypi.org/documentation/hardware/raspberrypi/bootmodes/msd.md

Then the procedure is the same as SD card booting: copy the contents of the
boot directory to the mass storage device, plug it in, and turn on.

### TFTP Boot

Copy `bootcode.bin` to the fat partition on your SD card. Scons generates a
`dnsmasq.conf` with the correct paths, so now just run dnsmasq:

    sudo dnsmasq -C dnsmasq.conf

Now put the SD card in the Pi and boot. Wired ethernet must be connected.
You can leave dnsmasq running across rebuilds as the boot directory is
not deleted and recreated.

**Note**: TFTP booting is sometimes unreliable due to:

https://github.com/raspberrypi/firmware/issues/764

As a workaround, enabling UART debugging seems to help reliability. rpi-ramdisk now does
this by default.

### USB device boot

Build rpiboot from:

https://github.com/raspberrypi/usbboot

Connect a Pi Zero or similar using a USB cable. Then run:

    sudo rpiboot -d boot

**Note**: initrd images larger than about 28MB may be too big to boot using this method, see:

https://github.com/raspberrypi/usbboot/issues/14

## Firmware update mode

rpi-ramdisk now installs the mass storage mode firmware for videocore. This makes USB device
capable Raspberry Pis export their SD card as a mass storage device which can be mounted on
the host PC for copying updated boot files. This is implemented using `bootcode.bin` GPIO 
filters. See https://github.com/raspberrypi/firmware/issues/1076

To enter this mode pull GPIO 5 low when powering on the device. The GPIO can be modified in
`firmware/config.txt`.
