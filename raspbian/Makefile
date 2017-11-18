all: initrd

initrd: multistrap.conf excludes.conf build ../kernel/kernel-root.tar.gz ../kernel/kernel7-root.tar.gz ../packages/qt/qt.tar.gz ../packages/gstreamer/gstreamer.tar.gz ../packages/rygel/rygel.tar.gz
	./build

clean:
	rm -rf root/ initrd

.PHONY: clean
