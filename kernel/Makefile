COMPILER=../tools/arm-bcm2708/gcc-linaro-arm-linux-gnueabihf-raspbian/bin/arm-linux-gnueabihf-

all: kernel kernel7

kernel: kernel-boot.tar.gz kernel-root.tar.gz

kernel7: kernel7-boot.tar.gz kernel7-root.tar.gz

linux:
	git clone --depth 1 -b rpi-4.9.y https://github.com/raspberrypi/linux.git

tools:
	git clone --depth 1 https://github.com/raspberrypi/tools.git

.NOTPARALLEL:
%-boot.tar.gz %-root.tar.gz: %.config linux.timestamp tools.timestamp
	git -C linux clean -d -f -x
	rm -rf root/
	rm -rf boot/
	mkdir -p boot/overlays/
	cp $*.config linux/.config
	$(MAKE) -C linux ARCH=arm CROSS_COMPILE=$(COMPILER) zImage modules dtbs
	$(MAKE) -C linux ARCH=arm CROSS_COMPILE=$(COMPILER) INSTALL_MOD_PATH=../root modules_install
	linux/scripts/mkknlimg linux/arch/arm/boot/zImage boot/$*.img
	cp linux/arch/arm/boot/dts/*.dtb boot/
	cp linux/arch/arm/boot/dts/overlays/*.dtb* boot/overlays/
	cp linux/arch/arm/boot/dts/overlays/README boot/overlays/
	tar -C root/ -czvf $*-root.tar.gz .
	tar -C boot/ -czvf $*-boot.tar.gz .

.PRECIOUS: %.timestamp
%.timestamp: % FORCE
	@if [ ! -f $*.timestamp ]; then echo $*/.git/logs/HEAD changed; touch -r $*/.git/logs/HEAD $*.timestamp; fi
	@if [ $*/.git/logs/HEAD -nt $*.timestamp ]; then echo $*/.git/logs/HEAD changed; touch -r $*/.git/logs/HEAD $*.timestamp; fi
	@for file in $$(git -C $* ls-files -mo --exclude-standard); do if [ $*/$$file -nt $*.timestamp ]; then echo $*/$$file changed; touch -r $*/$$file $*.timestamp; fi; done

FORCE: ;

pull: linux tools
	git -C linux pull
	git -C tools pull

clean:
	git -C linux clean -d -f -x
	rm -rf root/ boot/ kernel-boot.tar.gz kernel-root.tar.gz kernel7-boot.tar.gz kernel7-root.tar.gz *.timestamp

.PHONY: kernel kernel7 clean pull

