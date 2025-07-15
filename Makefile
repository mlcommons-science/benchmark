# makefile that will create all the content

#FILES=source/benchmarks.yaml#source/benchmarks-addon.yaml
FILES=source/benchmark-entry-comment-gregor.yaml

SCRIPT=bin/generate.py

COLUMNS=date,name,domain,focus,keyword,task_types,metrics,models,cite

.PHONY: all content single tex pdf

all: content standalone pdf
	echo TODO

content: md tex
	echo DONE

md:
	python ${SCRIPT} --files ${FILES}  --format=md --out=./content --index --columns ${COLUMNS}

tex-old:
	python ${SCRIPT} --files ${FILES} --format=tex --out=./content --standalone --columns=${COLUMNS}
	# python ${SCRIPT} --files ${FILES} --format=tex --out=./content --standalone --columns=${COLUMNS}
	cd content/tex; bibtool -s -i benchmarks.bib -o tmp.bib
	cd content/tex; mv tmp.bib benchmarks.bib

tex:
	python ${SCRIPT} --files ${FILES} --format=tex --out=./content --standalone --columns=${COLUMNS} # --tex=benchmarks.tex
	cd content/tex; bibtool -s -i benchmarks.bib -o tmp.bib
	cd content/tex; mv tmp.bib benchmarks.bib


standalone:
	python ${SCRIPT} --files=${FILES} --format=tex --standalone --out-dir ./content


pdf: tex
	cd content/tex; latexmk -pdf -silent benchmarks.tex

clean:
	cd content/tex && latexmk -C
	# Remove existing benchmark markdown files if they exist
	rm -f content/benchmarks.md
	rm -rf content/md_pages


view:
	open content/tex/benchmarks.pdf

debug: tex pdf view

check:
	python ${SCRIPT} --files ${FILES} --check --format=tex 
