BASEDIR := $(shell readlink -f .)
TOOLCHAIN := $(shell readlink -f ..)/toolchain/bin/arm-linux-gnueabihf-
SYSROOT := $(shell readlink -f ..)/sysroot/
PREFIX := /opt/qt
STAGE := $(BASEDIR)/root
HOSTPREFIX := $(BASEDIR)/qt-host

QTBRANCH := 5.9
REPOS := qtbase qtxmlpatterns qtdeclarative

ifeq ("$(VERBOSE_QT_BUILD)","1")
REDIRECT :=
else
REDIRECT := > /dev/null
endif

all: qt.tar.gz

$(REPOS):
	git clone --depth 1 -b $(QTBRANCH) git://code.qt.io/qt/$@.git

qt.tar.gz: $(shell for repo in $(REPOS); do echo $$repo.timestamp; done )
	rm -rf --one-file-system $(STAGE) $(HOSTPREFIX)
	for repo in $(REPOS); do git -C $$repo clean -dfxq; done

	cp qmake.conf qtbase/mkspecs/devices/linux-rasp-pi2-g++/qmake.conf
	cd qtbase && ./configure -release -opengl es2 -device linux-rasp-pi2-g++ \
		-qpa eglfs -no-libinput -no-linuxfb -no-xcb -no-kms -no-gbm -no-gtk -no-widgets -no-compile-examples \
		-device-option CROSS_COMPILE=$(TOOLCHAIN) -sysroot $(SYSROOT) \
		-opensource -confirm-license -make libs \
		-prefix $(PREFIX) -extprefix $(STAGE)/$(PREFIX) -hostprefix $(HOSTPREFIX) $(REDIRECT)

	$(MAKE) -C qtbase $(REDIRECT)
	$(MAKE) -C qtbase install $(REDIRECT)
	cd qtxmlpatterns && ../qt-host/bin/qmake $(REDIRECT)
	$(MAKE) -C qtxmlpatterns $(REDIRECT)
	$(MAKE) -C qtxmlpatterns install $(REDIRECT)
	cd qtdeclarative && ../qt-host/bin/qmake $(REDIRECT)
	$(MAKE) -C qtdeclarative $(REDIRECT)
	$(MAKE) -C qtdeclarative install $(REDIRECT)

	mkdir -p $(STAGE)/etc/ld.so.conf.d
	echo $(PREFIX)/lib > $(STAGE)/etc/ld.so.conf.d/opt-qt.conf

	tar -C $(STAGE) --exclude=.$(PREFIX)/doc --exclude=.$(PREFIX)/include -czf qt.tar.gz .

.PRECIOUS: %.timestamp
%.timestamp: % FORCE
	@echo Checking timestamps in $*...
	@if [ ! -f $*.timestamp ]; then echo $* timestamp not found; touch -r $$(git -C $* rev-parse --git-dir)/logs/HEAD $*.timestamp; fi
	@if [ $$(git -C $* rev-parse --git-dir)/logs/HEAD -nt $*.timestamp ]; then echo $* HEAD changed; touch -r $$(git -C $* rev-parse --git-dir)/logs/HEAD $*.timestamp; fi
	@for file in $$(git -C $* ls-files -mo --exclude-standard); do if [ $*/$$file -nt $*.timestamp ]; then echo $*/$$file changed; touch -r $*/$$file $*.timestamp; fi; done

FORCE: ;

pull: $(REPOS)
	for repo in $(REPOS); do git -C $$repo pull; done

clean:
	for repo in $(REPOS); do git -C $$repo clean -dfxq; done
	rm -rf --one-file-system $(STAGE) $(HOSTPREFIX) *.timestamp qt.tar.gz

.PHONY: clean
