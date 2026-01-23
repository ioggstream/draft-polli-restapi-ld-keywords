LIBDIR := lib

# Include vocab directory files in GitHub Pages
GHPAGES_EXTRA := vocab/jsonld-dialect.json vocab/jsonld-meta.json vocab/README.md vocab/semantic-data-package.json  vocab/table-schema-jsonld.json

include $(LIBDIR)/main.mk

$(LIBDIR)/main.mk:
ifneq (,$(shell grep "path *= *$(LIBDIR)" .gitmodules 2>/dev/null))
	git submodule sync
	git submodule update $(CLONE_ARGS) --init
else
	git clone -q --depth 10 $(CLONE_ARGS) \
	    -b main https://github.com/martinthomson/i-d-template $(LIBDIR)
endif
