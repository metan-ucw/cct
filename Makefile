check:
	@cd tests && ./runtests.sh

regen:
	@cd tests && ./regen.sh

bindir=/usr/bin

ifdef DESTDIR
BINDIR=$(DESTDIR)$(bindir)
else
BINDIR=$(bindir)
endif

install:
	install -d "$(BINDIR)"
	install -m 775 cct.py "$(BINDIR)"
	cd "$(BINDIR)" && ln -sf cct.py cct
