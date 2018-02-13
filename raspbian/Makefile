include ../.config

all: initrd

multistrap.conf: multistrap.part $(foreach DIR,$(PACKAGES),../packages/$(DIR)/multistrap.part)
	cat multistrap.part > multistrap.conf
	for dir in $(PACKAGES); do cat ../packages/$$dir/multistrap.part >> multistrap.conf; done

initrd: ../.config multistrap.conf excludes.conf build ../kernel/kernel-root.tar.gz ../kernel/kernel7-root.tar.gz $(foreach DIR,$(PACKAGES),../packages/$(DIR)/$(DIR).tar.gz)
	PACKAGES="$(PACKAGES)" ./build

clean:
	rm -rf root/ initrd multistrap.conf

.PHONY: clean
