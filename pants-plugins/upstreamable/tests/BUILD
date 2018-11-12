pants_requirement(name='pants-base')

python_requirement_library(
  name='pants',
  requirements=[
    python_requirement('pantsbuild.pants.testinfra==1.11.0rc1'),
  ],
  dependencies=[':pants-base'],
)

python_tests(
  dependencies=[':pants'],
  compatibility=['CPython<3'],
)
