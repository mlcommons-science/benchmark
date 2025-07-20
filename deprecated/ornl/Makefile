FILES=source/benchmarks.yaml

COLUMNS=date,name,domain,focus,keyword,task_types,metrics,models,cite

.PHONY: all content single tex pdf clean view debug standalone pdf2

all: content standalone pdf
	echo TODO

content: md tex
	echo DONE

md:
	python bin/generate.py --files ${FILES}  --format=md --out=./content --index

tex:
	python bin/generate.py --files ${FILES} --format=tex --out=./content --standalone --columns=${COLUMNS}
	cd content/tex; bibtool -s -i benchmarks.bib -o tmp.bib
	cd content/tex; mv tmp.bib benchmarks.bib


standalone:
	python bin/generate.py --files=${FILES} --format=tex --standalone --out-dir ./content

# produce file content/tex/benchmarks.pdf
pdf2: tex 
	cd content/tex; pdflatex benchmarks
	cd content/tex; biber benchmarks
	cd content/tex; pdflatex benchmarks
	cd content/tex; pdflatex benchmarks

pdf: tex
	cd content/tex; latexmk -pdf -silent benchmarks.tex

clean:
	echo "HHHH"
	#rm -rf content/md/benchmarks.*
	#rm -rf content/tex/*
	# cd content/tex && latexmk -C

remove:
	echo "HHHH"
	#rm -rf content/md/benchmarks.*
	#rm -rf content/tex/*
	# cd content/tex && latexmk -C


view:
	open content/tex/benchmarks.pdf

debug: tex pdf view
