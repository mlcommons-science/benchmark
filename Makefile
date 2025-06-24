# makefile that will create all the content

FILES=source/benchmarks.yaml

COLUMNS=date,name,domain,focus,keyword,task_types,metrics,models,cite

.PHONY: all content single tex pdf

all: content standalone pdf
	echo TODO

content: md tex
	echo DONE

md:
	python bin/generate.py --files ${FILES}  --format=md --out=./content/md

tex:
	python bin/generate.py --files ${FILES} --format=tex --out=./content --standalone --columns=${COLUMNS}
	cd content/tex; bibtool -s -i benchmarks.bib -o tmp.bib
	cd content/tex; mv tmp.bib benchmarks.bib


standalone:
	python bin/generate.py --files=${FILES} --format=tex --standalone --out-dir ./content

# produce file content/tex/benchmarks.pdf
pdf: tex 
	cd content/tex; pdflatex benchmarks
	cd content/tex; bibtex benchmarks
	cd content/tex; pdflatex benchmarks
	cd content/tex; pdflatex benchmarks

clean:
	rm -rf content/tex/benchmarks.*
	rm -rf content/md/benchmarks.*


view:
	open content/tex/benchmarks.pdf

debug: tex pdf view
