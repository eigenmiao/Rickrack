# -*- coding: utf-8 -*-

"""
Real-time Color Kit (Rickrack) is a free software, which is distributed 
in the hope that it will be useful, but WITHOUT ANY WARRANTY. You can 
redistribute it and/or modify it under the terms of the GNU General Public 
License as published by the Free Software Foundation. See the GNU General 
Public License for more details.

Please visit https://github.com/eigenmiao/Rickrack for more infomation 
about Rickrack.

Copyright (c) 2019-2022 by Eigenmiao. All Rights Reserved.
"""

from setuptools import setup


setup(
    name="Rickrack",
    version="2.5.24",
    author="Eigenmiao",
    author_email="eigenmiao@outlook.com",
    description="Generate harmonious colors freely.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://eigenmiao.github.io/rickrack/",
    classifiers=[
        "Topic :: Multimedia :: Graphics",
        "Topic :: Utilities",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Environment :: X11 Applications",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Other Audience",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
    ],
    keywords=["Color-Editor", "Color-Picker", "Color-Palette", "Digital-Palette", "Desktop-Application"],
    install_requires=[
        "numpy",
    ],
    python_requires=">=3.5",
    entry_points={
        "console_scripts": [
            "rickrack = rickrack.rickrack:startup",
        ],
        "gui_scripts": [
            "rickrack-gui = rickrack.rickrack:startup",
        ],
    },
    include_package_data=True,
    packages=["rickrack"],
    package_data={
        "rickrack": [
            "rickrack/*",
        ],
    }
)
