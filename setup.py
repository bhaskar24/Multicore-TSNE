import sys
import shutil
import os
from os import path
from glob import glob

from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools import setup, find_packages
from distutils.spawn import find_executable


PACKAGE_NAME = "MulticoreTSNE"

VERSION = '0.1'

SETUP_REQUIRES = ['cmake'] if not find_executable('cmake') else []


class _LibBuilderMixin(object):
    def run(self):
        CWD = path.dirname(__file__)
        BUILD_DIR = path.join(CWD, 'multicore_tsne', 'release')
        try:
            os.makedirs(BUILD_DIR)
        except OSError:
            pass

        os.chdir(BUILD_DIR)

        if 0 != os.system('cmake -DCMAKE_BUILD_TYPE=RELEASE ..'):
            sys.exit('Cannot find cmake. Install cmake.')
        if 0 != os.system('make -j4' + ' VERBOSE=1' * int(self.verbose)):
            sys.exit('Cannot find make. Install make.')

        sofile = (glob('lib*.so') + glob('lib*.dll'))[0]
        shutil.copy(sofile, path.join('..', '..', PACKAGE_NAME))

        os.chdir(CWD)
        super(_LibBuilderMixin, self).run()


class Install(_LibBuilderMixin, install):
    pass


class Develop(_LibBuilderMixin, develop):
    pass


def _discover_tests():
    import unittest
    return unittest.defaultTestLoader.discover('MulticoreTSNE',
                                               pattern='test_*.py',
                                               top_level_dir='.')


if __name__ == '__main__':
    setup(
        name=PACKAGE_NAME,
        version=VERSION,
        description='Multicore version of t-SNE algorithm.',
        author="Dmitry Ulyanov (based on L. Van der Maaten's code)",
        author_email='dmitry.ulyanov.msu@gmail.com',
        url='https://github.com/DmitryUlyanov/Multicore-TSNE',
        setup_requires=SETUP_REQUIRES,
        install_requires=[
            'numpy',
            'psutil',
            'cffi'
        ],
        packages=find_packages(),
        include_package_data=True,

        cmdclass={
            'install': Install,
            'develop': Develop,
        },

        test_suite='setup._discover_tests',
        tests_require=[
            'scikit-learn',
        ]
    )
