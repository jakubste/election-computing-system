%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%	File: aghdoc.cls 
%         
%	LaTeX Document class option "aghdoc" based on
%				Marcin Szpyrka's     (mszpyrka@agh.edu.pl)
%				and
%			   	Grzegorz J. Nalepa's  (gjn@agh.edu.pl)
%   			Latex Document class option "aghdpl"  
%	
%				AGH University of Science and Technology, Kraków, POLAND
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\message{ -------- [aghdoc.cls] -------- }       

\newif\ifpdflatex\pdflatexfalse
\NeedsTeXFormat{LaTeX2e} % 
\ProvidesClass{../aghdoc_version2} % Use this class in .tex files from subdirectories
\DeclareOption{pdflatex}{\pdflatextrue}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}} 
\ProcessOptions\LoadClass[a4paper,oneside]{report} 

\RequirePackage{times}
\RequirePackage[T1]{fontenc}
\RequirePackage{graphicx}
\RequirePackage{geometry}
\RequirePackage[usenames]{color}
\RequirePackage{fancyhdr}
\RequirePackage{url}
\RequirePackage{titlesec}
\RequirePackage{tocloft}

\geometry{lmargin=30mm, rmargin=20mm, tmargin=25mm, bmargin=25mm, foot=10mm, head=10mm}
\definecolor{Green}{rgb}{0.1,0.5,0.1}

\def\shorttitlePL#1   {\gdef\@shorttitlePL{#1}}
\def\shortauthor#1    {\gdef\@shortauthor{#1}}
\def\titlePL#1        {\gdef\@titlePL{#1}}
\def\facultyPL#1      {\gdef\@facultyPL{#1}}
\def\thesistypePL#1   {\gdef\@thesistypePL{#1}}
\def\supervisorPL#1   {\gdef\@supervisorPL{#1}}
\def\departmentPL#1   {\gdef\@departmentPL{#1}}

% \thesisheaders
% 
% \pagestyle{fancy}

%\bibliographystyle{abbrv}
\linespread{1.3}
%\renewcommand{\labelitemi}{--}

%------------------------------------------------------------------------------

\newcommand{\titlepages}{%

\newpage \titlepage 

\begin{center}

{\sffamily{\Large{\bfseries{\textsc Akademia G\'{o}rniczo-Hutnicza\\[2mm]
im. Stanis\l{}awa Staszica w Krakowie}}}

\vspace*{1mm}\rule{\textwidth}{1mm}\vspace*{1mm}

{\large \@facultyPL}}\\\vspace*{2mm}
{\large\textsc{\@departmentPL}}\vspace*{1cm}

\ifpdflatex\includegraphics[scale=0.7]{agh}
\else\includegraphics[scale=0.7]{agh}
\fi
\vspace*{1cm}

{\huge\scshape \@thesistypePL}\\\vspace*{2cm}

{\LARGE\scshape \@author}\\\vspace*{2cm}

{\LARGE{\bfseries\scshape \@titlePL}}\\\vspace*{3cm}

\begin{flushright}
\begin{minipage}[!h]{6cm} 
\large{\scshape Promotor:}\\ \@supervisorPL
\end{minipage}
\end{flushright}

\vfill{\Large Krak\'{o}w \@date}

\end{center}

%\clearpage 
\titlepage

%\vspace*{15cm} \vfill
\begin{flushright} 
\begin{minipage}[!h]{8cm}
\end{minipage}
\end{flushright}

%\clearpage

\setcounter{page}{2}

}

\def\thesisheaders{
\fancyfoot[L]{\small \@shortauthor\quad\textit{\@shorttitlePL}}
}

\ProcessOptions

\pagestyle{fancy}
\renewcommand{\chaptermark}[1]{\markboth{\thechapter.\ #1}{}}
\renewcommand{\sectionmark}[1]{\markright{\thesection.\ #1}}
\renewcommand{\headrulewidth}{0.5pt}
\renewcommand{\footrulewidth}{0.5pt}
\fancyhf{}
\fancyhead{}
%\fancyhead[L]{\slshape{\small \rightmark}}
%\fancyhead[R]{\bfseries \thepage}


\fancyhead[LE]{\bfseries \thepage}
\fancyhead[RO]{\bfseries \thepage}
\cfoot{\@titlePL}


%\thesisheaders

\frenchspacing
\sloppy 
\widowpenalty     9999 
\clubpenalty      9999 
\flushbottom

%---------------------------------------------------------------------------
% Ustawienia parametrów dla tytułów rozdziałów, podrozdziałów, itd.
%---------------------------------------------------------------------------


\titleformat{\chapter}[block]
{\bfseries\LARGE}{\filright \LARGE\thechapter. }{0ex}{}
%odstępy: lewy, góra, dół
\titlespacing{\chapter}{0pt}{7mm}{7mm}
\titleformat{\section}[block]
{\bfseries\Large}{\filright \Large\thesection. }{0ex}{}
\titlespacing{\section}{0mm}{8mm plus 0mm minus 1mm}{4mm plus 0mm minus 1mm}
\titleformat{\subsection}[block]
{\bfseries\large}{\filright \large\thesubsection. }{0ex}{}
\titlespacing{\subsection}{0mm}{6mm}{2.5mm}
\titleformat{\subsubsection}[block]
{\bfseries\normalsize}{\filright \normalsize\thesubsubsection. }{0ex}{}
\titlespacing{\subsubsection}{0mm}{3mm}{1.5mm}

%---------------------------------------------------------------------------
% Ustawienia parametrów generowania spisu treści i spisu rysunków
%---------------------------------------------------------------------------

\renewcommand{\cfttoctitlefont}{\bfseries\Large}
%\renewcommand{\cftbeforetoctitleskip}{20mm}
%\renewcommand{\cftaftertoctitleskip}{19mm}
\renewcommand{\cftchapleader}{\cftdotfill{\cftdot}}
\renewcommand{\cftsecleader}{\cftdotfill{\cftdot}}
\renewcommand{\cftsubsecleader}{\cftdotfill{\cftdot}}
\renewcommand{\cftchapaftersnum}{.}
\renewcommand{\cftsecaftersnum}{.}
\renewcommand{\cftsubsecaftersnum}{.}
\setlength{\cftparskip}{2pt}
\setlength{\cftbeforechapskip}{0mm}
\renewcommand{\cftchappagefont}{\normalsize}
