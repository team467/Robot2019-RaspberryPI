from distutils.core import setup, Extension
from distutils.command.build_ext import build_ext


# Found this on stack overflow:
# https://stackoverflow.com/questions/4529555/building-a-ctypes-based-c-library-with-distutils
# noinspection PyPep8Naming
class build_ext(build_ext, object):

    def build_extension(self, ext):
        # noinspection PyAttributeOutsideInit
        self._ctypes = isinstance(ext, CTypesExtension)
        return super(build_ext,self).build_extension(ext)

    def get_export_symbols(self, ext):
        if self._ctypes:
            return ext.export_symbols
        return super(build_ext,self).get_export_symbols(ext)

    def get_ext_filename(self, ext_name):
        if self._ctypes:
            return ext_name + '.so'
        return super(build_ext,self).get_ext_filename(ext_name)


class CTypesExtension(Extension):
    pass


extension = CTypesExtension(
    'vl53l0x_python',
    define_macros=[],
    include_dirs=['.', 'Api/core/inc', 'platform/inc'],
    libraries=[],
    library_dirs=[],
    sources=['Api/core/src/vl53l0x_api_calibration.c',
             'Api/core/src/vl53l0x_api_core.c',
             'Api/core/src/vl53l0x_api_ranging.c',
             'Api/core/src/vl53l0x_api_strings.c',
             'Api/core/src/vl53l0x_api.c',
             'platform/src/vl53l0x_platform.c',
             'python_lib/vl53l0x_python.c'])

setup(name='VL53L0X_rasp_python',
      version='1.0.2',
      description='VL53L0X sensor for raspberry PI/JetsonTX2',
      # author='?',
      # author_email='?',
      url='https://github.com/naisy/VL53L0X_rasp_python',
      long_description='''
VL53L0X sensor for raspberry PI/JetsonTX2.
''',
      ext_modules=[extension],
      package_dir={'': 'python'},
      py_modules=['VL53L0X'],
      requires=['smbus' or 'smbus2'],
      cmdclass={'build_ext': build_ext})
