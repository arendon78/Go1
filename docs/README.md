Documentation is done using sphinx

to generate documentation : 
go to the docs/ directory

type './clean_and_run.sh'

then you got to remove the line "source/index" in the index.rst file, and the source/index.rst file.
type make html

open it with firefox : 

type 'firefox _build/html/index.html' 

to add new documentation to your file, you need to have them in the src directory, and comment your code using the reStructuredText format

to ignore the generation of documentation of new files, add their path to the arguments in the third line of the .sh script