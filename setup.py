#! /usr/bin/env python
"""Pypp package setuptools installer."""

import setuptools


name = 'cpypp'
repo_slug = 'wellrats/{}'.format(name.lower())
repo_url = 'https://github.com/{}'.format(repo_slug)

with open("README.rst", "r") as fh:
    long_description = fh.read()


params = dict(
    name=name,
    version="1.0.2",
    description='c-style preprocessor for Python',
    long_description=long_description, 
    lond_description_content_type="text/x-rst",
    author='Wellington Rats',
    author_email='wellrats@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: Freely Distributable',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.3',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development', 
        'Topic :: Software Development :: Build Tools', 
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Compilers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    url=repo_url,
    project_urls={
        'GitHub: issues': '{}/issues'.format(repo_url),
        'GitHub: repo': repo_url,
    },
    packages= setuptools.find_packages()
    ,
    scripts=["cpypp2", "cpypp3" ],
    entry_points={'console_scripts': ['cpypp = cpypp.__main__:run']},
    package_data={
       'cpypp.tests': ['*.txt'] 
    },
    install_requires=[
    ],
    extras_require={
        'docs': [ ],
        'testing': [ ]
    },
    setup_requires=[
        # 'setuptools_scm',
    ]
)


__name__ == '__main__' and setuptools.setup(**params)
