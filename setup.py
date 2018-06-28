#!/usr/bin/env python

import os
import pathlib

from distutils.core import setup, Extension
from distutils.command.build_ext import build_ext as build_ext_orig

class CMakeExtension(Extension):

    def __init__(self, name, source_dir = ''):
        super().__init__(name, sources=[])
        self.source_dir = os.path.abspath(source_dir)


class build_ext(build_ext_orig):

    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)
        super().run()

    def build_cmake(self, ext):
        cwd = pathlib.Path().absolute()

        build_temp = pathlib.Path(self.build_temp)
        build_temp.mkdir(parents=True, exist_ok=True)
        extdir = pathlib.Path(self.get_ext_fullpath(ext.name))
        extdir.mkdir(parents=True, exist_ok=True)

        config = 'Debug' if self.debug else 'Release'
        cmake_args = [
            '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + str(extdir.parent.absolute()),
            '-DCMAKE_BUILD_TYPE=' + config
        ]

        build_args = ['--config', config, '--', '-j4']

        os.chdir(str(build_temp))
        self.spawn(['cmake', ext.source_dir] + cmake_args)
        if not self.dry_run:
            self.spawn(['cmake', '--build', '.'] + build_args)
        os.chdir(str(cwd))


setup(name = 'spam',
      version = '0.0.1',
      description = 'Sample Package',
      packages = [],
      ext_modules = [CMakeExtension('cpp', 'src')],
      cmdclass = {
          'build_ext': build_ext,
      })
