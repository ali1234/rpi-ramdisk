include ../toolchain.mk

PREFIX := /opt/apds9960d

REPOS := apds9960d

all: apds9960d.tar.gz

apds9960d.tar.gz: apds9960d.service $(shell for repo in $(REPOS); do echo $$repo.timestamp; done )
	rm -rf --one-file-system $(STAGE)
	mkdir -p $(STAGE)/etc/systemd/system
	mkdir -p $(STAGE)$(PREFIX)/bin

	rm -rf --one-file-system build
	mkdir build
	cd build && cmake -DCMAKE_SYSTEM_NAME=Linux -DCMAKE_C_COMPILER=$(TOOLCHAIN)gcc \
		-DCMAKE_CXX_COMPILER=$(TOOLCHAIN)g++ -DCMAKE_SYSROOT=$(SYSROOT) \
		-DCMAKE_FIND_ROOT_PATH_MODE_PROGRAM=NEVER \
		-DCMAKE_FIND_ROOT_PATH_MODE_INCLUDE=ONLY \
		-DCMAKE_FIND_ROOT_PATH_MODE_LIBRARY=ONLY \
		../apds9960d && make

	cp build/apds9960d $(STAGE)$(PREFIX)/bin
	cp apds9960d.service $(STAGE)/etc/systemd/system

	tar -C $(STAGE) -czf apds9960d.tar.gz .

include ../../include/timestamp.mk

install: apds9960d.tar.gz
	tar -xf apds9960d.tar.gz -C $(DESTDIR)
	$(MYCHROOT) $(DESTDIR) /bin/systemctl reenable apds9960d.service

clean:
	rm -rf --one-file-system $(STAGE) build apds9960d.tar.gz

.PHONY: clean install
