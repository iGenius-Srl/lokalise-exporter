from setuptools import setup

# https://packaging.python.org/tutorials/distributing-packages
setup(name='iGenius-lokalise-exporter',
      version='0.21',
      description='Export strings from lokalise.com',
      long_description='Utility tool to export localization strings from one or multiple lokalise.com projects at '
                       'once for iOS/Android/Frontend/Backend',
      url='https://github.com/iGenius-Srl/lokalise-exporter',
      author='iGenius',
      author_email='code@igenius.net',
      license='Apache-2.0',
      # https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.0',
          'Programming Language :: Python :: 3.1',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Software Development :: Internationalization',
          'Topic :: Software Development :: Localization'
      ],
      keywords='localization l10n internationalization i18n lokalise localise export exporter tools development',
      packages=['lokalise_exporter'],
      entry_points={
          # This has to be like this because of begins package for command line parsing
          'console_scripts': ['lokalise-exporter=lokalise_exporter.main:main.start'],
      },
      install_requires=['requests', 'begins', 'colorlog', 'xmltodict', 'future', 'chardet',
                        'backports.tempfile;python_version<"3.2"',
                        'scandir;python_version<"3.5"'],
      python_requires='>=2.7.9, <4',
      zip_safe=False)
