#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
from setuptools import setup

name = "SystemEvent"

with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = name,
    version = "1.0.0",
    license = "MIT",
    description = "System-wide Event synchonization for posix (emulating the threading.Event api)",
    long_description = long_description,
    packages = ["SystemEvent"],
    scripts = [
        "bin/evt_clear",
        "bin/evt_set",
        "bin/evt_wait",
    ],
    install_requires = [
        "posix_ipc >= 1.0.0",
    ],
)
