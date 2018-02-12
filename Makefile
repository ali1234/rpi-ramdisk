all: boot-raspbian.zip boot-busybox-klibc.zip

SUBDIRS=kernel firmware packages raspbian busybox-klibc

$(SUBDIRS):
	$(MAKE) -C $@

raspbian: kernel packages

boot-%.zip: kernel firmware %
	mkdir -p boot-$*/
	cp $*/initrd boot-$*/
	tar -xf firmware/firmware.tar.gz -C boot-$*/
	tar -xf kernel/kernel-boot.tar.gz -C boot-$*/
	tar -xf kernel/kernel7-boot.tar.gz -C boot-$*/
	cd boot-$*/ && zip -qr ../$@ *

%.config: configs/%.config
	cp configs/$@ .config

clean:
	for dir in $(SUBDIRS); do $(MAKE) -C $$dir clean; done
	rm -rf boot-*

.PHONY: $(SUBDIRS) clean %.config

.NOTPARALLEL:
