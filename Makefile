# makefile that will create all the content

FILES=source/benchmarks.yaml

.PHONY: all content single

all: content standalone pdf
	echo TODO

content: md tex
	echo DONE

md:
	python bin/generate.py --files ${FILES}  --format md --out ./content

tex:
	python bin/generate.py --files ${FILES} --format=tex

standalone:
	python bin/generate.py --files=${FILES} --format=tex --standalone --out-dir ./content

# produce file content/tex/benchmarks.pdf
pdf:
	cd content/tex; pdflatex benchmarks
	cd content/tex; bibtex benchmarks
	cd content/tex; pdflatex benchmarks
	cd content/tex; pdflatex benchmarks