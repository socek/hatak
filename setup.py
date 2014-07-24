# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

install_requires = [
    'bael.project'
]

if __name__ == '__main__':
    setup(name='hatak',
          version='0.1',
          packages=find_packages('src'),
          package_dir={'': 'src'},
          install_requires=install_requires,
          namespace_packages=['bael'],
          include_package_data=True,
          zip_safe=False,
          package_data={
              '': ['.gitignore.tpl'],
          },
          entry_points="""\
              [console_scripts]
                  hatak = bael.hatak.recipe:run
          """,
          )
