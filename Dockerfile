FROM ubuntu:eoan

RUN dpkg --add-architecture i386 && apt-get update -qy && apt-get -qy install \
 libc6:i386 libstdc++6:i386 libgcc1:i386 \
 libncurses5:i386 libtinfo5:i386 zlib1g:i386 \
 build-essential git bc python zip wget gettext \
 autoconf automake libtool pkg-config autopoint \
 bison flex libglib2.0-dev gobject-introspection \
 multistrap proot qemu-user binfmt-support makedev cpio \
 gtk-doc-tools valac python3.7-minimal python3-pip \
 libssl-dev gpg nano cmake dnsmasq ninja-build \
 strace

# make dnsmasq setuid so we can run it in the container without being root
RUN chmod u+s /usr/sbin/dnsmasq

# https://gitlab.gnome.org/GNOME/gobject-introspection/issues/314
RUN sed -i \
 -e 's/filter(lambda x: x.endswith(".la"), libraries)/list(filter(lambda x: x.endswith(".la"), libraries))/' \
 -e 's/filter(lambda x: not x.endswith(".la"), libraries)/list(filter(lambda x: not x.endswith(".la"), libraries))/' \
 /usr/lib/x86_64-linux-gnu/gobject-introspection/giscanner/shlibs.py

RUN git clone git://github.com/ali1234/pydo && cd pydo && pip3 install .[color]

# we need 0.52 for sysroot support - not released yet so install from git
RUN git clone git://github.com/mesonbuild/meson && cd meson && pip3 install .

ARG UID=1000
ARG GID=1000
ARG USER=rpi-ramdisk
ARG GROUP=rpi-ramdisk

RUN groupadd -g $GID $GROUP
RUN useradd -ms /bin/bash -u $UID -g $GID $USER

USER $USER

RUN gpg --keyserver hkps://keyserver.ubuntu.com --recv-key 9165938D90FDDD2E # raspbian-archive-keyring
RUN gpg --keyserver hkps://keyserver.ubuntu.com --recv-key 82B129927FA3303E # foundation key

