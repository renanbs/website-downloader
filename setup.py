from setuptools import setup, find_packages


setup(name='website-downloader',
      description='A simple website downloader',
      long_description='A simple website downloader',
      packages=find_packages(exclude=["*tests*"]),
      package_data={'': ['*.yaml']},
      version='1.0.0',
      install_requires=[
          'beautifulsoup4>=4.9.1',
          'requests>=2.23.0'
      ],
      extras_require={
          'dev': [
              'pycodestyle>=2.6.0',
              'pytest>=5.4.3',
              'pytest-cov>=2.10.0',
              'requests-mock>=1.8.0',
              'pytest-mock>=3.1.1',
              'pytest-lazy-fixture>=0.6.3',
          ],
      }
      )
