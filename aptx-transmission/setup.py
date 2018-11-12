# coding=utf-8

from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

from setuptools import setup, find_packages


setup(
  name='aptx_transmission',
  version='0.0.1',
  packages=find_packages(),
  # Declare one shared lib at the top-level directory (denoted by '').
  data_files=[('', ['libubertooth-wrapper.so'])],
)
