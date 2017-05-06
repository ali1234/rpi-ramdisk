all: initrd

UTILS=awk cpio free grep gunzip unlzop ls mkdir mount rm sh umount

.PHONY: multistrap

initrd: initrd.dir
	fakeroot sh -c "cd initrd.dir && find * | cpio --create -H newc" | xz --check=crc32 -9 > initrd

initrd.dir: root multistrap.conf init
	mkdir -p initrd.dir/bin
	mkdir -p initrd.dir/lib
	cp root/bin/busybox initrd.dir/bin/
	for UTIL in $(UTILS); do \
		ln initrd.dir/bin/busybox initrd.dir/bin/$$UTIL ; \
	done
	cp root/usr/lib/klibc/bin/run-init initrd.dir/bin/
	cp root/lib/klibc-* initrd.dir/lib/
	cp init initrd.dir/init
	chmod a+x initrd.dir/init

root: multistrap

multistrap:
	http_proxy=$(APT_HTTP_PROXY) /usr/sbin/multistrap -d root -f multistrap.conf

clean:
	rm -rf initrd initrd.dir/ root/
