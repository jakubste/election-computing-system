\NeedsTeXFormat{LaTeX2e} %
\ProvidesClass{aghthesis}

% DECLARING OPTIONS

\DeclareOption{polish}
{
\newcommand*{\LangAgh}{Akademia G\'{o}rniczo-Hutnicza\\[2mm] im. Stanis\l{}awa Staszica w Krakowie}
\newcommand*{\LangFaculty}{Wydzia{\l} Informatyki, Elektroniki i Telekomunikacji\\[2mm] Katedra Informatyki}
\newcommand*{\LangSupervisor}{Opiekun:}
\newcommand*{\LangStatementHead}{O\'SWIADCZENIE AUTOR\'OW PRACY}
\newcommand*{\LangStatementBody}{
Uprzedzeni o odpowiedzialno\'sci karnej na podstawie art. 115 ust. 1 i 2 ustawy z dnia 
4 lutego 1994 r. o prawie autorskim i prawach pokrewnych (t.j. Dz.U. z 2006 r. Nr 90, poz. 631 z p\'o\'zn. zm.):\\
``Kto przyw{\l}aszcza sobie autorstwo albo wprowadza w b{\l}\k{a}d co do autorstwa 
ca{\l}o\'sci lub cz\k{e}\'sci cudzego utworu albo artystycznego wykonania, podlega grzywnie, karze 
ograniczenia wolno\'sci albo pozbawienia wolno\'sci do lat 3. Tej samej karze podlega, kto 
rozpowszechnia bez podania nazwiska lub pseudonimu tw\'orcy cudzy utw\'or 
w wersji oryginalnej albo w postaci opracowania, artystyczne wykonanie albo publicznie zniekszta{\l}ca 
taki utw\'or, artystyczne wykonanie, fonogram, wideogram lub nadanie.'',\\
a tak\.ze uprzedzeni o odpowiedzialno\'sci dyscyplinarnej na podstawie art. 211 ust. 1 ustawy z dnia 
27 lipca 2005 r. Prawo o szkolnictwie wy\.zszym (t.j. Dz. U. z 2012 r. poz. 572, z p\'o\'zn. zm.) ``Za naruszenie przepis\'ow obowi\k{a}zuj\k{a}cych w uczelni oraz za czyny uchybiaj\k{a}ce godno\'sci studenta student ponosi odpowiedzialno\'s\'c dyscyplinarn\k{a} przed komisj\k{a} dyscyplinarn\k{a} albo przed s\k{a}dem kole\.ze\'nskim samorz\k{a}du studenckiego, zwanym dalej `s\k{a}dem kole\.ze\'nskim'{''}, o\'swiadczamy, \.ze niniejsz\k{a} prac\k{e} dyplomow\k{a} wykonali\'smy osobi\'scie, samodzielnie i \.ze nie korzysta{\l}i\'smy ze \'zr\'ode{\l} innych ni\.z wymienione w pracy.
}
\newcommand*{\LangSignature}{PODPIS}
\newcommand*{\LangThesisType}{Projekt in\.zynierski}
}

\DeclareOption{english}
{
\newcommand*{\LangAgh}{AGH University of Science and Technology}
\newcommand*{\LangFaculty}{Faculty of Computer Science, Electronics and Telecommunications\\[1mm] Department of Computer Science}
\newcommand*{\LangSupervisor}{Supervisor:}
\newcommand*{\LangStatementHead}{NON-PLAGIARISM STATEMENT}
\newcommand*{\LangStatementBody}{I hereby declare that I have written this thesis completely by myself, that I have used no other sources or resources than the ones mentioned,
and that I am aware of the rules of the Penal Code referring to criminal liability for providing false evidence.}
\newcommand*{\LangSignature}{SIGNATURE}
\newcommand*{\LangThesisType}{Final project}
}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}


% PROCESSING OPTIONS
\ProcessOptions
\LoadClass[a4paper, twoside]{article}
% \LoadClass[a4paper, twoside]{article} - dwustronne drukowanie (zamiast liniji wyżej)


\RequirePackage{setspace}
\RequirePackage{times}
\RequirePackage[T1]{fontenc}
\RequirePackage{graphicx}
\RequirePackage{geometry}
\RequirePackage[usenames]{color}
\RequirePackage{fancyhdr}
\RequirePackage{titlesec}
\RequirePackage{babel}



\addto\captionspolish{%
  \def\bibname{Materia{\l}y {\'z}r{\'o}d{\l}owe}%
  \def\refname{Materia{\l}y {\'z}r{\'o}d{\l}owe}%
  \def\listtablename{Spis tabel}%
  \def\tablename{Tabela}%
}


\geometry{bindingoffset=10mm, lmargin=15mm, rmargin=25mm, tmargin=25mm, bmargin=25mm, foot=10mm, head=10mm}


\renewcommand{\baselinestretch}{1.1}

\def\title#1        {\gdef\@title{#1}}
\def\en_title#1     {\gdef\@en_title{#1}}
\def\faculty#1      {\gdef\@faculty{#1}}
\def\thesistype#1   {\gdef\@thesistype{#1}}
\def\supervisor#1   {\gdef\@supervisor{#1}}

\bibliographystyle{abbrv}

%------------------------------------------------------------------------------


\renewcommand{\maketitle}{%


\newpage \titlepage

\begin{center}

{\Large{\bfseries{\textsc \LangAgh}}}

\vspace*{1mm}\rule{.9\textwidth}{1mm}\vspace*{1mm}

{\large \LangFaculty}\vspace*{1cm}

\includegraphics[width=70pt,viewport=250 350 350 500]{agh.pdf}

\vspace*{1cm}
{\huge\scshape \LangThesisType}\\
\vspace*{2cm}

\doublespacing
{\huge{\bfseries\scshape \@title}}\\
\singlespacing
{\scshape\@en_title}
\vspace*{1.5cm}


{\Large\scshape 
\begin{doublespacing}
\@author
\end{doublespacing}
}\\

\vfill

\singlespacing

\large{\scshape \LangSupervisor}\\
{\@supervisor}
\vfill

\rule{.7\textwidth}{1mm}\\
\vspace*{1mm}
{\large Krak\'{o}w \@date}

\end{center}


\newpage
\thispagestyle{empty}

%\vspace*{15cm}
\mbox{}
\vfill

\begin{flushright}
\begin{minipage}[!h]{13cm}
\mbox{\large{\scshape \textbf{\LangStatementHead}}}\\[3mm]
{\scshape \LangStatementBody}\\
\end{minipage}

\vspace{2cm}
\makebox[6cm][s]{\dotfill}\par
\makebox[6cm][c]{\small \LangSignature} \\
\vspace{2cm}
\makebox[6cm][s]{\dotfill}\par
\makebox[6cm][c]{\small \LangSignature} \\
\vspace{2cm}
\makebox[6cm][s]{\dotfill}\par
\makebox[6cm][c]{\small \LangSignature}

\end{flushright}

%------------------------------------------------------------------------------

\clearpage
\setcounter{page}{3}

}

%\ProcessOptions

\pagestyle{fancy}
\renewcommand{\sectionmark}[1]{\markright{\thesection.\ #1}}
\renewcommand{\headrulewidth}{0.5pt}
\renewcommand{\footrulewidth}{0.5pt}
\fancyhf{}
\fancyhead{}

\fancyhead[LE]{\bfseries \thepage}
\fancyhead[RO]{\bfseries \thepage}
\cfoot{\@title}

\frenchspacing
\sloppy
\widowpenalty     9999
\clubpenalty      9999
\flushbottom




\titleformat{\section}[block]
{\bfseries\Large}{\filright \Large\thesection. }{0ex}{}
\titleformat{\subsection}[block]
{\bfseries\large}{\filright \large\thesubsection. }{0ex}{}
\titleformat{\subsubsection}[block]
{\bfseries\normalsize}{\filright \normalsize\thesubsubsection. }{0ex}{}
