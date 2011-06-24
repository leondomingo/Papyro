# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='paPyro',
      version='1.0.5',
      author='León Domingo',
      author_email='leon.domingo@ender.es',
      description=('A PDF report generator written in Python'),
      #license=???,
      keywords='pdf reports ender',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Utilities',
      ],
      url='http://www.ender.es',      
      packages=['papyro',
                'papyro.ttfonts'],
      package_data={
        'papyro.ttfonts': ['*.ttf'],
      },
      install_requires=[
        'Neptuno2',
        'ReportLab>=2.5',
        'SQLAlchemy==0.6.7',
        'lxml==2.2.7',
      ],
     )
