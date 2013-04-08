NAME=vzstats
ETCDIR=/etc/vz
SBINDIR=/usr/sbin
REPDIR=/usr/libexec/$(NAME)

all:
.PHONY: all

install:
	mkdir -p $(DESTDIR)$(ETCDIR)
	install $(NAME).conf $(DESTDIR)$(ETCDIR)
	mkdir -p $(DESTDIR)/$(SBINDIR)
	install $(NAME) $(DESTDIR)/$(SBINDIR)
	mkdir -p $(DESTDIR)/$(REPDIR)
	install bin/* $(DESTDIR)/$(REPDIR)

CRONDIR=/etc/cron.monthly
install-cronjob:
	mkdir -p $(DESTDIR)$(CRONDIR)
	echo "$(NAME)" > $(DESTDIR)$(CRONDIR)/$(NAME)
	chmod a+x $(DESTDIR)$(CRONDIR)/$(NAME)

.PHONY: install

clean:
.PHONY: clean

# Tar and rpm build
SPEC=$(NAME).spec
VERSION=$(shell awk '/^Version:/{print $$2}' $(SPEC))
RELEASE=$(shell awk '/^%define rel / {if ($$3 != 1) print "-"$$3}' $(SPEC))
NAMEVER=$(NAME)-$(VERSION)$(RELEASE)
TARBALL=$(NAMEVER).tar.bz2

dist: tar
tar: $(TARBALL)
.PHONY: dist tar

$(TARBALL): clean
	rm -f ../$(NAMEVER)
	ln -s `pwd | awk -F / '{print $$NF}'` ../$(NAMEVER)
	tar --directory .. --exclude-vcs --exclude .depend \
		--exclude-from .gitignore \
		-cvhjf ../$(TARBALL) $(NAMEVER)
	rm -f $(TARBALL)
	mv ../$(TARBALL) .
	rm -f ../$(NAMEVER)

rpms: tar
	rpmbuild -ta $(TARBALL) ${RPMB_ARGS}
.PHONY: rpms

