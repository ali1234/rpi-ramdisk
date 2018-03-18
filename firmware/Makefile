all: firmware.tar.gz

firmware.tar.gz: root/boot multistrap.conf config.txt cmdline.txt
	cp config.txt root/boot/
	cp cmdline.txt root/boot/
	tar -C root/boot/ -czvf firmware.tar.gz .

root/boot:
	rm -rf --one-file-system root/
	mkdir -p root/etc/apt/trusted.gpg.d/
	gpg --export 82B129927FA3303E > root/etc/apt/trusted.gpg.d/raspberrypi-archive-keyring.gpg
	http_proxy=$(APT_HTTP_PROXY) /usr/sbin/multistrap -d root -f multistrap.conf

clean:
	rm -rf --one-file-system firmware.tar.gz root/

.PHONY: multistrap clean
