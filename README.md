# ASCIIzer - Make beautiful ASCII arts from images 

This program creates ASCII art from your image. You can show the ASCII art or save it directly to file. Also you can specify the character width of the picture.

## Usage of ASCIIzer

usage: asciizer [-h] -i INPUT [-o OUTPUT] [-w WIDTH] [-r]

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

### Example of ASCIIzer usage

Open happy.jpg picture and display the ASCII art

    asciizer.py -i happy.jpg

Open happy.jpg picture and save the ASCII art as happy.txt

    asciizer.py -i happy.jpg -o happy.txt
