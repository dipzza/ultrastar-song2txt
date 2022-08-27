DOC := proyecto.tex

ignored_envs := otherlanguage,displaymath
ignored_rules := sh:seclen,sh:stacked
ignored_macros := tableofcontents,listoffigures,listoftables,begin,centeroffset,oddsidemargin,evensidemargin,centering,bfseries,end,cleardoublepage,setlength,texttt
dict_es := ../.github/workflows/words-allowlist.txt

all: doc

doc: $(DOC:.tex=.pdf)

all: proyecto.pdf

%.pdf: %.tex
	pdflatex $< && bibtex $* && pdflatex $< && pdflatex $<

clean:
	rm -f *.log *.toc *.out *.bbl *.lof *.lot *.blg *.aux *.synctex.gz

check: es-check en-check

es-check:
	textidote --check es --ignore $(ignored_rules) --remove $(ignored_envs) --remove-macros $(ignored_macros) --dict $(dict_es) proyecto.tex

en-check:
	textidote --check en --read-all --ignore $(ignored_rules) --remove-macros $(ignored_macros) prefacios/english_abstract.tex
