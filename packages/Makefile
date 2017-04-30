SUBDIRS := qt gstreamer

all: toolchain sysroot $(SUBDIRS)

toolchain:
	wget -N https://releases.linaro.org/archive/15.02/components/toolchain/binaries/arm-linux-gnueabihf/gcc-linaro-4.9-2015.02-3-x86_64_arm-linux-gnueabihf.tar.xz
	tar -xf gcc-linaro-4.9-2015.02-3-x86_64_arm-linux-gnueabihf.tar.xz
	mv gcc-linaro-4.9-2015.02-3-x86_64_arm-linux-gnueabihf/ toolchain/

sysroot: multistrap.conf
	rm -rf --one-file-system sysroot/
	http_proxy=$APT_HTTP_PROXY multistrap -d sysroot/ -f multistrap.conf
	./relativelinks.py sysroot/
	# work around for libtool badness
	cd sysroot/opt/ && ln -s ../../gstreamer/opt/gst gst

$(SUBDIRS):
	$(MAKE) -C $@

clean:
	for dir in $(SUBDIRS); do $(MAKE) -C $$dir clean; done
	rm -rf sysroot/ toolchain/

.PHONY: $(SUBDIRS) clean

