import os
import sys
from setuptools import (
    setup,
    find_packages
)

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (2, 7)

# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================

This version of django-queryset-signals requires Python {}.{}, but you are
trying to install it on Python {}.{}.

This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have pip >= 9.0 and setuptools >= 24.2, then try again:
    $ python -m pip install --upgrade pip setuptools
    $ python -m pip install django-queryset-signals
This will install the latest version of django-queryset-signals which works on
your version of Python.""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

setup(
    name='django-queryset-signals',
    version='0.1.0',
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    url='https://github.com/magenta-aps/django-queryset-signals',
    author='Emil Madsen (Originally Martin P. Hellwig)',
    author_email='emil@magenta.dk',
    description=('A library that will send signals on queryset data '
                 'manipulation methods.'),
    long_description=read('README.rst'),
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    download_url='https://github.com/magenta-aps/django-queryset-signals/archive/master.zip',
    zip_safe=False,
    install_requires=['Django'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=[
        'django',
    ],
    project_urls={
        'Upstream': 'https://bitbucket.org/hellwig/django-query-signals',
        'Source': 'https://github.com/magenta-aps/django-queryset-signals',
        # TODO: Add documentation URL
    },
)
