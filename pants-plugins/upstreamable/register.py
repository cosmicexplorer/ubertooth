# coding=utf-8

from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

import os

from pants.backend.native.config.environment import GCCCToolchain, GCCCppToolchain, Platform
from pants.backend.native.targets.native_library import NativeLibrary
from pants.backend.native.tasks.c_compile import CCompile
from pants.backend.native.tasks.cpp_compile import CppCompile
from pants.backend.native.tasks.link_shared_libraries import LinkSharedLibraries
from pants.backend.native.tasks.native_external_library_fetch import NativeExternalLibraryFetch, NativeExternalLibraryFiles
from pants.backend.python.tasks.python_run import PythonRun
from pants.base.build_environment import get_buildroot
from pants.build_graph.build_file_aliases import BuildFileAliases
from pants.build_graph.target import Target
from pants.goal.goal import Goal
from pants.goal.products import UnionProducts
from pants.goal.task_registrar import TaskRegistrar as task
from pants.task.task import Task
from pants.util.contextutil import environment_as
from pants.util.memo import memoized_property
from pants.util.objects import SubclassesOf


class OsLibTarget(Target):

  @memoized_property
  def files(self):
    return NativeExternalLibraryFiles(
      include_dir=os.path.join(get_buildroot(), self._include_dir),
      lib_dir=os.path.join(get_buildroot(), self._lib_dir),
      lib_names=tuple(self._lib_names or []),
    )

  def __init__(self, include_dir=None, lib_dir=None, lib_names=None, **kw):
    self._include_dir = include_dir
    self._lib_dir = lib_dir
    self._lib_names = lib_names
    super(OsLibTarget, self).__init__(**kw)


class CCompileHack(CCompile):

  dependent_target_constraint = SubclassesOf(NativeLibrary, OsLibTarget)

  def get_compiler(self):
    return self._request_single(GCCCToolchain, self._native_toolchain).c_toolchain.c_compiler


class CppCompileHack(CppCompile):

  dependent_target_constraint = SubclassesOf(NativeLibrary, OsLibTarget)

  def get_compiler(self):
    return self._request_single(GCCCppToolchain, self._native_toolchain).cpp_toolchain.cpp_compiler


class LinkSharedLibsHack(LinkSharedLibraries):

  dependent_target_constraint = SubclassesOf(NativeLibrary, OsLibTarget)

  @memoized_property
  def _cpp_toolchain(self):
    return self._request_single(GCCCppToolchain, self._native_toolchain).cpp_toolchain

  @memoized_property
  def linker(self):
    return self._cpp_toolchain.cpp_linker


class LibusbExternLibHack(Task):

  @classmethod
  def product_types(cls):
    return [NativeExternalLibraryFiles]

  def execute(self):
    files_prod = UnionProducts()
    for tgt in self.context.targets(lambda t: isinstance(t, OsLibTarget)):
      files_prod.add_for_target(tgt, [tgt.files])
    self.context.products.register_data(NativeExternalLibraryFiles, files_prod)


class PythonRunExternLibHack(PythonRun):
  """A wrapper around PythonRun which sets some hardcoded shared lib paths."""

  def execute(self):
    loader_env_var_for_plat = Platform.create().resolve_platform_specific({
      'darwin': lambda: 'DYLD_LIBRARY_PATH',
      'linux': lambda: 'LD_LIBRARY_PATH',
    })
    shared_lib_path = os.path.join(get_buildroot(), 'host/libubertooth/src')
    with environment_as(**{loader_env_var_for_plat: shared_lib_path}):
      super(PythonRunExternLibHack, self).execute()


def build_file_aliases():
  return BuildFileAliases(
    targets={
      'os_lib': OsLibTarget,
    },
  )


def register_goals():
  Goal.by_name('native-compile').uninstall_task('native-third-party-fetch')
  Goal.by_name('native-compile').uninstall_task('c-for-ctypes')
  Goal.by_name('native-compile').uninstall_task('cpp-for-ctypes')
  Goal.by_name('link').uninstall_task('shared-libraries')

  task(name='register-libusb', action=LibusbExternLibHack).install('libusb-hack')
  task(name='c-hack-for-ctypes', action=CCompileHack).install('native-compile')
  task(name='cpp-hack-for-ctypes', action=CppCompileHack).install('native-compile')
  task(name='shared-libs-libusb', action=LinkSharedLibsHack).install('link')

  task(name='hack-rt-libs-py-run', action=PythonRunExternLibHack).install('run-hack')
