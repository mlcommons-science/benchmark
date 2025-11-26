# makefile that will create all the content
SUDO := $(shell command -v sudo >/dev/null 2>&1 && echo sudo || echo)

BASE=.

FILES=${BASE}/source/benchmarks.yaml,${BASE}/source/benchmarks-addon.yaml 

CHECK_FILES=${BASE}/source/benchmarks.yaml,${BASE}/source/benchmarks-addon.yaml 

SCRIPT=bin/generate.py

COLUMNS=date,name,domain,focus,keywords,task_types,metrics,models,cite,ratings.software.rating,ratings.software.reason,ratings.specification.rating,ratings.specification.reason,ratings.dataset.rating,ratings.dataset.reason,ratings.metrics.rating,ratings.metrics.reason,ratings.reference_solution.rating,ratings.reference_solution.reason,ratings.documentation.rating,ratings.documentation.reason

.PHONY: all content single tex pdf publish

define BANNER
	@echo
    @echo "\033[34m# ====================================================================="
    @echo "# "$(1)
    @echo "# =====================================================================\033[0m"
endef

all: pdf mkdocs
	echo "If you see no errors it is finished."

ls:
	cd ${BASE}; pwd; ls
	ls ${BASE}

install_latex:
	$(SUDO) apt-get update
	$(SUDO) apt-get install texlive-full
	$(SUDO) apt-get install latexmk
	$(SUDO) apt-get install bibtool
	$(SUDO) apt-get install biber
	$(SUDO) apt-get update
	biber --version
	latexmk --version
	pdflatex --version

install:
	pip install -r requirements.txt

content: md tex
	echo DONE

md:
	python ${SCRIPT} --files=${FILES}  --format=md --outdir=./content --columns ${COLUMNS}

DOCS=www/science-ai-benchmarks/docs
WWW=www/science-ai-benchmarks
LATEX_DIR=content/tex
LATEX_EXCLUDE=content/latex-export.exclude
LATEX_DOWNLOAD_DIR=content/downloads
LATEX_ZIP_SRC=$(LATEX_DOWNLOAD_DIR)/benchmarks-latex.zip
LATEX_ZIP_DEST=$(DOCS)/downloads/benchmarks-latex.zip

SERVE_HOST ?= 127.0.0.1

publish: pdf mkdocs
	$(call BANNER,"Publishing from ${DOCS}") 
	-git commit -am "Update documentation"
	-git push
	cd ${WWW}; mkdocs gh-deploy

mkdocs: latex-export
	$(call BANNER,"Generating MkDocs content")
	python ${SCRIPT} --files=${FILES}  --format=mkdocs --outdir=./content --columns ${COLUMNS}
	mkdir -p ${DOCS}/tex/images
	mkdir -p ${DOCS}/md
	mkdir -p ${DOCS}/assets
	mkdir -p ${DOCS}/downloads
	cp -r content/md ${DOCS}
	cp -r content/tex ${DOCS}
	cp -r content/assets ${DOCS}
	cp content/mkdocs.yml ${WWW}
	cp source/index.md ${DOCS}/index.md
	cp content/tex/benchmarks.pdf ${DOCS}/benchmarks.pdf
	cp $(LATEX_ZIP_SRC) $(LATEX_ZIP_DEST)
	$(call BANNER, "CLEAN LaTeX")
	
tex:
	python ${SCRIPT} --files=${FILES} --format=tex --outdir=./content --standalone --columns=${COLUMNS}
	cd content/tex; bibtool -s -i benchmarks.bib -o tmp.bib
	sleep 1
	cd content/tex; mv tmp.bib benchmarks.bib

standalone:
	python ${SCRIPT} --files=${FILES} --format=tex --standalone --out-dir ./content

pdf: tex
	cd content/tex; latexmk -pdf -silent benchmarks.tex

latex-export:
	mkdir -p $(LATEX_DOWNLOAD_DIR)
	cd $(LATEX_DIR); zip -rq $(abspath $(LATEX_ZIP_SRC)) . -x@$(abspath $(LATEX_EXCLUDE))

clean:
	rm -rf content/md
	rm -rf content/tex

view:
	open content/tex/benchmarks.pdf

debug: tex pdf view

check:
	python ${SCRIPT} --files ${CHECK_FILES} --check 

check_urls:
	python ${SCRIPT} --files ${CHECK_FILES} --check_url 

u:
	python ${SCRIPT} --files ${CHECK_FILES} --check_url --url=https://pubs.acs.org/doi/10.1021/acscatal.2c05426

log:
	open -a Aquamacs content/tex/benchmarks.log

structure:
	python ${SCRIPT} --files=source/benchmarks.yaml --check_structure 
	python ${SCRIPT} --files=source/benchmarks.yaml --check_structure --structure=source/benchmarks-addon.yaml
	python ${SCRIPT} --files=source/benchmarks-addon.yaml --check_structure 

serve: mkdocs
	cd www/science-ai-benchmarks; mkdocs serve -a $(SERVE_HOST):8000
