CROSS_COMPILE := ../tools/arm-bcm2708/gcc-linaro-arm-linux-gnueabihf-raspbian/bin/arm-linux-gnueabihf-
CROSS_OPTS := CROSS_COMPILE=$(CROSS_COMPILE)

ifeq ("$(USE_CCACHE)","1")
CROSS_OPTS += CC="ccache $(CROSS_COMPILE)gcc"
endif

ifeq ("$(VERBOSE_KERNEL_BUILD)","1")
REDIRECT :=
else
REDIRECT := > /dev/null
endif

all: kernel kernel7

kernel: kernel-boot.tar.gz kernel-root.tar.gz

kernel7: kernel7-boot.tar.gz kernel7-root.tar.gz

.NOTPARALLEL:
%-boot.tar.gz %-root.tar.gz: %.config linux.timestamp tools.timestamp
	git -C linux clean -dfxq
	rm -rf root/
	rm -rf boot/
	mkdir -p boot/overlays/
	cp $*.config linux/.config
	$(MAKE) -C linux ARCH=arm $(CROSS_OPTS) zImage modules dtbs $(REDIRECT)
	$(MAKE) -C linux ARCH=arm $(CROSS_OPTS) INSTALL_MOD_PATH=../root modules_install $(REDIRECT)
	cp linux/arch/arm/boot/zImage boot/$*.img
	cp linux/arch/arm/boot/dts/*.dtb boot/
	cp linux/arch/arm/boot/dts/overlays/*.dtb* boot/overlays/
	cp linux/arch/arm/boot/dts/overlays/README boot/overlays/
	tar -C root/ -czf $*-root.tar.gz .
	tar -C boot/ -czf $*-boot.tar.gz .

.PRECIOUS: %.timestamp
%.timestamp: % FORCE
	@echo Checking timestamps in $*...
	@if [ ! -f $*.timestamp ]; then echo $* timestamp not found; touch -r $$(git -C $* rev-parse --absolute-git-dir)/logs/HEAD $*.timestamp; fi
	@if [ $$(git -C $* rev-parse --absolute-git-dir)/logs/HEAD -nt $*.timestamp ]; then echo $* HEAD changed; touch -r $$(git -C $* rev-parse --absolute-git-dir)/logs/HEAD $*.timestamp; fi
	@for file in $$(git -C $* ls-files -mo --exclude-standard); do if [ $*/$$file -nt $*.timestamp ]; then echo $*/$$file changed; touch -r $*/$$file $*.timestamp; fi; done

FORCE: ;

updateconfig:
	$(MAKE) -C linux ARCH=arm $(CROSS_OPTS) mrproper
	cp kernel.config linux/.config
	$(MAKE) -C linux ARCH=arm $(CROSS_OPTS) oldconfig
	cp linux/.config kernel.config
	cp kernel7.config linux/.config
	$(MAKE) -C linux ARCH=arm $(CROSS_OPTS) oldconfig
	cp linux/.config kernel7.config

updatesubmodules:
	git submodule update --remote .
	$(MAKE) updateconfig

clean:
	git -C linux clean -dfxq
	rm -rf root/ boot/ kernel-boot.tar.gz kernel-root.tar.gz kernel7-boot.tar.gz kernel7-root.tar.gz *.timestamp

.PHONY: kernel kernel7 clean

