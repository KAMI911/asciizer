try:
    import filecmp
    import os
    import unittest
    import asciizer
except ImportError as err:
    print('Error {0} import module: {1}'.format(__name__, err))
    exit(128)


def input_file_path(filename):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'test', 'input', filename))


def compare_file_path(filename):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'test', 'compare', filename))


def temp_file_path(filename):
    temp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test', 'tmp'))
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    return os.path.join(temp_dir, filename)


class TestCalculations(unittest.TestCase):
    def test_image_pixel_ratio_original_value(self):
        self.t = asciizer.asciizer(filename=input_file_path('Tux.png'))
        self.assertEqual(self.t.image_ratio, 2)

    def test_image_pixel_ratio_medium_value(self):
        self.t = asciizer.asciizer(filename=input_file_path('Tux.png'), max_width=40)
        self.assertEqual(self.t.image_ratio, 6)

    def test_image_pixel_ratio_small_value(self):
        self.t = asciizer.asciizer(filename=input_file_path('Tux.png'), max_width=10)
        self.assertEqual(self.t.image_ratio, 26)

class TestIntensityBar(unittest.TestCase):
    def test_image_load_intensity_bar(self):
        self.t = asciizer.asciizer(filename=input_file_path('Tux.png'))
        self.assertEqual(self.t.intensity_bar, ' .:-=+*#%@')

    def test_image_load_intensity_bar_reverse(self):
        self.t = asciizer.asciizer(filename=input_file_path('Tux.png'), reverse=True)
        self.assertEqual(self.t.intensity_bar, '@%#*+=-:. ')

    def test_image_load_intensity_step_value(self):
        self.t = asciizer.asciizer(filename=input_file_path('Tux.png'))
        self.assertEqual(self.t.intensity_step, 85)

    def test_image_load_intensity_step_int_value(self):
        self.t = asciizer.asciizer(filename=input_file_path('Tux.png'))
        self.assertEqual(self.t.intensity_step_int, 28)

    def test_image_load_custom_intensity_bar(self):
        self.t = asciizer.asciizer(filename=input_file_path('Tux.png'), intensity='TESZ')
        self.assertEqual(self.t.intensity_bar, 'TESZ')

class TestSaveImage(unittest.TestCase):
    def test_image_save_jpg(self):
        self.temp_file = temp_file_path('Tux100.txt')
        self.compare_file = compare_file_path('Tux100.txt')
        self.t = asciizer.asciizer(filename=input_file_path('Tux.jpg'))
        self.t.save(self.temp_file)
        self.assertTrue(filecmp.cmp(self.compare_file, self.temp_file))
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def test_image_save_transparent_png(self):
        self.temp_file = temp_file_path('Tux100t.txt')
        self.compare_file = compare_file_path('Tux100t.txt')
        self.t = asciizer.asciizer(filename=input_file_path('Tux.png'))
        self.t.save(self.temp_file)
        self.assertTrue(filecmp.cmp(self.compare_file, self.temp_file))
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def test_image_save_jpg_reverse(self):
        self.temp_file = temp_file_path('Tux100r.txt')
        self.compare_file = compare_file_path('Tux100r.txt')
        self.t = asciizer.asciizer(filename=input_file_path('Tux.jpg'), reverse=True)
        self.t.save(self.temp_file)
        self.assertTrue(filecmp.cmp(self.compare_file, self.temp_file))
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def test_image_save_transparent_png_reverse(self):
        self.temp_file = temp_file_path('Tux100tr.txt')
        self.compare_file = compare_file_path('Tux100tr.txt')
        self.t = asciizer.asciizer(filename=input_file_path('Tux.png'), reverse=True)
        self.t.save(self.temp_file)
        self.assertTrue(filecmp.cmp(self.compare_file, self.temp_file))
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)


def testing_asciizer():
    calculate = unittest.TestLoader().loadTestsFromTestCase(TestCalculations)
    intensity_bar = unittest.TestLoader().loadTestsFromTestCase(TestIntensityBar)
    save_image = unittest.TestLoader().loadTestsFromTestCase(TestSaveImage)
    suite = unittest.TestSuite([calculate, intensity_bar, save_image])
    return unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    testing_asciizer()
