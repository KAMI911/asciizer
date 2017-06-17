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
DEFAULT_MAX_ONE_CHANNEL_INTENSITY = 255


class asciizer:
    def __init__(self, **kwargs):
        self.max_width = DEFAULT_IMAGE_MAX_SIZE
        self.reverse = False
        self.intensity_bar = DEFAULT_INTENSITY_SCALE
        for key, value in kwargs.items():
            if key == 'max_width': self.max_width = value
            if key == 'filename': self.orig_image = Image.open(value)
            if key == 'reverse': self.reverse = value
            if key == 'intensity': self.intensity_bar = value
        if self.reverse:
            self.intensity_bar = self.intensity_bar[::-1]
        else:
            self.intensity_bar = self.intensity_bar
        self.orig_img = self.orig_image.load()
        self.image_size = self.orig_image.size
        self.__calculate_pixel_ration()
        self.intensity_step = int(DEFAULT_MAX_INTENSITY / (len(self.intensity_bar) - 1))
        self.intensity_step_int = int(DEFAULT_MAX_ONE_CHANNEL_INTENSITY / (len(self.intensity_bar) - 1))

    def __calculate_pixel_ration(self):
        self.image_ratio = int(self.orig_image.width / self.max_width)

    def __intensity_calculator(self, one_pixel, intensity_diff):
        return (self.intensity_bar[int(sum(one_pixel) / intensity_diff)])

    def process(self):
        image_str = ""
        for y in range(0, self.orig_image.height - 1, self.image_ratio):
            for x in range(0, self.orig_image.width - 1, self.image_ratio):
                pixel = self.orig_img[x, y]
                if not isinstance(pixel, int):
                    image_str += self.__intensity_calculator(pixel, self.intensity_step)
                else:
                    image_str += self.intensity_bar[int((255 - pixel) / self.intensity_step_int)]
            image_str += "\n"
        return image_str

    def draw(self):
        print(self.process())

    def save(self, filename):
        with open(filename, "w") as f:
            f.write(self.process())

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
            ascii = asciizer(filename=cmd.input, max_width=cmd.width, intensity=DEFAULT_INTENSITY_SCALE,
                             reverse=cmd.reverse)
        except:
            print('Unable load ({0}) image!'.format(cmd.input))
            exit(1)
        ascii.draw()
    else:
        print('File is not exist! ({0})'.format(cmd.input))
        exit(1)
    if cmd.output is not None:
        try:
            ascii.save(cmd.output)
        except:
            print('Unable save text file! {0}'.format(cmd.output))
        finally:
            ascii.close()
    else:
        ascii.close()
