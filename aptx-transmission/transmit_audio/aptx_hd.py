# coding=utf-8

from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

import ctypes
import os


def get_generated_shared_lib(lib_name):
  # These are the same filenames as in setup.py.
  filename = 'lib{}.so'.format(lib_name)
  # The data files are in the root directory, but we are in ctypes_python_pkg/.
  rel_path = os.path.join(os.path.dirname(__file__), '..', filename)
  return os.path.normpath(rel_path)


ubertooth_wrapper_lib_path = get_generated_shared_lib('ubertooth-wrapper')
ubertooth_wrapper_lib = ctypes.CDLL(ubertooth_wrapper_lib_path)
