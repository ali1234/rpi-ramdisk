all: boot-raspbian.zip boot-busybox-klibc.zip

SUBDIRS=kernel firmware raspbian busybox-klibc

$(SUBDIRS):
	$(MAKE) -C $@

raspbian: kernel

boot-%.zip: kernel firmware %
	mkdir -p boot-$*/
	cp $*/initrd boot-$*/
	tar -xf firmware/firmware.tar.gz -C boot-$*/
	tar -xf kernel/kernel-boot.tar.gz -C boot-$*/
	tar -xf kernel/kernel7-boot.tar.gz -C boot-$*/
	cd boot-$*/ && zip -r ../$@ *

clean:
	$(MAKE) -C kernel clean
	$(MAKE) -C firmware clean
	$(MAKE) -C raspbian clean
	$(MAKE) -C busybox-klibc clean
	rm -rf boot-*

.PHONY: $(SUBDIRS) clean

.NOTPARALLEL:
