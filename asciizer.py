#!/usr/bin/python
try:
    from PIL import Image
    import argparse, textwrap, os, sys, atexit, logging, logging.config
except ImportError as err:
    print('Error {0} import module: {1}'.format(__name__, err))
    exit(128)

__program__ = 'ASCIIzer'
__version__ = '0.1.4'

DEFAULT_IMAGE_MAX_SIZE = 100
DEFAULT_INTENSITY_SCALE = " .:-=+*#%@"
DEFAULT_MAX_INTENSITY = 3 * 255
DEFAULT_MAX_ONE_CHANNEL_INTENSITY = 255


def init_log():
    logging.config.fileConfig('log.conf')


def on_exit():
    if 'converter' in globals():
        if converter.is_input_file_opened:
            logging.info('Closing opened input file.')
            converter.close()
    logging.info('Finished, exiting and go home ...')


def exception_hook(exc_type, exc_value, exc_traceback):
    if 'converter' in globals():
        if converter.is_input_file_opened:
            converter.close()
    logging.fatal("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    exit(-1)


sys.excepthook = exception_hook
atexit.register(on_exit)


class asciizer:
    def __init__(self, **kwargs):
        self.input_file_opened = False
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
        if self.orig_image is None:
            raise IOerror('Unable load ({0}) input image!'.format(cmd.input))
        else:
            self.input_file_opened = True
        self.orig_img = self.orig_image.load()
        self.image_size = self.orig_image.size
        self.__calculate_pixel_ration()
        self.intensity_step = int(DEFAULT_MAX_INTENSITY / (len(self.intensity_bar) - 1))
        self.intensity_one_channel_step = int(DEFAULT_MAX_ONE_CHANNEL_INTENSITY / (len(self.intensity_bar) - 1))

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
                    image_str += self.intensity_bar[int((255 - pixel) / self.intensity_one_channel_step)]
            image_str += "\n"
        return image_str

    def draw(self):
        print(self.process())

    def save(self, filename):
        try:
            with open(filename, "w") as f:
                f.write(self.process())
        except Exception as e:
            raise IOError('Unable save text file! {0} Error: {1}'.format(cmd.output, e))

    def close(self):
        self.orig_image.close()
        self.input_file_opened = False

    @property
    def is_input_file_opened(self):
        return self.input_file_opened


class asciizer_commandline:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="asciizer",
                                              formatter_class=argparse.RawTextHelpFormatter,
                                              description='',
                                              epilog=textwrap.dedent('''
        example:
          asciizer.py -i happy.jpg  '''))

        self.parser.add_argument('-i', '--input', type=str, dest='input', required=True,
                                 help='required:  input file (with or witout path)')

        self.parser.add_argument('-o', '--output', type=str, dest='output', required=False,
                                 help='optional:  output file (with or witout path)')

        self.parser.add_argument('-w', '--width', type=int, dest='width', required=False,
                                 help='optional:  ASCII with (in characters) [default: {0}]'.format(
                                     DEFAULT_IMAGE_MAX_SIZE))

        self.parser.add_argument('-r', '--reverse', dest='reverse', required=False,
                                 help='optional:  Use reverse intensity bar', action='store_true')

        self.parser.add_argument('-s', '--show', dest='show', required=False,
                                 help='optional:  show image when file is saved', action='store_true')

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

    @property
    def show(self):
        return self.args.show


if __name__ == "__main__":
    try:
        init_log()
        logging.info('Starting {0} ...'.format(__program__))
        logging.info('Reading command line parameters ...'.format(__program__))
        cmd = asciizer_commandline()
        logging.info('Parsing command line parameters ...'.format(__program__))
        cmd.parse()
        if os.path.isfile(cmd.input):
            logging.info('Processing image ...'.format(__program__))
            converter = asciizer(filename=cmd.input, max_width=cmd.width, intensity=DEFAULT_INTENSITY_SCALE,
                                 reverse=cmd.reverse)
        else:
            raise IOError('Input file is not exist! ({0})'.format(cmd.input))
        if cmd.show == True or cmd.output is None:
            converter.draw()
        if cmd.output is not None:
            logging.info('Saving image to {0} text file ...'.format(cmd.output))
            converter.save(cmd.output)
    except KeyboardInterrupt as e:
        logging.fatal('Processing is interrupted by the user.')
    except IOError as e:
        logging.error('File error: {0}'.format(e))
    except Exception as e:
        logging.error(e, exc_info=True)
