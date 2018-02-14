include ../toolchain.mk

PREFIX := /opt/qt

REPOS := qmlrss

all: qmlrss.tar.gz

qmlrss.tar.gz: qmlrss.service $(shell for repo in $(REPOS); do echo $$repo.timestamp; done )
	rm -rf --one-file-system $(STAGE)
	mkdir -p $(STAGE)/etc/systemd/system
	mkdir -p $(STAGE)/opt/qt/bin

	cd qmlrss && ../../qt/qt-host/bin/qmake
	$(MAKE) -C qmlrss
	cp qmlrss/qmlrss $(STAGE)/opt/qt/bin/

	cp qmlrss.service $(STAGE)/etc/systemd/system/

	tar -C $(STAGE) -czf qmlrss.tar.gz .

include ../../include/timestamp.mk

install: qmlrss.tar.gz
	tar -xf qmlrss.tar.gz -C $(DESTDIR)
	$(MYCHROOT) $(DESTDIR) /bin/systemctl reenable qmlrss.service

clean:
	rm -rf --one-file-system $(STAGE) qmlrss.tar.gz

.PHONY: clean install
