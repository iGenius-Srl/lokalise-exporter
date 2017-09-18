from setuptools import setup

setup(name='lokalise-exporter',
      version='0.4',
      description='Export strings from lokalise.co',
      long_description='Utility tool to export localization strings from lokalise.co for iOS/Android/Frontend/Backend',
      url='https://github.com/gotev/lokalise-exporter',
      author='Aleksandar Gotev',
      author_email='alexgotev@gmail.com',
      license='Apache-2.0',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
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
      install_requires=['requests', 'begins', 'colorlog'],
      python_requires='>=3',
      zip_safe=False)
