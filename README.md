# ASCIIzer - Make beautiful ASCII arts from images 

This program creates ASCII art from your image. You can show the ASCII art or save it directly to file. Also you can specify the character width of the picture.

## Usage of ASCIIzer

usage: asciizer [-h] -i INPUT [-o OUTPUT] [-w WIDTH] [-r]

optional arguments:

optional arguments:

  -h, --help
    show this help message and exit
  -i INPUT, --input INPUT
    required:  input file (with or witout path)
  -o OUTPUT, --output OUTPUT
    optional:  output file (with or witout path)
  -w WIDTH, --width WIDTH
    optional:  ASCII with (in characters) [default: 100]
  -r, --reverse
    optional:  Use reverse intensity bar
  -s, --show
    optional:  show image when file is saved

example:

  asciizer.py -i happy.jpg
