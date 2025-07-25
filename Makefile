# makefile that will create all the content

FILES=source/benchmarks-addon.yaml
# FILES=source/benchmarks.yaml source/benchmarks-addon.yaml

CHECK_FILES=source/benchmarks.yaml,source/benchmarks-addon.yaml 

# FILES=source/benchmark-entry-comment-gregor.yaml

SCRIPT=bin/generate.py

COLUMNS=date,name,domain,focus,keywords,task_types,metrics,models,cite,ratings.specification.rating,ratings.specification.reason,ratings.dataset.rating,ratings.dataset.reason,ratings.metrics.rating,ratings.metrics.reason,ratings.reference_solution.rating,ratings.reference_solution.reason,ratings.documentation.rating,ratings.documentation.reason
#COLUMNS=date,expired,valid,name,url,domain,focus,keywords,summary,task_types,ai_capability_measured,metrics,models,notes,cite,ratings.specification.rating,ratings.specification.reason,ratings.dataset.rating,ratings.dataset.reason,ratings.metrics.rating,ratings.metrics.reason,ratings.reference_solution.rating,ratings.reference_solution.reason,ratings.documentation.rating,ratings.documentation.reason
#COLUMNS=date,name,url,domain,focus,keywords,summary,task_types,ai_capability_measured,metrics,models,notes,cite,ratings.specification.rating,ratings.specification.reason,ratings.dataset.rating,ratings.dataset.reason,ratings.metrics.rating,ratings.metrics.reason,ratings.reference_solution.rating,ratings.reference_solution.reason,ratings.documentation.rating,ratings.documentation.reason

.PHONY: all content single tex pdf publish

all: pdf md publish
	echo "If you see no errors it is finished."
	
g:
	python bin/test.py

summary:
	python bin/summary.py --file source/benchmarks-addon.yaml --graph=pdf
	python bin/summary.py --file source/benchmarks-addon.yaml --graph=png
	#cd content/summary; bibtool -s -i benchmarks.bib -o tmp.bib
	cd content/tex; latexmk -pdf -silent summary.tex
	open content/tex/summary.pdf 

install:
	pip install cloudmesh-common
	pip install pybtex
	pip install pylatexenc
	pip install bibtexparser
	pip install docopt
	pip install bs4
	pip install numpy
	pip install matplotlib
	pip install selenium

content: md tex
	echo DONE

md:
	python ${SCRIPT} --files=${FILES}  --format=md --outdir=./content --columns ${COLUMNS}

tex:
	python ${SCRIPT} --files=${FILES} --format=tex --outdir=./content --standalone --columns=${COLUMNS}
	cd content/tex; bibtool -s -i benchmarks.bib -o tmp.bib
	sleep 1
	cd content/tex; mv tmp.bib benchmarks.bib

t:
	python ${SCRIPT} --files=${FILES} --format=tex --outdir=./content --standalone --columns=${COLUMNS}
	cd content/tex; latexmk -pdf benchmarks.tex

standalone:
	python ${SCRIPT} --files=${FILES} --format=tex --standalone --out-dir ./content


pdf: tex
	cd content/tex; latexmk -pdf -silent benchmarks.tex

clean:
	rm -rf content/md
	rm -rf content/summary
	rm -rf content/md_pages
	rm -rf content/tex
	cd content/tex && latexmk -C


view:
	open content/tex/benchmarks.pdf

debug: tex pdf view

check:
	python ${SCRIPT} --files ${CHECK_FILES} --check 


check_url:
	python ${SCRIPT} --files ${CHECK_FILES} --check_url 

u:
	python ${SCRIPT} --files ${CHECK_FILES} --check_url --url=https://pubs.acs.org/doi/10.1021/acscatal.2c05426



log:
	open -a Aquamacs content/tex/benchmarks.log

publish:
	mkdir -p docs/tex/images
	mkdir -p docs/md
	
	cp -r content/md/* docs/md
	cp source/index.md docs/index.md
	cp content/tex/benchmarks.pdf docs/benchmarks.pdf
	cp content/tex/images/* docs/tex/images

structure:
	python ${SCRIPT} --files=source/benchmarks.yaml --check_structure 
	python ${SCRIPT} --files=source/benchmarks.yaml --check_structure --structure=source/benchmarks-addon.yaml
	python ${SCRIPT} --files=source/benchmarks-addon.yaml --check_structure 
	