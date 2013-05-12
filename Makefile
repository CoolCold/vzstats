NAME=vzstats
ETCDIR=/etc/vz
SBINDIR=/usr/sbin
MANDIR=/usr/share/man
MAN8DIR=$(MANDIR)/man8
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
	mkdir -p $(DESTDIR)/$(MAN8DIR)
	install $(NAME).8 $(DESTDIR)/$(MAN8DIR)
.PHONY: install

BASHCDIR=/etc/bash_completion.d
install-bashcomp:
	mkdir -p $(DESTDIR)$(BASHCDIR)
	install bash_completion.sh $(DESTDIR)$(BASHCDIR)/$(NAME)
.PHONY: install-bashcomp

CRONDIR=/etc/cron.monthly
install-cronjob:
	mkdir -p $(DESTDIR)$(CRONDIR)
	echo "$(NAME)" > $(DESTDIR)$(CRONDIR)/$(NAME)
	chmod a+x $(DESTDIR)$(CRONDIR)/$(NAME)

.PHONY: install-cronjob

install-all: install install-bashcomp install-cronjob
.PHONY: install-all

clean:
.PHONY: clean

# Tar and rpm build
SPEC=$(NAME).spec
VERSION_SPEC=$(shell awk '/^Version:/{print $$2}' $(SPEC))
VERSION_FILE=$(shell awk -F = '($$1=="VERSION") {print $$2}' $(NAME))
RELEASE=$(shell awk '/^%define rel / {if ($$3 != 1) print "-"$$3}' $(SPEC))
NAMEVER=$(NAME)-$(VERSION_SPEC)$(RELEASE)
TARBALL=$(NAMEVER).tar.bz2

check-version:
	test "$(VERSION_SPEC)" = "$(VERSION_FILE)" || exit 1
.PHONY: check-version

dist: tar
tar: $(TARBALL)
.PHONY: dist tar

$(TARBALL): check-version clean
	rm -f ../$(NAMEVER)
	ln -s `pwd | awk -F / '{print $$NF}'` ../$(NAMEVER)
	tar --directory .. --exclude .git --exclude .depend \
		--exclude-from .gitignore \
		-cvhjf ../$(TARBALL) $(NAMEVER)
	rm -f $(TARBALL)
	mv ../$(TARBALL) .
	rm -f ../$(NAMEVER)

rpms: tar
	rpmbuild -ta $(TARBALL) ${RPMB_ARGS}
.PHONY: rpms

