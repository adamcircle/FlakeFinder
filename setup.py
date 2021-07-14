from setuptools import setup

setup(
    name='FlakeFinder',
    version='1.0',
    packages=['weather', 'weather.migrations', 'scraping',
              'scraping.migrations', 'FlakeFinder'],
    url='www.flakefinder.com',
    license='GPLv3',
    author='Adam Circle',
    author_email='',
    description='Worldwide snowflake shape forecasts'
)
