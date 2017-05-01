GSTBRANCH := 1.10

export BASEDIR := $(shell readlink -f .)
export PATH := $(shell readlink -f ..)/toolchain/bin:$(PATH)
export SYSROOT := $(shell readlink -f ..)/sysroot
export PREFIX := /opt/gst

GSTREPOS := gstreamer gst-plugins-base gst-plugins-good gst-plugins-bad gst-plugins-ugly
REPOS := orc $(GSTREPOS)

ifeq ("$(VERBOSE_GST_BUILD)","1")
REDIRECT :=
else
REDIRECT := > /dev/null
endif


export PKG_CONFIG := $(BASEDIR)/pkg-config
export PKG_CONFIG_DIR :=
export PKG_CONFIG_LIBDIR := $(SYSROOT)/usr/lib/pkgconfig:$(SYSROOT)/usr/lib/arm-linux-gnueabihf/pkgconfig:$(SYSROOT)/usr/share/pkgconfig:$(SYSROOT)$(PREFIX)/lib/pkgconfig
export PKG_CONFIG_SYSROOT_DIR := $(SYSROOT)

export XDG_DATA_DIRS := $(SYSROOT)/usr/share:$(SYSROOT)$(PREFIX)/share

ARCH_CFLAGS := -pipe -march=armv7-a -marm -mthumb-interwork -mfpu=neon-vfpv4 -mtune=cortex-a7 -mabi=aapcs-linux -mfloat-abi=hard

# put dispmanx/EGL flags into the global state. https://bugzilla.gnome.org/show_bug.cgi?id=770987
export CPPFLAGS := -I$(SYSROOT)/opt/vc/include -I$(SYSROOT)/opt/vc/include/interface/vcos/pthreads -I$(SYSROOT)/opt/vc/include/interface/vmcs_host/linux
export LIBS := -L$(SYSROOT)/opt/vc/lib

export CFLAGS := --sysroot=$(SYSROOT) $(ARCH_CFLAGS)
export LDFLAGS := --sysroot=$(SYSROOT) -Wl,--unresolved-symbols=ignore-in-shared-libs

# Set up Qemu for G-I
export QEMU_LD_PREFIX := $(SYSROOT)
export LD_LIBRARY_PATH := $(SYSROOT)/opt/vc/lib


## Configuration options:

# cross compiler options
CROSS_OPTS := --host=arm-linux-gnueabihf --build=x86_64-linux-gnu --prefix=$(PREFIX) --with-sysroot=$(BASEDIR)

# common options for every build
COMMON_OPTS := --disable-dependency-tracking --disable-maintainer-mode --disable-fatal-warnings --disable-debug --disable-docbook --disable-gtk-doc --disable-gtk-doc-html --disable-gtk-doc-pdf --disable-examples --disable-benchmarks

# options for gobject-introspection
GI_OPTS := --enable-introspection=yes

# options that turn off all debugging
NODEBUG_OPTS := --enable-gobject-cast-checks=no --enable-glib-asserts=no --disable-gst-debug --disable-gst-tracer-hooks --disable-trace --disable-alloc-trace --disable-valgrind

# options common to base/good/bad/ugly
PLUGIN_OPTS := --enable-orc --disable-x --disable-xvideo --disable-xshm --disable-wayland --disable-fbdev --disable-jack --disable-pulse --disable-cairo --disable-gdk_pixbuf --disable-festival --disable-flite --disable-fluidsynth

# options for dispmanx in bad
DISPMANX_OPTS := --disable-opengl --enable-gles2 --enable-egl --disable-glx --enable-dispmanx --with-gles2-module-name=/opt/vc/lib/libGLESv2.so --with-egl-module-name=/opt/vc/lib/libEGL.so

# options for OMX
OMX_OPTS := --with-omx-target=rpi --with-omx-header-path=${SYSROOT}/opt/vc/include/IL

# options for "make install"
INSTALL_OPTS := DESTDIR=$(BASEDIR)


all: gst.tar.gz

$(GSTREPOS):
	git clone --depth 1 -b $(GSTBRANCH) git://anongit.freedesktop.org/git/gstreamer/$@

orc:
	git clone --depth 1 git://anongit.freedesktop.org/git/gstreamer/orc

gst.tar.gz: orc.timestamp $(shell for repo in $(GSTREPOS); do echo $$repo.timestamp; done )
	for repo in $(REPOS); do git -C $$repo clean -dfxq; done

	rm -rf --one-file-system opt/

	cd orc && ./autogen.sh $(CROSS_OPTS) $(COMMON_OPTS)
	$(MAKE) -C orc
	$(MAKE) -C orc $(INSTALL_OPTS) install

	cd gstreamer && ./autogen.sh $(CROSS_OPTS) $(COMMON_OPTS) $(NODEBUG_OPTS) $(GI_OPTS)
	$(MAKE) -C gstreamer
	$(MAKE) -C gstreamer $(INSTALL_OPTS) install

	cd gst-plugins-base && ./autogen.sh $(CROSS_OPTS) $(COMMON_OPTS) $(NODEBUG_OPTS) $(GI_OPTS) $(PLUGIN_OPTS)
	$(MAKE) -C gst-plugins-base
	$(MAKE) -C gst-plugins-base $(INSTALL_OPTS) install

	cd gst-plugins-good && ./autogen.sh $(CROSS_OPTS) $(COMMON_OPTS) $(NODEBUG_OPTS) $(GI_OPTS) $(PLUGIN_OPTS)
	$(MAKE) -C gst-plugins-good
	$(MAKE) -C gst-plugins-good $(INSTALL_OPTS) install

	cd gst-plugins-bad && ./autogen.sh $(CROSS_OPTS) $(COMMON_OPTS) $(NODEBUG_OPTS) $(GI_OPTS) $(PLUGIN_OPTS) $(DISPMANX_OPTS)
	$(MAKE) -C gst-plugins-bad
	$(MAKE) -C gst-plugins-bad $(INSTALL_OPTS) install

	cd gst-plugins-ugly && ./autogen.sh $(CROSS_OPTS) $(COMMON_OPTS) $(NODEBUG_OPTS) $(GI_OPTS) $(PLUGIN_OPTS)
	$(MAKE) -C gst-plugins-ugly
	$(MAKE) -C gst-plugins-ugly $(INSTALL_OPTS) install

#	cd opt/ && find -name '*.so' -exec chrpath -d {} \;

	cd opt/ && tar --exclude=gst/doc --exclude=gst/include --exclude=*.la --exclude=gst/lib/pkgconfig \
		--exclude=gst/share/man --exclude=gst/share/locale --exclude=gst/share/aclocal \
		--exclude=gst/share/bash-completion -czf ../gst.tar.gz gst/

.PRECIOUS: %.timestamp
%.timestamp: % FORCE
	@echo Checking timestamps in $*...
	@if [ ! -f $*.timestamp ]; then echo $*/.git/logs/HEAD changed; touch -r $*/.git/logs/HEAD $*.timestamp; fi
	@if [ $*/.git/logs/HEAD -nt $*.timestamp ]; then echo $*/.git/logs/HEAD changed; touch -r $*/.git/logs/HEAD $*.timestamp; fi
	@for file in $$(git -C $* ls-files -mo --exclude-standard); do if [ $*/$$file -nt $*.timestamp ]; then echo $*/$$file changed; touch -r $*/$$file $*.timestamp; fi; done

FORCE: ;

pull: $(REPOS)
	for repo in $(REPOS); do git -C $$repo pull; done

clean:
	for repo in $(REPOS); do git -C $$repo clean -dfxq; done
	rm -rf --one-file-system opt/ *.timestamp gst.tar.gz

.PHONY: clean
