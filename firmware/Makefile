all: firmware.tar.gz

firmware.tar.gz: root multistrap.conf config.txt cmdline.txt
	cp config.txt root/boot/
	cp cmdline.txt root/boot/
	tar -C root/boot/ -czvf firmware.tar.gz .

root: multistrap

multistrap:
	http_proxy=$(APT_HTTP_PROXY) multistrap -d root -f multistrap.conf

clean:
	rm -rf firmware.tar.gz root/

.PHONY: multistrap clean
