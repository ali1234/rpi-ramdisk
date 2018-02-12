include ../toolchain.mk
include ../workarounds.mk

PREFIX := /opt/rygel

REPOS := gssdp gupnp gupnp-av gupnp-dlna gupnp-tools rygel

ifeq ("$(VERBOSE_RYGEL_BUILD)","1")
REDIRECT :=
else
REDIRECT := > /dev/null
endif


export XDG_DATA_DIRS := $(SYSROOT)/usr/share:$(SYSROOT)$(PREFIX)/share:$(SYSROOT)/opt/gstreamer/share
export PKG_CONFIG_LIBDIR := $(SYSROOT)/usr/lib/pkgconfig:$(SYSROOT)/usr/lib/arm-linux-gnueabihf/pkgconfig:$(SYSROOT)/usr/share/pkgconfig:$(SYSROOT)$(PREFIX)/lib/pkgconfig:$(SYSROOT)/opt/gstreamer/lib/pkgconfig

## Configuration options:

# cross compiler options
CROSS_OPTS := --host=arm-linux-gnueabihf --build=x86_64-linux-gnu --prefix=$(PREFIX) --with-sysroot=$(SYSROOT)

# common options for every build
COMMON_OPTS := --disable-dependency-tracking --disable-maintainer-mode --disable-fatal-warnings --disable-debug --disable-docbook --disable-gtk-doc --disable-gtk-doc-html --disable-gtk-doc-pdf --disable-examples --disable-benchmarks

# options for gobject-introspection
GI_OPTS := --enable-introspection=yes

# options that turn off all debugging
NODEBUG_OPTS := --enable-gobject-cast-checks=no --enable-glib-asserts=no --disable-gst-debug --disable-gst-tracer-hooks --disable-trace --disable-alloc-trace --disable-valgrind

# options for "make install"
INSTALL_OPTS := DESTDIR=$(STAGE)


all: rygel.tar.gz

rygel.tar.gz: $(shell for repo in $(REPOS); do echo $$repo.timestamp; done )
	for repo in $(REPOS); do git -C $$repo clean -dfxq; done

	rm -rf --one-file-system $(STAGE)

	cd gssdp && ./autogen.sh ${CROSS_OPTS} ${COMMON_OPTS} ${NODEBUG_OPTS} ${GI_OPTS}
	$(MAKE) -C gssdp $(REDIRECT)
	$(MAKE) -C gssdp $(INSTALL_OPTS) install $(REDIRECT)

	cd gupnp && ./autogen.sh ${CROSS_OPTS} ${COMMON_OPTS} ${NODEBUG_OPTS} ${GI_OPTS}
	$(MAKE) -C gupnp $(REDIRECT)
	$(MAKE) -C gupnp $(INSTALL_OPTS) install $(REDIRECT)

	cd gupnp-av && ./autogen.sh ${CROSS_OPTS} ${COMMON_OPTS} ${NODEBUG_OPTS} ${GI_OPTS}
	$(MAKE) -C gupnp-av $(REDIRECT)
	$(MAKE) -C gupnp-av $(INSTALL_OPTS) install $(REDIRECT)

	cd gupnp-dlna && ./autogen.sh ${CROSS_OPTS} ${COMMON_OPTS} ${NODEBUG_OPTS} ${GI_OPTS}
	$(MAKE) -C gupnp-dlna $(REDIRECT)
	$(MAKE) -j1 -C gupnp-dlna $(INSTALL_OPTS) install $(REDIRECT)

	cd rygel && ./autogen.sh ${CROSS_OPTS} ${COMMON_OPTS} ${NODEBUG_OPTS} --without-ui --disable-media-export-plugin --disable-tracker-plugin --disable-external-plugin --disable-ruih-plugin --disable-mpris-plugin --enable-apidocs=no
	$(MAKE) -C rygel $(REDIRECT)
	$(MAKE) -C rygel $(INSTALL_OPTS) install $(REDIRECT)

#	cd opt/ && find -name '*.so' -exec chrpath -d {} \;

	mkdir -p $(STAGE)/etc/ld.so.conf.d
	echo $(PREFIX)/lib > $(STAGE)/etc/ld.so.conf.d/opt-rygel.conf

	tar -C $(STAGE) --exclude=.$(PREFIX)/doc --exclude=.$(PREFIX)/include --exclude=*.la --exclude=.$(PREFIX)/lib/pkgconfig \
		--exclude=.$(PREFIX)/share/man --exclude=.$(PREFIX)/share/locale --exclude=.$(PREFIX)/share/aclocal \
		--exclude=.$(PREFIX)/share/bash-completion -czf rygel.tar.gz .

include ../../include/timestamp.mk

install: rygel.tar.gz
	tar -xf rygel.tar.gz -C $(DESTDIR)

clean:
	for repo in $(REPOS); do git -C $$repo clean -dfxq; done
	rm -rf --one-file-system $(STAGE) *.timestamp rygel.tar.gz

.PHONY: clean install
