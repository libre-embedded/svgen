<!--
    =====================================
    generator=datazen
    version=3.2.1
    hash=9c8763b9bdf3c645e4945f0d19c5f118
    =====================================
-->

# svgen ([0.8.0](https://pypi.org/project/svgen/))

[![python](https://img.shields.io/pypi/pyversions/svgen.svg)](https://pypi.org/project/svgen/)
![Build Status](https://github.com/libre-embedded/svgen/workflows/Python%20Package/badge.svg)
[![codecov](https://codecov.io/gh/libre-embedded/svgen/branch/master/graphs/badge.svg?branch=master)](https://codecov.io/github/libre-embedded/svgen)
![PyPI - Status](https://img.shields.io/pypi/status/svgen)
![Dependents (via libraries.io)](https://img.shields.io/librariesio/dependents/pypi/svgen)

*A tool for working with scalable vector graphics.*

Consider [sponsoring development](https://github.com/sponsors/libre-embedded).

([interface documentation](https://libre-embedded.github.io/python/svgen))

## Python Version Support

This package is tested with the following Python minor versions:

* [`python3.12`](https://docs.python.org/3.12/)
* [`python3.13`](https://docs.python.org/3.13/)

## Platform Support

This package is tested on the following platforms:

* `ubuntu-latest`
* `macos-latest`
* `windows-latest`

# Introduction

This utility provides a means to work on graphics with a programmatic workflow.

# Command-line Options

```
$ ./venv3.12/bin/svgen -h

usage: svgen [-h] [--version] [-v] [-q] [--curses] [--no-uvloop] [-C DIR]
             [-c CONFIG] [--height HEIGHT] [--width WIDTH] [--images]
             [-o OUTPUT]
             [scripts ...]

A tool for working with scalable vector graphics.

positional arguments:
  scripts               scripts to run for composing the SVG document (in
                        order)

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v, --verbose         set to increase logging verbosity
  -q, --quiet           set to reduce output
  --curses              whether or not to use curses.wrapper when starting
  --no-uvloop           whether or not to disable uvloop as event loop driver
  -C DIR, --dir DIR     execute from a specific directory
  -c CONFIG, --config CONFIG
                        top-level configuration to load (default:
                        'svgen.json')
  --height HEIGHT       height of the document, if not specified by
                        configuration (default: 100)
  --width WIDTH         width of the document, if not specified by
                        configuration (default: 100)
  --images              generate output images
  -o OUTPUT, --output OUTPUT
                        file to write SVG output (default: 'svgen.svg')

```

# Internal Dependency Graph

A coarse view of the internal structure and scale of
`svgen`'s source.
Generated using [pydeps](https://github.com/thebjorn/pydeps) (via
`mk python-deps`).

![svgen's Dependency Graph](im/pydeps.svg)
