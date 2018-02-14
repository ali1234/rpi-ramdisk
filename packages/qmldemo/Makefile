include ../toolchain.mk

PREFIX := /opt/qt

all: qmldemo.tar.gz

qmldemo.tar.gz: qmldemo.service qmldemo.qml
	rm -rf --one-file-system $(STAGE)
	mkdir -p $(STAGE)/etc/systemd/system
	mkdir -p $(STAGE)/opt/qt
	cp qmldemo.service $(STAGE)/etc/systemd/system/
	cp qmldemo.qml $(STAGE)/opt/qt/

	tar -C $(STAGE) -czf qmldemo.tar.gz .

install: qmldemo.tar.gz
	tar -xf qmldemo.tar.gz -C $(DESTDIR)
	$(MYCHROOT) $(DESTDIR) /bin/systemctl reenable qmldemo.service

clean:
	rm -rf --one-file-system $(STAGE) qmldemo.tar.gz

.PHONY: clean install
