# ASCIIzer - Make beautiful ASCII arts from images 

This program creates ASCII art from your image. You can show the ASCII art or save it directly to file. Also you can specify the character width of the picture.

## Usage of ASCIIzer

usage: asciizer [-h] -i INPUT [-o OUTPUT] [-w WIDTH] [-r]

optional arguments:

  -h, --help  show this help message and exit

  -i INPUT    required:  input file (with or witout path)

  -o OUTPUT   optional:  output file (with or witout path)

  -w WIDTH    optional:  ASCII with (in characters) [default: 100]

  -r          optional:  Use reverse intensity bar

example:

  asciizer.py -i happy.jpg
