#!/usr/bin/env python
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'uuid>=1.30',
    'pymongo>=2.5.2',
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'waitress',
    'gunicorn',
    'thriftpy',
    'thriftpywrap',
    'xylose'
    ]

test_requires = ['mocker']

setup(
    name="articlemeta",
    version='0.2.45',
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
    dependency_links=[
        "git+https://github.com/scieloorg/thriftpy-wrap@0.1.1#egg=thriftpywrap",
        "git+https://github.com/scieloorg/xylose@0.35#egg=xylose"
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
    articlemeta_loadbody=processing.load_body:main
    articlemeta_loadlanguages=processing.load_languages:main
    articlemeta_loadsections=processing.load_sections:main
    articlemeta_loadlicenses=processing.load_licenses:main
    articlemeta_loaddoi=processing.load_doi:main
    articlemeta_importaffiliation=processing.importaffiliation:main
    articlemeta_dumparticles=processing.dumparticles:main
    articlemeta_thrift_server=articlemeta.thrift.server:main
    """,
)
