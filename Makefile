PROGRAM_NAME=r5steg
#VERSION=0.1

PROGRAM_DIR=/usr/bin
DATA_DIR=/usr/share
LICENSE_DIR=$(DATA_DIR)/licenses
DOC_DIR=$(DATA_DIR)/doc
localedir=$(DATA_DIR)/locale


install:
	install -Dm755 r5steg.py $(PROGRAM_DIR)/$(PROGRAM_NAME)
	install -Dm644 LICENSE $(LICENSE_DIR)/$(PROGRAM_NAME)/LICENSE
	install -Dm644 README.md $(DOC_DIR)/$(PROGRAM_NAME)/README.md
	for i in $$(cd po/ && ls *.po | sed 's/\.po$$//'); do \
		msgfmt --statistics po/$$i.po -o po/$$i.mo; \
		install -Dm644 po/$$i.mo "$(localedir)/$$i/LC_MESSAGES/r5steg.mo"; \
	done

uninstall:
	rm -Rf $(PROGRAM_DIR)/$(PROGRAM_NAME)
	rm -Rf $(LICENSE_DIR)/$(PROGRAM_NAME)
	rm -Rf $(DOC_DIR)/$(PROGRAM_NAME)
	for i in $$(cd po/ && ls ??.po | sed 's/\.po$$//'); do \
		rm -f "$(localedir)/$$i/LC_MESSAGES/r5steg.mo"; \
	done

clean:
	rm -f po/*.mo
