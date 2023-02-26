<div align="center">
<img width="100%" align="center" src="src/main/icons/logo_long.png" alt="Rickrack">
<br/><br/>
Rickrack<br/>焰火十二卷<br/> ----- ----- ----- ----- ----- ----- ----- ----- <br/>
Generate Harmonious Colors Freely.<br/>自由自在生成和谐色彩。
<br/><br/>
[<a href="https://eigenmiao.com/yanhuo/zh.html">中文</a>] | [<a href="https://eigenmiao.com/yanhuo/en.html">English</a>] | [<a href="https://eigenmiao.com/yanhuo/ja.html">日本語</a>]
<br/><br/>
</div>

# Rickrack
Rickrack (**R**e**a**l-t**i**me **C**olor **K**it) is a free and user-friendly color editor. It is designed to generate a set of harmonious colors from the color wheel or other places. You can share these colors with your friends, or apply them into your creative works.

# 焰火十二卷
焰火十二卷（实时色彩工具箱）是一款免费且实用的色彩编辑器。它可以帮助你从色轮或者其他地方生成一组和谐的色彩。你可以将这些色彩分享给其他人，或者应用到你自己的创作当中。

# Table of Content
* [Introduction](#introduction)
* [Feature](#feature)
* [Information](#information)
  * [Homepage](#homepage)
  * [Repository](#repository)
  * [Author](#author)
  * [Support](#support)
* [Installation](#installation)
  * [Current Release](#current-release)
  * [Download Software](#download-software)
  * [Install Software](#install-software)
  * [Install Module](#install-module)
* [Usage](#usage)
  * [How to Use the Software](#how-to-use-the-software)
  * [How to Use the Module](#how-to-use-the-module)
  * [Notice](#notice)
* [Development](#development)
  * [Install Requirement](#install-requirement)
  * [How to Build the Software](#how-to-build-the-software)
  * [How to Build the Module](#how-to-build-the-module)
* [Copyright](#copyright)
* [License](#license)
  * [License for Rickrack](#license-for-rickrack)
  * [License for Required Packages](#license-for-required-packages)
* [Acknowledgment](#acknowledgment)

# Introduction
Colors enrich our world and affect our emotions. For artists, they display objects and convey feelings by varied colors in photos, images and drawings. For scientist, they present data by distinguishable colors in figures and graphics. However, the majority of color softwares and websites put restrictions on users, which include the inability to export color palettes into individual files, not providing invocation interfaces, requiring registrations, regional limitations and (or) collecting users' personal information.

If you are running into these issues, Rickrack is the perfect solution for you!

Rickrack is a free and user-friendly color editor. It is designed to generate a set of harmonious colors from the color wheel or other places. You can share these colors with your friends, or apply them into your creative works. You can store the color sets and color boards in the software, and access them whenever you need. What's more, you can export them into individual files, back them up, share them with others or import them in to other softwares such as Adobe Photoshop, GIMP, Krita, Pencil 2D and Clip Studio Paint. Rickrack, written in PyQt5, operates effectively on Windows, Linux and other mainstream operating systems.

Rickrack consists of two parts: the Rickrack software and the Rickrack module; the Rickrack software is designed for producing and organizing harmonious colors, and the Rickrack module is utilized for obtaining colors from the software in real-time, along with the plotting of images combined with other modules such as Matplotlib and Turtle.

<div align="right"><a href="#table-of-content">[-> Back to TOC <-]</a></div>

# Feature
Rickrack has several features:
* A strong and free color editor.
* Create a set of colors from the color wheel.
* Pick-up a set of colors from an image.
* Generate a color board from the color set.
* Attach the color set and color board into the depot.
* Import colors from elsewhere and manage them in depot.
* Export colors and import them into other image processors.
* Obtain colors through the Python module in real-time.
* No function limitations and no registration required.
* ... and more!

<div align="right"><a href="#table-of-content">[-> Back to TOC <-]</a></div>

# Information
## Homepage
https://eigenmiao.com/rickrack/

## Repository
https://github.com/eigenmiao/Rickrack

## Author
[Eigenmiao](mailto:eigenmiao@outlook.com)

## Support
[Support the Future of Rickrack!](https://eigenmiao.com/rickrack/support.html)

<div align="right"><a href="#table-of-content">[-> Back to TOC <-]</a></div>

# Installation
## Current Release
The latest preview version is [v2.7.23](https://github.com/eigenmiao/Rickrack/releases/tag/v2.7.23-pre).

## Download Software
https://github.com/eigenmiao/Rickrack/releases/tag/v2.7.23-pre

## Install Software
Visit https://eigenmiao.com/rickrack/ for more information. The installation steps are presented in [tutorials](https://eigenmiao.com/2021/12/12/rickrack-tutorial-en-v2.3.4/#Installation).

Here is a [video tutorial](https://www.bilibili.com/video/BV17r4y1L7R6/).

## Install Module
Install the latest [Rickrack](https://pypi.org/project/Rickrack/) from PyPI!

```Bash
# Install Rickrack.
pip install Rickrack

# Start the installed software.
rickrack -d "/PATH/TO/RICKRACK/SOFTWARE"
```

<div align="right"><a href="#table-of-content">[-> Back to TOC <-]</a></div>

# Usage
## How to Use the Software
Visit https://eigenmiao.com/rickrack/ for tutorials. Just feel free to click anywhere in the interface!

Here is a [video tutorial](https://www.bilibili.com/video/BV17L4y1A7P9/).

Here is a [demo](https://zhuanlan.zhihu.com/p/590842339).

## How to Use the Module
Include Rickrack in other Python scripts, programs and softwares!

Here is a [video tutorial](https://www.bilibili.com/video/BV1VD4y157tX/).

Here is a [demo](demo/).

```Python
# Use Rickrack module in code.
# This code fragment could be reused.

from rickrack import Rickrack

# Init Rickrack.
rr = Rickrack()

# Display the help information.
dp_proj = "/PATH/TO/RICKRACK/PROJECT"
dp_argv = dict()
dp_argv["help"] = True

# Run and see the full contents and examples.
rr.run(dp_argv=dp_argv, dp_proj=dp_proj)
```

## Notice
* Please read the documents and tutorials when you encounter any difficulties.
* The socket server is designed for obtaining colors from the Rickrack software in real-time. By default, this server is disabled and can only be started from the command line.

<div align="right"><a href="#table-of-content">[-> Back to TOC <-]</a></div>

# Development
## Install Requirement
* Python 3.6
* Git version control system
* Additional modules listed in requirements folder

## How to Build the Software
Rickrack requires the "ricore" module to function, however, it is not open-sourced yet and therefore is not supported.

## How to Build the Module
```bash
# Download the Rickrack source code.
git clone https://github.com/eigenmiao/Rickrack.git

# Change into the directory.
cd Rickrack

# Generate modules.
python setup.py sdist --formats=gztar,zip
```

<div align="right"><a href="#table-of-content">[-> Back to TOC <-]</a></div>

# Copyright
Copyright (c) 2019-2023 [Eigenmiao](mailto:eigenmiao@outlook.com). All Rights Reserved.

<div align="right"><a href="#table-of-content">[-> Back to TOC <-]</a></div>

# License
## License for Rickrack
Rickrack is a free software, which is distributed in the hope that it will be useful, but without any warranty. You can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation. See the [GNU General Public License 3.0 (GPL 3.0)](https://www.gnu.org/licenses/) for more details.

All images, documents and translations in Rickrack [code repository](https://github.com/eigenmiao/Rickrack) are licensed under [Creative Commons Attribution-NonCommercial-ShareAlike License 4.0 (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/) unless stating additionally.

Rickrack default uses [Noto Serif](https://fonts.google.com/specimen/Noto+Serif) ([SC](https://fonts.google.com/specimen/Noto+Serif+SC)) fonts and [Noto Sans](https://fonts.google.com/specimen/Noto+Sans) ([SC](https://fonts.google.com/specimen/Noto+Sans+SC)) fonts for interface display, which are designed by Google and published in website [Google Fonts](https://fonts.google.com/). These fonts are open-sourced under [Apache 2.0](http://www.apache.org/licenses/) and [SIL Open Font License 1.1](http://scripts.sil.org/OFL), respectively.

## License for Required Packages
| Package        | Version  | License        |
|----------------|----------|----------------|
| altgraph       | 0.17.2   | MIT            |
| fbs            | 0.8.9    | GPLv3 or Later |
| future         | 0.18.2   | MIT            |
| lxml           | 4.6.3    | BSD            |
| macholib       | 1.15.2   | MIT            |
| numpy          | 1.19.5   | BSD            |
| pefile         | 2021.9.3 | MIT            |
| Pillow         | 8.4.0    | HPND           |
| pip            | 21.3.1   | MIT            |
| PyInstaller    | 3.4      | GPLv2 or Later |
| PyQt5          | 5.12.1   | GPLv3          |
| PyQt5_sip      | 4.19.19  | SIP            |
| pywin32        | 302      | PSF            |
| pywin32-ctypes | 0.2.0    | BSD            |
| ricore         | 0.0.0    | Private Module |
| setuptools     | 40.6.2   | MIT            |
| swatch         | 0.4.0    | MIT            |

<div align="right"><a href="#table-of-content">[-> Back to TOC <-]</a></div>

# Acknowledgment
* The Rickrack software is written in [Python](https://www.python.org/), constructed based on [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) and packed up by [fbs (free edition)](https://build-system.fman.io/).
* The localization (l10n) and internationalization (i18n) of Rickrack is based on [Google Translate](https://translate.google.cn/) and [Microsoft Translator](https://cn.bing.com/translator), deployed on [POEditor](https://poeditor.com/join/project?hash=kBeQjfxCES).
* The code repository is deposited on [Github](https://github.com/eigenmiao/Rickrack) and [Gitee](https://gitee.com/eigenmiao/Rickrack).

<div align="right"><a href="#rickrack">[-> Back to Top <-]</a> <a href="#table-of-content">[-> Back to TOC <-]</a></div>
