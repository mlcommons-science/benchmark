# makefile that will create all the content

FILES=source/benchmarks.yaml
FILES2=source/benchmarks-addon.yaml
FILES3=source/benchmarks.yaml source/benchmarks-addon.yaml
FILES4=source/benchmarks.yaml source/benchmarks-test.yaml

SCRIPT=bin/generate-fermi.py

COLUMNS=date,name,domain,focus,keyword,task_types,metrics,models,cite
COLUMNS2=date,name,domain,focus,keyword,task_types,metrics,models,cite,

.PHONY: all content single tex pdf

all: content standalone pdf
	echo TODO

content: md tex
	echo DONE

md:
	python ${SCRIPT} --files ${FILES}  --format=md --out=./content --index

md-fermi:
	python ${SCRIPT} --files ${FILES}  --format=md --out=./content --index

tex:
	python ${SCRIPT} --files ${FILES} --format=tex --out=./content --standalone --columns=${COLUMNS}
	# python ${SCRIPT} --files ${FILES} --format=tex --out=./content --standalone --columns=${COLUMNS}
	cd content/tex; bibtool -s -i benchmarks.bib -o tmp.bib
	cd content/tex; mv tmp.bib benchmarks.bib

tex-fermi:
	python ${SCRIPT} --files ${FILES4} --format=tex --out=./content --standalone --columns=${COLUMNS} # --tex=benchmarks.tex
	cd content/tex; bibtool -s -i benchmarks.bib -o tmp.bib
	cd content/tex; mv tmp.bib benchmarks.bib


standalone:
	python ${SCRIPT} --files=${FILES} --format=tex --standalone --out-dir ./content


pdf: tex
	cd content/tex; latexmk -pdf -silent benchmarks.tex

pdf-fermi: tex-fermi
	cd content/tex; latexmk -pdf -silent benchmarks.tex

clean:
	cd content/tex && latexmk -C
	rm -rf content/md/benchmarks.*


view:
	open content/tex/benchmarks.pdf

debug: tex pdf view

check:
	python -c "import yaml, sys; print(yaml.safe_load(sys.stdin))" < source/benchmarks.yaml
	python -c "import yaml, sys; print(yaml.safe_load(sys.stdin))" < source/benchmarks-addon.yaml