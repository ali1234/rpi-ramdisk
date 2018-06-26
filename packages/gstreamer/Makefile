include ../toolchain.mk
include ../workarounds.mk

PREFIX := /opt/gstreamer

REPOS := gstreamer gst-plugins-base gst-plugins-good gst-plugins-bad gst-plugins-ugly gst-libav gst-omx

ifeq ("$(VERBOSE_GSTREAMER_BUILD)","1")
REDIRECT :=
else
REDIRECT := > /dev/null
endif


# search dirs for G-I
export XDG_DATA_DIRS := $(SYSROOT)/usr/share:$(SYSROOT)$(PREFIX)/share
export PKG_CONFIG_LIBDIR := $(SYSROOT)/usr/lib/pkgconfig:$(SYSROOT)/usr/lib/arm-linux-gnueabihf/pkgconfig:$(SYSROOT)/usr/share/pkgconfig:$(SYSROOT)$(PREFIX)/lib/pkgconfig

# put dispmanx/EGL flags into the global state. https://bugzilla.gnome.org/show_bug.cgi?id=770987
export CPPFLAGS := $(CPPFLAGS) -I$(SYSROOT)/opt/vc/include -I$(SYSROOT)/opt/vc/include/interface/vcos/pthreads -I$(SYSROOT)/opt/vc/include/interface/vmcs_host/linux
export LIBS := -L$(SYSROOT)/opt/vc/lib

## Configuration options:

# cross compiler options
CROSS_OPTS := --host=arm-linux-gnueabihf --build=x86_64-linux-gnu --prefix=$(PREFIX) --with-sysroot=$(SYSROOT) --with-libgcrypt-prefix=$(SYSROOT)/usr

# common options for every build
COMMON_OPTS := --disable-dependency-tracking --disable-maintainer-mode --disable-fatal-warnings --disable-debug --disable-docbook --disable-gtk-doc --disable-gtk-doc-html --disable-gtk-doc-pdf --disable-examples --disable-benchmarks

# options for gobject-introspection
GI_OPTS := --enable-introspection=yes

# options that turn off all debugging
NODEBUG_OPTS := --enable-gobject-cast-checks=no --enable-glib-asserts=no --disable-gst-debug --disable-gst-tracer-hooks --disable-trace --disable-alloc-trace --disable-valgrind

# options common to base/good/bad/ugly
PLUGIN_OPTS := --enable-orc --disable-x --disable-xvideo --disable-xshm --disable-wayland --disable-fbdev --disable-jack --disable-pulse --disable-cairo --disable-gdk_pixbuf --disable-festival --disable-flite --disable-fluidsynth

# options for dispmanx in base
DISPMANX_OPTS := --disable-opengl --enable-gles2 --enable-egl --disable-glx --enable-dispmanx --with-gles2-module-name=/opt/vc/lib/libbrcmGLESv2.so --with-egl-module-name=/opt/vc/lib/libbrcmEGL.so

# options for OMX
OMX_OPTS := --with-omx-target=rpi --with-omx-header-path=${SYSROOT}/opt/vc/include/IL

# options for "make install"
INSTALL_OPTS := DESTDIR=$(STAGE)


all: gstreamer.tar.gz

gstreamer.tar.gz: sysroot.part $(shell for repo in $(REPOS); do echo $$repo.timestamp; done )
	for repo in $(REPOS); do git -C $$repo clean -dfxq; done

	rm -rf --one-file-system $(STAGE)

	cd gstreamer && ./autogen.sh $(CROSS_OPTS) $(COMMON_OPTS) $(NODEBUG_OPTS) $(GI_OPTS) | tee ../gstreamer.config.log $(REDIRECT)
	$(MAKE) -C gstreamer $(REDIRECT)
	$(MAKE) -C gstreamer $(INSTALL_OPTS) install-strip $(REDIRECT)

	cd gst-plugins-base && ./autogen.sh $(CROSS_OPTS) $(COMMON_OPTS) $(NODEBUG_OPTS) $(GI_OPTS) $(PLUGIN_OPTS) $(DISPMANX_OPTS) | tee ../gst-plugins-base.config.log $(REDIRECT)
	$(MAKE) -C gst-plugins-base $(REDIRECT)
	$(MAKE) -C gst-plugins-base $(INSTALL_OPTS) install-strip $(REDIRECT)

	cd gst-plugins-good && ./autogen.sh $(CROSS_OPTS) $(COMMON_OPTS) $(NODEBUG_OPTS) $(GI_OPTS) $(PLUGIN_OPTS) | tee ../gst-plugins-good.config.log $(REDIRECT)
	$(MAKE) -C gst-plugins-good $(REDIRECT)
	$(MAKE) -C gst-plugins-good $(INSTALL_OPTS) install-strip $(REDIRECT)

	cd gst-plugins-bad && ./autogen.sh $(CROSS_OPTS) $(COMMON_OPTS) $(NODEBUG_OPTS) $(GI_OPTS) $(PLUGIN_OPTS) --disable-gl | tee ../gst-plugins-bad.config.log $(REDIRECT)
	$(MAKE) -C gst-plugins-bad $(REDIRECT)
	$(MAKE) -C gst-plugins-bad $(INSTALL_OPTS) install-strip $(REDIRECT)

	cd gst-plugins-ugly && ./autogen.sh $(CROSS_OPTS) $(COMMON_OPTS) $(NODEBUG_OPTS) $(GI_OPTS) $(PLUGIN_OPTS) | tee ../gst-plugins-ugly.config.log $(REDIRECT)
	$(MAKE) -C gst-plugins-ugly $(REDIRECT)
	$(MAKE) -C gst-plugins-ugly $(INSTALL_OPTS) install-strip $(REDIRECT)

#	cd gst-libav && ./autogen.sh $(CROSS_OPTS) $(COMMON_OPTS) $(NODEBUG_OPTS) $(GI_OPTS) $(PLUGIN_OPTS) | tee ../gst-libav.config.log $(REDIRECT)
#	$(MAKE) -C gst-libav $(REDIRECT)
#	$(MAKE) -C gst-libav $(INSTALL_OPTS) install-strip $(REDIRECT)

	cd gst-omx && ./autogen.sh $(CROSS_OPTS) $(COMMON_OPTS) $(OMX_OPTS) $(NODEBUG_OPTS) $(GI_OPTS) $(PLUGIN_OPTS) | tee ../gst-omx.config.log $(REDIRECT)
	$(MAKE) -C gst-omx $(REDIRECT)
	$(MAKE) -C gst-omx $(INSTALL_OPTS) install-strip $(REDIRECT)

#	cd opt/ && find -name '*.so' -exec chrpath -d {} \;

	mkdir -p $(STAGE)/etc/ld.so.conf.d
	echo $(PREFIX)/lib > $(STAGE)/etc/ld.so.conf.d/opt-gstreamer.conf

	tar -C $(STAGE) --exclude=.$(PREFIX)/doc --exclude=.$(PREFIX)/include --exclude=*.la --exclude=.$(PREFIX)/lib/pkgconfig \
		--exclude=.$(PREFIX)/share/man --exclude=.$(PREFIX)/share/locale --exclude=.$(PREFIX)/share/aclocal \
		--exclude=.$(PREFIX)/share/bash-completion -czf gstreamer.tar.gz .

include ../../include/timestamp.mk

install: gstreamer.tar.gz
	tar -xf gstreamer.tar.gz -C $(DESTDIR)

clean:
	for repo in $(REPOS); do git -C $$repo clean -dfxq; done
	rm -rf --one-file-system $(STAGE) *.timestamp gstreamer.tar.gz

.PHONY: clean install
