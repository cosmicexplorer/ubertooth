python_dist(
  name='wrapper-dist',
  sources=rglobs('*.py', exclude=['main.py']),
  dependencies=[':ubertooth-wrapper-lib'],
  compatibility=['CPython<3'],
)

python_binary(
  name='bin',
  source='main.py',
  dependencies=[':wrapper-dist'],
  platforms=['current'],
)

os_lib(
  name='libusb',
  include_dir='/usr/include/libusb-1.0',
  lib_dir='/usr/lib',
  lib_names=('usb',),
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
    ':libusb',
    ':ubertooth-precompiled',
    'libopenaptx',
  ],
)
