# makefile that will create all the content

FILES=source/benchmarks.yaml

.PHONY: all content index

all: content index
	echo TODO

content:
	bin/tomd.py ${FILES} --out=content
	bin/toindex.py ${FILES} --out=content
	bin/tolongtable.py ${FILES} --out=content

index:
	echo TODO
