try:
    from PIL import Image
    import argparse
    import textwrap
    import os
except ImportError as err:
    print('Error {0} import module: {1}'.format(__name__, err))
    exit(128)

DEFAULT_IMAGE_MAX_SIZE = 100
DEFAULT_INTENSITY_SCALE = " .:-=+*#%@"
DEFAULT_MAX_INTENSITY = 3 * 255


class asciizer:
    def __init__(self, filename, max_with=DEFAULT_IMAGE_MAX_SIZE, intensity=DEFAULT_INTENSITY_SCALE, reverse=False):
        self.max_with = max_with
        self.orig_image = Image.open(filename)
        self.orig_img = self.orig_image.load()
        self.image_size = self.orig_image.size
        self.__calculate_pixel_ration()
        self.reverse = reverse

        if not self.reverse:
            self.intensity_bar = intensity
        else:
            self.intensity_bar = intensity[::-1]
        self.intensity_step = DEFAULT_MAX_INTENSITY / (len(intensity) - 1)

    def __calculate_pixel_ration(self):
        self.image_ratio = int(self.orig_image.width / self.max_with)

    def __intensity_calculator(self):
        image_str = ""
        for y in range(0, self.orig_image.height - 1, self.image_ratio):
            for x in range(0, self.orig_image.width - 1, self.image_ratio):
                pixel = (self.orig_img[x, y])
                image_str += (self.intensity_bar[int(sum(pixel) / self.intensity_step)])
            image_str += "\n"
        return image_str

    def draw(self):
        print(self.__intensity_calculator())

    def save(self, filename):
        with open(filename, "w") as f:
            f.write(self.__intensity_calculator())

    def close(self):
        self.orig_image.close()


class asciizer_commandline:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="asciizer",
                                              formatter_class=argparse.RawTextHelpFormatter,
                                              description='',
                                              epilog=textwrap.dedent('''
        example:
          asciizer.py -i happy.jpg  '''))

        self.parser.add_argument('-i', type=str, dest='input', required=True,
                                 help='required:  input file (with or witout path)')

        self.parser.add_argument('-o', type=str, dest='output', required=False,
                                 help='optional:  output file (with or witout path)')

        self.parser.add_argument('-w', type=int, dest='width', required=False,
                                 help='optional:  ASCII with (in characters) [default: {0}]'.format(
                                     DEFAULT_IMAGE_MAX_SIZE))

        self.parser.add_argument('-r', dest='reverse', required=False,
                                 help='optional:  Use reverse intensity bar', action='store_true')

    def parse(self):
        self.args = self.parser.parse_args()

    @property
    def input(self):
        return self.args.input

    @property
    def output(self):
        return self.args.output

    @property
    def width(self):
        return DEFAULT_IMAGE_MAX_SIZE if self.args.width is None else self.args.width

    @property
    def reverse(self):
        return self.args.reverse


if __name__ == "__main__":
    cmd = asciizer_commandline()
    cmd.parse()
    if os.path.isfile(cmd.input):
        try:
            ascii = asciizer(cmd.input, cmd.width, DEFAULT_INTENSITY_SCALE, cmd.reverse)
        except:
            print('Unable load image!')
            exit(1)
        ascii.draw()
    else:
        print('File is not exist! ({0})'.format(cmd.input))
        exit (1)
    if cmd.output is not None:
        try:
            ascii.save(cmd.output)
        except:
            print('Unable save text file! {0}'.format(cmd.output))
        finally:
            ascii.close()
    else:
        ascii.close()
