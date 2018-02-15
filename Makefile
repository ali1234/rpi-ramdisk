all: boot.zip dnsmasq.conf

SUBDIRS=kernel firmware packages raspbian

$(SUBDIRS):
	$(MAKE) -C $@

raspbian: kernel packages

boot.zip: kernel firmware raspbian
	mkdir -p boot/
	cp raspbian/initrd boot/
	tar -xf firmware/firmware.tar.gz -C boot/
	tar -xf kernel/kernel-boot.tar.gz -C boot/
	tar -xf kernel/kernel7-boot.tar.gz -C boot/
	cd boot/ && zip -qr ../$@ *

%.config: configs/%.config
	cp configs/$@ .config

dnsmasq.conf: dnsmasq.conf.in
	sed -e 's|##bootdir##|$(shell readlink -f boot)|' dnsmasq.conf.in > dnsmasq.conf

clean:
	for dir in $(SUBDIRS); do $(MAKE) -C $$dir clean; done
	rm -rf boot

.PHONY: $(SUBDIRS) clean %.config dnsmasq.conf

.NOTPARALLEL:
