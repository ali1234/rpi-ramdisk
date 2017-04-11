RPi Ramdisk
-----------

Builds two ramdisk environments for Raspberry Pi.

- busybox/klibc is a minimal tiny environment
- raspbian is a full system

Install qemu-user-static, binfmt-support, multistrap, fakeroot, fakechroot
and then run ./build.

To boot the images you have three options:

1. From SD card:

Copy boot-raspbian/* to the root of the fat partition on your SD card and
then put it in the Pi.

2. Netboot:

Copy boot-raspbian/bootcode.bin to the root of the fat partition on your
SD card. Edit dnsmasq.conf and change the tftpboot path to point to
boot-raspbian/ and then run "sudo dnsmasq -C dnsmasq.conf". Now put the SD
card in the Pi and boot. Wired ethernet must be connected.

Note: netboot is unreliable due to this bug:

https://github.com/raspberrypi/firmware/issues/764

3. USB device mode boot:

Connect a Pi Zero or similar using a USB cable. Build rpiboot from:

https://github.com/raspberrypi/usbboot

Then run "sudo rpiboot -d boot-busybox-klibc"

Note: Raspbian image is too big to boot using this method, see:

https://github.com/raspberrypi/usbboot/issues/14
