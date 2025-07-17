# makefile that will create all the content

FILES=source/benchmarks-addon-new.yaml#source/benchmarks.yaml
# FILES=source/benchmark-entry-comment-gregor.yaml

SCRIPT=bin/generate.py

COLUMNS=date,name,domain,focus,keywords,task_types,metrics,models,cite

.PHONY: all content single tex pdf

all: content standalone pdf
	echo TODO

g:
	python bin/test.py

summary:
	python bin/summary.py --graph=pdf
	#cd content/summary; bibtool -s -i benchmarks.bib -o tmp.bib
	cd content/summary; latexmk -pdf -silent summary.tex
	open content/summary/summary.pdf 

install:
	pip install cloudmesh-common
	pip install pybtex

content: md tex
	echo DONE

md:
	python ${SCRIPT} --files ${FILES}  --format=md --out=./content --index --columns ${COLUMNS}

tex:
	python ${SCRIPT} --files ${FILES} --format=tex --out=./content --standalone --columns=${COLUMNS}
	cd content/tex; bibtool -s -i benchmarks.bib -o tmp.bib
	cd content/tex; mv tmp.bib benchmarks.bib


standalone:
	python ${SCRIPT} --files=${FILES} --format=tex --standalone --out-dir ./content


pdf: tex
	cd content/tex; latexmk -pdf -silent benchmarks.tex

clean:
	cd content/tex && latexmk -C
	# Remove existing benchmark files if they exist
	rm -f content/md/benchmarks.md
	rm -rf content/md_pages
	rm -rf content/tex_pages


view:
	open content/tex/benchmarks.pdf

debug: tex pdf view

check:
	python ${SCRIPT} --files ${FILES} --check --outdir foo --format=tex 
