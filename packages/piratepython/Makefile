include ../toolchain.mk

ifeq ("$(VERBOSE_PIRATEPYTHON_BUILD)","1")
REDIRECT :=
else
REDIRECT := > /dev/null
endif

all: pymtpd.tar.gz

pymtpd.tar.gz: piratepython.service pp-restart.service pp-restart.path
	rm -rf --one-file-system $(STAGE)

	mkdir -p $(STAGE)/etc/systemd/system

	cp piratepython.service $(STAGE)/etc/systemd/system/
	cp pp-restart.service $(STAGE)/etc/systemd/system/
	cp pp-restart.path $(STAGE)/etc/systemd/system/

	mkdir -p $(STAGE)/mtp
	cp main.py $(STAGE)/mtp

	tar -C $(STAGE) -czf piratepython.tar.gz .

clean:
	rm -rf --one-file-system $(STAGE) $(HOSTPREFIX) *.timestamp qt.tar.gz

install: piratepython.tar.gz
	tar -xf piratepython.tar.gz -C $(DESTDIR)
	$(MYCHROOT) $(DESTDIR) /bin/systemctl reenable piratepython.service
	$(MYCHROOT) $(DESTDIR) /bin/systemctl reenable pp-restart.service
	$(MYCHROOT) $(DESTDIR) /bin/systemctl reenable pp-restart.path

.PHONY: clean install
