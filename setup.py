#!/usr/bin/env python
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pymongo==3.3.0',
    'lxml==3.4.2',
    'requests==2.11.1',
    'picles.plumber==0.10',
    'pyramid==1.5.4',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'waitress',
    'thriftpy==0.3.1',
    'thriftpywrap',
    'xylose==1.18.6',
    'raven'
    ]

test_requires = ['mocker']

setup(
    name="articlemeta",
    version='1.26.23',
    description="A SciELO API to load SciELO Articles metadata",
    author="SciELO",
    author_email="scielo-dev@googlegroups.com",
    license="BSD 2-clause",
    url="http://docs.scielo.org",
    keywords='scielo articlemeta',
    packages=find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Operating System :: POSIX :: Linux",
        "Topic :: System",
        "Topic :: Utilities",
    ],
    dependency_links=[
        "git+https://github.com/scieloorg/thriftpy-wrap@0.1.1#egg=thriftpywrap"
    ],
    include_package_data=True,
    zip_safe=False,
    setup_requires=["nose>=1.0", "coverage"],
    tests_require=test_requires,
    install_requires=requires,
    test_suite="nose.collector",
    entry_points="""\
    [paste.app_factory]
    main = articlemeta:main
    [console_scripts]
    articlemeta_loadmixedcitations=processing.load_mixedcitations:main
    articlemeta_loadbody=processing.load_body:main
    articlemeta_loadlanguages=processing.load_languages:main
    articlemeta_loadsections=processing.load_sections:main
    articlemeta_loadlicense=processing.load_licenses:main
    articlemeta_loaddoi=processing.load_doi:main
    articlemeta_importaffiliation=processing.importaffiliation:main
    articlemeta_fixpages=processing.fixpages:main
    articlemeta_dumparticles=processing.dumparticles:main
    articlemeta_thriftserver=articlemeta.thrift.server:main
    """,
)
