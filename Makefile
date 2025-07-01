# makefile that will create all the content

FILES=source/benchmarks.yaml source/benchmarks_addition.yaml 
SCRIPT=bin/generate-fermi.py

COLUMNS=date,name,domain,focus,keyword,task_types,metrics,models,cite

.PHONY: all content single tex pdf

all: content standalone pdf
	echo TODO

content: md tex
	echo DONE

md:
	python ${SCRIPT} --files ${FILES}  --format=md --out=./content --index

tex:
	python ${SCRIPT} --files ${FILES} --format=tex --out=./content --standalone --columns=${COLUMNS}
	cd content/tex; bibtool -s -i benchmarks.bib -o tmp.bib
	cd content/tex; mv tmp.bib benchmarks.bib


standalone:
	python ${SCRIPT} --files=${FILES} --format=tex --standalone --out-dir ./content

# produce file content/tex/benchmarks.pdf
pdf2: tex 
	cd content/tex; pdflatex benchmarks
	cd content/tex; biber benchmarks
	cd content/tex; pdflatex benchmarks
	cd content/tex; pdflatex benchmarks

pdf: tex
	cd content/tex; latexmk -pdf -silent benchmarks.tex

clean:
	cd content/tex && latexmk -C
	rm -rf content/md/benchmarks.*


view:
	open content/tex/benchmarks.pdf

debug: tex pdf view
