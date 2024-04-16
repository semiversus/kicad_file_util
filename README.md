# Sperry
Parse, generate and manipulate KiCAD files

## Goals
* [x] read any (KiCAD) s-expression based files (without fixed scheme)
* [x] write parsed data back as s-expression
* [ ] Methods to work with parsed s-expressions (create, read, update, delete)
* [ ] registration of python classes to handle specific s-expressions
* [ ] rules for line ending generation for writing s-expressions

### Notes
* Unknown expression should be abe to be read and manipulated
* Schema of files and expressions are stored in JSON files
* Python code with classes is generated from schema files
* Python classes can be inherited and extended
