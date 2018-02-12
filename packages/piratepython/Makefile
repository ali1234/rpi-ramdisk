include ../toolchain.mk

PREFIX := /opt/pymtpd

ifeq ("$(VERBOSE_PIRATEPYTHON_BUILD)","1")
REDIRECT :=
else
REDIRECT := > /dev/null
endif

all: pymtpd.tar.gz

pymtpd.tar.gz: $(shell for repo in $(REPOS); do echo $$repo.timestamp; done )
	rm -rf --one-file-system $(STAGE)

	mkdir -p $(STAGE)/etc/systemd/system
	cp piratepython.service $(STAGE)/etc/systemd/system/
	cp pp-restart.service $(STAGE)/etc/systemd/system/

	tar -C $(STAGE) --exclude=.$(PREFIX)/doc --exclude=.$(PREFIX)/include -czf piratepython.tar.gz .

include ../../include/timestamp.mk

pull:
	git submodule update --remote .

clean:
	for repo in $(REPOS); do git -C $$repo clean -dfxq; done
	rm -rf --one-file-system $(STAGE) $(HOSTPREFIX) *.timestamp qt.tar.gz

install: piratepython.tar.gz
	tar -xf piratepython.tar.gz -C $(DESTDIR)
	$(MYCHROOT) $(DESTDIR) /bin/systemctl reenable piratepython.service
	$(MYCHROOT) $(DESTDIR) /bin/systemctl reenable pp-restart.service

.PHONY: clean install
