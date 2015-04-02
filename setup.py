#!/usr/bin/env python
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'uuid==1.30',
    'pymongo==2.5.2',
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'waitress',
    'gunicorn'
    ]

test_requires = requires+['mocker']

setup(
    name="articlemeta",
    version='0.2.5',
    description="A SciELO API to load SciELO Articles metadata",
    author="SciELO",
    author_email="scielo-dev@googlegroups.com",
    license="BSD 2-clause",
    url="http://docs.scielo.org",
    keywords='scielo articlemeta',
    packages=['articlemeta'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Operating System :: POSIX :: Linux",
        "Topic :: System",
        "Topic :: Utilities",
    ],
    setup_requires=["nose>=1.0", "coverage"],
    tests_require=test_requires,
    test_suite="nose.collector",
    entry_points="""\
    [paste.app_factory]
    main = articlemeta:main
    [console_scripts]
    articlemeta_loadlanguages=processing.load_languages:main
    articlemeta_importaffiliation=processing.importaffiliation:main
    articlemeta_dumparticles=processing.dumparticles:main
    """,
)