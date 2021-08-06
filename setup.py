try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as f:
    README = f.read()

VERSION = '0.1.0'

setup(
    name = 'propublica-nonprofit',
    version = VERSION,
    description = 'A Python client for the ProPublica NonProfit Explorer API.',
    long_description = README,
    url = 'https://github.com/amoffatt/propublica-nonprofit',
    author = 'Rob Remington, Aaron Moffatt',
    author_email = 'contact@aaronmoffatt.com',
    license = 'MIT',
    py_modules = ['nonprofit'],
    install_requires = ['httplib2'],
    platforms = ['any'],
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    test_suite='test',
)
