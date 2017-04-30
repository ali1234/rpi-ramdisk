QTBRANCH := 5.8
BASEDIR := $(shell readlink -f .)
TOOLCHAIN := $(shell readlink -f ..)/toolchain/bin/arm-linux-gnueabihf-
SYSROOT := $(shell readlink -f ..)/sysroot/
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
	for repo in $(REPOS); do git -C $$repo clean -dfxq; done

	cd qtbase && ./configure -release -opengl es2 -device linux-rasp-pi2-g++ \
		-qpa eglfs -no-libinput -no-linuxfb -no-xcb -no-kms -no-gbm -no-gtk -no-widgets -no-compile-examples \
		-device-option CROSS_COMPILE=$(TOOLCHAIN) -sysroot $(SYSROOT) \
		-opensource -confirm-license -make libs \
		-prefix /opt/qt -extprefix $(BASEDIR)/qt -hostprefix $(BASEDIR)/qt-host $(REDIRECT)

	$(MAKE) -C qtbase $(REDIRECT)
	$(MAKE) -C qtbase install $(REDIRECT)
	cd qtxmlpatterns && ../qt-host/bin/qmake $(REDIRECT)
	$(MAKE) -C qtxmlpatterns $(REDIRECT)
	$(MAKE) -C qtxmlpatterns install $(REDIRECT)
	cd qtdeclarative && ../qt-host/bin/qmake $(REDIRECT)
	$(MAKE) -C qtdeclarative $(REDIRECT)
	$(MAKE) -C qtdeclarative install $(REDIRECT)

	tar --exclude=qt/doc --exclude=qt/include -czf qt.tar.gz qt/

.PRECIOUS: %.timestamp
%.timestamp: % FORCE
	@echo Checking timestamps in $*...
	@if [ ! -f $*.timestamp ]; then echo $*/.git/logs/HEAD changed; touch -r $*/.git/logs/HEAD $*.timestamp; fi
	@if [ $*/.git/logs/HEAD -nt $*.timestamp ]; then echo $*/.git/logs/HEAD changed; touch -r $*/.git/logs/HEAD $*.timestamp; fi
	@for file in $$(git -C $* ls-files -mo --exclude-standard); do if [ $*/$$file -nt $*.timestamp ]; then echo $*/$$file changed; touch -r $*/$$file $*.timestamp; fi; done

FORCE: ;

pull: $(REPOS)
	for repo in $(REPOS); do git -C $$repo pull; done

clean:
	for repo in $(REPOS); do git -C $$repo clean -dfxq; done
	rm -rf --one-file-system qt/ qt-host/ *.timestamp qt.tar.gz

.PHONY: clean
