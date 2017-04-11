FROM ubuntu:xenial

RUN dpkg --add-architecture i386

RUN apt-get update -qy && apt-get -qy install \
 libc6:i386 libstdc++6:i386 libgcc1:i386 \
 libncurses5:i386 libtinfo5:i386 zlib1g:i386 \
 build-essential git bc python \
 multistrap fakeroot fakechroot \
 qemu-user-static binfmt-support

WORKDIR /rpi-ramdisk

COPY . .

RUN ln -sf /rpi-ramdisk/raspbian/root/lib/ld-linux-armhf.so.3 /lib

CMD ["./build"]
