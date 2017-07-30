SUBDIRS := qt gstreamer

all: toolchain sysroot $(SUBDIRS)

toolchain:
	wget -N https://releases.linaro.org/components/toolchain/binaries/6.3-2017.05/arm-linux-gnueabihf/gcc-linaro-6.3.1-2017.05-x86_64_arm-linux-gnueabihf.tar.xz
	tar -xf gcc-linaro-6.3.1-2017.05-x86_64_arm-linux-gnueabihf.tar.xz
	mv gcc-linaro-6.3.1-2017.05-x86_64_arm-linux-gnueabihf/ toolchain/

sysroot: multistrap.conf
	rm -rf --one-file-system sysroot/
	http_proxy=$APT_HTTP_PROXY /usr/sbin/multistrap -d sysroot/ -f multistrap.conf
	./relativelinks.py sysroot/
	# work around for libtool badness
	cd sysroot/opt/ && ln -s ../../gstreamer/root/opt/gst gst
	touch sysroot

$(SUBDIRS): toolchain sysroot
	$(MAKE) -C $@

clean:
	for dir in $(SUBDIRS); do $(MAKE) -C $$dir clean; done
	rm -rf sysroot/ toolchain/

.PHONY: $(SUBDIRS) clean

