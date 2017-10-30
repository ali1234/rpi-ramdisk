# Workarounds for libtool and gobject badness.

# pkg-config cannot handle sysroots properly, so we need to use a
# wrapper to adjust any paths it outputs.
# Also need to export PKG_CONFIG_LIBDIR in each package Makefile.
export PKG_CONFIG := $(BASEDIR)/../pkg-config
export PKG_CONFIG_DIR :=
export PKG_CONFIG_SYSROOT_DIR := $(SYSROOT)

# Set up Qemu for gobject introspection
# G-I binding generation is done by building a native executable and
# then running it to see what it exports. We need Qemu for this.
# Also need to export XDG_DATA_DIRS in each package Makefile.
export QEMU_LD_PREFIX := $(SYSROOT)
export LD_LIBRARY_PATH := $(SYSROOT)/opt/vc/lib

# tell g-ir-scanner about the sysroot.
export CFLAGS := --sysroot=$(SYSROOT) $(ARCH_CFLAGS)
export CPPFLAGS := --sysroot=$(SYSROOT)
export LDFLAGS := --sysroot=$(SYSROOT) -Wl,--unresolved-symbols=ignore-in-shared-libs
