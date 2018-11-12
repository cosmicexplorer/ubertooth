python_dist(
  name='wrapper-dist',
  sources=rglobs('*.py', exclude=['main.py']),
  dependencies=[':ubertooth-wrapper-lib'],
)

python_binary(
  name='bin',
  source='main.py',
  dependencies=[':wrapper-dist'],
  platforms=['current'],
)

ubertooth_lib_loc = 'host/libubertooth/src'

os_lib(
  name='ubertooth-precompiled',
  include_dir=ubertooth_lib_loc,
  lib_dir=ubertooth_lib_loc,
  lib_names=('ubertooth',),
)

ctypes_compatible_cpp_library(
  name='ubertooth-wrapper-lib',
  ctypes_native_library=native_artifact(lib_name='ubertooth-wrapper'),
  dependencies=[
    # 'host/libubertooth/src',
    ':ubertooth-precompiled',
    'libopenaptx',
  ],
)
