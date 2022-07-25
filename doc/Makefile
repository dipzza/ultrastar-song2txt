DOC := proyecto.tex

spellargs := --ignore sh:seclen,sh:stacked --remove-macros tableofcontents,listoffigures,listoftables,begin,centeroffset,oddsidemargin,evensidemargin,centering,bfseries,end,cleardoublepage,setlength,texttt

all: doc

doc: $(DOC:.tex=.pdf)

all: proyecto.pdf

%.pdf: %.tex
	pdflatex $< && bibtex $* && pdflatex $< && pdflatex $<

clean:
	rm -f *.log *.toc *.out *.bbl *.lof *.lot *.blg *.aux *.synctex.gz

check: es-check en-check

es-check:
	textidote --check es --remove otherlanguage --dict ../.github/workflows/words-allowlist.txt $(spellargs) proyecto.tex

en-check:
	textidote --check en --read-all $(spellargs) prefacios/english_abstract.tex
