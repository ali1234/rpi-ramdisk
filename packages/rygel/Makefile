RYGELBRANCH=master

export BASEDIR := $(shell readlink -f .)
export PATH := $(shell readlink -f ..)/toolchain/bin:$(PATH)
export SYSROOT := $(shell readlink -f ..)/sysroot
PREFIX := /opt/rygel
STAGE := $(BASEDIR)/root

REPOS := rygel

ifeq ("$(VERBOSE_RYGEL_BUILD)","1")
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
#export CPPFLAGS := -I$(SYSROOT)/opt/vc/include -I$(SYSROOT)/opt/vc/include/interface/vcos/pthreads -I$(SYSROOT)/opt/vc/include/interface/vmcs_host/linux
#export LIBS := -L$(SYSROOT)/opt/vc/lib

export CFLAGS := --sysroot=$(SYSROOT) $(ARCH_CFLAGS)
export LDFLAGS := --sysroot=$(SYSROOT) -Wl,--unresolved-symbols=ignore-in-shared-libs

# Set up Qemu for G-I
export QEMU_LD_PREFIX := $(SYSROOT)
export LD_LIBRARY_PATH := $(SYSROOT)/opt/vc/lib


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

$(REPOS):
	git clone --depth 1 -b $(RYGELBRANCH) git://git.gnome.org/$@

rygel.tar.gz: $(shell for repo in $(REPOS); do echo $$repo.timestamp; done )
	for repo in $(REPOS); do git -C $$repo clean -dfxq; done

	rm -rf --one-file-system $(STAGE)

	cd rygel && ./autogen.sh ${CROSS_OPTS} ${COMMON_OPTS} ${NODEBUG_OPTS} --without-ui --disable-media-export-plugin --disable-tracker-plugin --disable-external-plugin --disable-ruih-plugin --disable-mpris-plugin --enable-apidocs=no
	$(MAKE) -C rygel $(REDIRECT)
	$(MAKE) -C rygel $(INSTALL_OPTS) install $(REDIRECT)

#	cd opt/ && find -name '*.so' -exec chrpath -d {} \;

	mkdir -p $(STAGE)/etc/ld.so.conf.d
	echo $(PREFIX)/lib > $(STAGE)/etc/ld.so.conf.d/opt-rygel.conf

	tar -C $(STAGE) --exclude=.$(PREFIX)/doc --exclude=.$(PREFIX)/include --exclude=*.la --exclude=.$(PREFIX)/lib/pkgconfig \
		--exclude=.$(PREFIX)/share/man --exclude=.$(PREFIX)/share/locale --exclude=.$(PREFIX)/share/aclocal \
		--exclude=.$(PREFIX)/share/bash-completion -czf rygel.tar.gz .

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
	rm -rf --one-file-system $(STAGE) *.timestamp rygel.tar.gz

.PHONY: clean
