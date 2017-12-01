include ../toolchain.mk

PREFIX := /opt/pymtpd

REPOS := pymtpd

ifeq ("$(VERBOSE_PYMTPD_BUILD)","1")
REDIRECT :=
else
REDIRECT := > /dev/null
endif

all: pymtpd.tar.gz

pymtpd.tar.gz: $(shell for repo in $(REPOS); do echo $$repo.timestamp; done )
	rm -rf --one-file-system $(STAGE)
	for repo in $(REPOS); do git -C $$repo clean -dfxq; done

	cd pymtpd && pip3 install --system --root=$(STAGE) --prefix=$(PREFIX) .

	mkdir -p $(STAGE)/etc/systemd/system
	cp pymtpd.service $(STAGE)/etc/systemd/system/

	tar -C $(STAGE) --exclude=.$(PREFIX)/doc --exclude=.$(PREFIX)/include -czf pymtpd.tar.gz .

include ../../include/timestamp.mk

pull:
	git submodule update --remote .

clean:
	for repo in $(REPOS); do git -C $$repo clean -dfxq; done
	rm -rf --one-file-system $(STAGE) $(HOSTPREFIX) *.timestamp qt.tar.gz

.PHONY: clean
