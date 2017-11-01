FROM ubuntu:artful

RUN dpkg --add-architecture i386

RUN apt-get update -qy && apt-get -qy install \
 libc6:i386 libstdc++6:i386 libgcc1:i386 \
 libncurses5:i386 libtinfo5:i386 zlib1g:i386 \
 build-essential git bc python zip wget gettext \
 autoconf automake libtool pkg-config autopoint \
 bison flex libglib2.0-dev gobject-introspection \
 multistrap fakeroot fakechroot proot cpio \
 qemu-user-static binfmt-support makedev

WORKDIR /rpi-ramdisk

COPY . .
