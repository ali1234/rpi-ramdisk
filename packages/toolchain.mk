export BASEDIR := $(shell readlink -f .)
export PATH := $(shell readlink -f ..)/toolchain/bin:$(PATH)
export SYSROOT := $(shell readlink -f ..)/sysroot
STAGE := $(BASEDIR)/root
TOOLCHAIN := $(shell readlink -f ..)/toolchain/bin/arm-linux-gnueabihf-

ARCH_CFLAGS := -pipe -march=armv7-a -marm -mthumb-interwork -mfpu=neon-vfpv4 -mtune=cortex-a7 -mabi=aapcs-linux -mfloat-abi=hard

# pkg-config wrapper setup
# Also need to export PKG_CONFIG_LIBDIR in each package Makefile.
export PKG_CONFIG := $(BASEDIR)/../pkg-config
export PKG_CONFIG_DIR :=
export PKG_CONFIG_SYSROOT_DIR := $(SYSROOT)

# Set up Qemu for G-I
# Also need to export XDG_DATA_DIRS in each package Makefile.
export QEMU_LD_PREFIX := $(SYSROOT)
export LD_LIBRARY_PATH := $(SYSROOT)/opt/vc/lib
