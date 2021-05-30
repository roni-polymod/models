Dependencies
------------

svgwrite - install instructions at https://pypi.org/project/svgwrite/

the svgwrite module is only referenced in one function, write_svg_file in write_model_file.py so if you have a better
svg writing module it can be easily substituted.

Usage
-----

$ python write_model_file.py [-h] [-n FILENAME] [-a] [-f] [-e] poly stkey

Write SVG file for polyhedron face or edge models

positional arguments:

  poly                  polyhedron name

  stkey                 dict key to size, type and repeat parameters

optional arguments:

  -h, --help            show this help message and exit

  -n FILENAME, --filename FILENAME            relative path and file name to save, (defaults to polyhedron name.svg in current folder)

  -a, --array           True for array repetition of pieces, default to single piece

  -f, --face            Face model (default)

  -e, --edge            Edge model (no effect if -f also used)


Examples
--------

$ python write_model_file.py cube 5e

will create a single face for a cube with 50mm edge (5e size and type key parameter). The file will be saved as cube.svg in the working directory.


$ python write_model_file.py cube 5r -n files/edges.svg -ae

will create an array (-a option) of edge struts (-e option) for a cube with 50mm circumradius (5r size/type key parameter).
The file will be saved as edges.svg in the files subdirectory directory.

The polyhedron name, 'cube' in the above examples, the size/type key and the array repetitions are set in the polyhedrondict
dictionary in param_dictionaries.py. Full code details are at http://polyhedronmodels.org/

The SVG subfolder contains precreated SVG files and parts key pdf documents for the main model sets. Details and assembly
instructions also at the above url.

Copyright
---------

None, use as you wish but please do share anything interesting.

