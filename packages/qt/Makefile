include ../toolchain.mk

PREFIX := /opt/qt
HOSTPREFIX := $(BASEDIR)/qt-host

REPOS := qtbase qtxmlpatterns qtdeclarative

ifeq ("$(VERBOSE_QT_BUILD)","1")
REDIRECT :=
else
REDIRECT := > /dev/null
endif

all: qt.tar.gz

qt.tar.gz: $(shell for repo in $(REPOS); do echo $$repo.timestamp; done )
	rm -rf --one-file-system $(STAGE) $(HOSTPREFIX)
	for repo in $(REPOS); do git -C $$repo clean -dfxq; done

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

include ../../include/timestamp.mk

pull:
	git submodule update --remote .

clean:
	for repo in $(REPOS); do git -C $$repo clean -dfxq; done
	rm -rf --one-file-system $(STAGE) $(HOSTPREFIX) *.timestamp qt.tar.gz

.PHONY: clean
