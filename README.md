# ASCIIzer - Make beautiful ASCII arts from images 

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/919cc7fae9f149dda4405d955517665f)](https://www.codacy.com/project/KAMI911/asciizer/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=KAMI911/asciizer&amp;utm_campaign=Badge_Grade_Dashboard)[![Maintainability](https://api.codeclimate.com/v1/badges/11940f5ee97d6720b091/maintainability)](https://codeclimate.com/github/KAMI911/asciizer/maintainability)

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
