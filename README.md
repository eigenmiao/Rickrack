<div align="center">
<img width="100%" align="center" src="src/main/icons/logo_long.png" alt="Rickrack">
<br/><br/>
Rickrack<br/>焰火十二卷<br/> ----- ----- ----- ----- ----- ----- ----- ----- <br/>
Generate Harmonious Colors Freely.<br/>自由自在生成和谐色彩。
<br/><br/>
[<a href="https://eigenmiao.com/yanhuo/">中文</a>] | [<a href="https://eigenmiao.com/rickrack/">English</a>]
<br/><br/>
</div>

# Rickrack
Rickrack (**R**e**a**l-t**i**me **C**olor **K**it) is a free and user-friendly color editor. It is designed to generate a set of harmonious colors from the color wheel or other places. You can share these colors with your friends, or apply them into your creative works.

# 焰火十二卷
焰火十二卷（实时色彩工具箱）是一款免费且实用的色彩编辑器。它可以帮助你从色轮或者其他地方生成一组和谐的色彩。你可以将这些色彩分享给其他人，或者应用到你自己的创作当中。

# Table of Content
* [Introduction](#introduction)
* [Feature](#feature)
* [Demo](#demo)
  * [Basic Functions](#basic-functions)
  * [Reference Colors](#reference-colors)
  * [Color Palettes](#color-palettes)
  * [Export and Import Colors](#export-and-import-colors)
  * [Languages and Settings](#languages-and-settings)
* [Reviews about Rickrack](#reviews-about-rickrack)
* [User Comments](#user-comments)
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
* [Development](#development)
  * [Install Requirement](#install-requirement)
  * [How to Build the Software](#how-to-build-the-software)
  * [How to Build the Module](#how-to-build-the-module)
* [Copyright](#copyright)
* [License](#license)
  * [License for Rickrack](#license-for-rickrack)
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

# Demo
## Basic Functions
|     |     |
| :---: | :---: |
| ![](demo/usage/000.gif) | ![](demo/usage/109.gif) |
| Create a set of colors from the color wheel. | Pick-up a set of colors from an image. (Image inside: [Copyright (c) 2001 Studio Ghibli](https://www.ghibli.jp/works/chihiro/), Non-Commercial Usage) |
| ![](demo/usage/202.gif) | ![](demo/usage/300.gif) |
| Generate a gradient color board from the color set. | Attach the color set and color board into the depot. |

## Reference Colors
|     |     |
| :---: | :---: |
| ![](demo/usage/018.gif) | ![](demo/usage/110.gif) |
| Add reference colors in the color wheel. | Add reference colors from the image. (Image inside: [Copyright (c) 2001 Studio Ghibli](https://www.ghibli.jp/works/chihiro/), Non-Commercial Usage) |

## Color Palettes
|     |     |
| :---: | :---: |
| ![](demo/usage/204.gif) | ![](demo/usage/205.gif) |
| Convert: gradient palette &harr; fixed palette. | Convert: gradient palette &harr; reference palette. |
| ![](demo/usage/700.gif) | ![](demo/usage/701.gif) |
| Fixed palette: Chinese Traditional Colors. (Color Names: [Copyright (c) China Science Publishing & Media Ltd.](http://zhongguose.com/), Non-Commercial Usage) | Fixed palette: Nippon Traditional Colors. (Color Names: [Copyright (c) PIE BOOKS.](http://nipponcolors.com/), Non-Commercial Usage) |

## Languages and Settings
|     |     |
| :---: | :---: |
| ![](demo/usage/707.gif) | ![](demo/usage/706.gif) |
| Support multiple languages, including Chinese, English, Japanese, German, French, Russian, and so on. (Languages except Chinese and English are translated by [Google Translate](https://translate.google.cn/).) | Support multiple interface themes. |

## Notice
* The interface display in demo uses [LXGWWenKai (SIL Open Font License)](https://lxgw.github.io/2021/01/28/Klee-Simpchin/) font.

<div align="right"><a href="#table-of-content">[-> Back to TOC <-]</a></div>

# Reviews about Rickrack
> All in all, Rickrack is a comprehensive tool for anything that requires color work. Experienced users have an exhaustive toolset to work with, while a more casual audience can improve the presentation of their art by quickly getting color synergy ideas. -- [Robert Condorache @ Softpedia](https://www.softpedia.com/get/Multimedia/Graphic/Graphic-Others/RickRack.shtml)

> Rickrack is an easy to use desktop app for creating and saving color palettes. It supports many major color palette formats for import and export, and is a great tool for generating color palettes of colors that go well together. -- [TJ FREE @ Youtube](https://www.youtube.com/watch?v=OUnktTCtv3E)

> ... and more!

<div align="right"><a href="#table-of-content">[-> Back to TOC <-]</a></div>

# User Comments
> 作为一个配色软件，它本身的色彩，嗯，足够惊艳...你完全可以信得过作者。 -- User from [Open Source China](https://www.oschina.net/comment/news/231426)

> 很棒！是一个不可多得的工具。 -- User from [Bilibili](https://www.bilibili.com/video/BV1VD4y157tX/)

> 谢谢分享，说明写的太详细了。 -- User from [Baidu Tieba](https://tieba.baidu.com/p/8253007907)

> Thanks a mil! All of my pallette creators were online. This a good offline tool to have with some additional features too. -- User from [Youtube](https://www.youtube.com/watch?v=OUnktTCtv3E)

> I don't like online-apps, so this is a huge plus from the get-go. Thanks for sharing this great tool. -- User from [Youtube](https://www.youtube.com/watch?v=OUnktTCtv3E)

> Thanks for sharing this! And - did I notice correctly that you are also the author of this software? This looks super exciting, can’t wait to investigate it more! -- User from [Krita Artists](https://krita-artists.org/t/alternatives-to-adobe-color-rickrack/60041)

> Hello, your software (the deb package) runs fine on Xubuntu 22.04 and is quite impressive! Thanks for sharing. Next step is to study some tutorials. -- User from [PIXLS.US](https://discuss.pixls.us/t/alternatives-to-adobe-color-rickrack/35997)

> ... and more!

<div align="right"><a href="#table-of-content">[-> Back to TOC <-]</a></div>

# Information
## Homepage
https://eigenmiao.com/rickrack/

## Repository
https://github.com/eigenmiao/Rickrack

## Author
[Eigenmiao](mailto:eigenmiao@outlook.com)

## Support
[Support the Future of Rickrack!](https://afdian.net/a/eigenmiao)

<div align="right"><a href="#table-of-content">[-> Back to TOC <-]</a></div>

# Installation
## Current Release
The latest preview version is [v2.7.25](https://github.com/eigenmiao/Rickrack/releases/tag/v2.7.25).

## Install Software
### Recommend: Install on Windows 10 or 11 via WinGet tool
```
winget install rickrack
```

## Install on other platforms
Download Software from [Github](https://github.com/eigenmiao/Rickrack/releases/tag/v2.7.25) or [Sourceforge](https://sourceforge.net/projects/rickrack/files/v2.7.25/). The installation steps are presented in [tutorials](https://eigenmiao.com/2021/12/12/rickrack-tutorial-en-v2.3.4/#Installation).

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

Here is a [demo](https://eigenmiao.com/2023/01/29/rickrack-alternative-to-adobe-color-en/).

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
```bash
# Download the Rickrack source code.
git clone https://github.com/eigenmiao/Rickrack.git

# Change into the directory.
cd Rickrack

# Run Rickrack.
python src/main/python/main.py

# Generate the installer for Rickrack.
fbs freeze && fbs installer
```

## How to Build the Module
```bash
# Download the Rickrack source code.
git clone https://github.com/eigenmiao/Rickrack.git

# Change into the directory.
cd Rickrack

# Generate the package for Rickrack.
python setup.py sdist --formats=gztar,zip
```

<div align="right"><a href="#table-of-content">[-> Back to TOC <-]</a></div>

# Copyright
Copyright (c) 2019-2023 [Eigenmiao](mailto:eigenmiao@outlook.com). All Rights Reserved.

<div align="right"><a href="#table-of-content">[-> Back to TOC <-]</a></div>

# Contributing
This project welcomes contributions of all types. Recommending Rickrack to people you know, writing reviews for Rickrack on websites, help spec'ing, design, documentation, finding bugs, etc. can all help the project grow better.

# License
## License for Rickrack
Rickrack is a free software, which is distributed in the hope that it will be useful, but without any warranty. You can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation. See the [GNU General Public License 3.0 (GPL 3.0)](https://www.gnu.org/licenses/) for more details.

All images, documents and translations in Rickrack [code repository](https://github.com/eigenmiao/Rickrack) are licensed under [Creative Commons Attribution-NonCommercial-ShareAlike License 4.0 (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/) unless stating additionally.

Rickrack default uses [Noto Serif](https://fonts.google.com/specimen/Noto+Serif) ([SC](https://fonts.google.com/specimen/Noto+Serif+SC)) fonts and [Noto Sans](https://fonts.google.com/specimen/Noto+Sans) ([SC](https://fonts.google.com/specimen/Noto+Sans+SC)) fonts for interface display, which are designed by Google and published in website [Google Fonts](https://fonts.google.com/). These fonts are open-sourced under [Apache 2.0](http://www.apache.org/licenses/) and [SIL Open Font License 1.1](http://scripts.sil.org/OFL), respectively.

# Acknowledgment
* The Rickrack software is written in [Python](https://www.python.org/), constructed based on [PyQt5](https://www.qt.io/qt-for-python) and packed up by [fbs (free edition)](https://build-system.fman.io/).
* The localization (l10n) and internationalization (i18n) of Rickrack is based on [Google Translate](https://translate.google.cn/) and [Microsoft Translator](https://cn.bing.com/translator), deployed on [POEditor](https://poeditor.com/join/project?hash=kBeQjfxCES).
* The code repository is deposited on [Github](https://github.com/eigenmiao/Rickrack) and [Gitee](https://gitee.com/eigenmiao/Rickrack).

<div align="right"><a href="#rickrack">[-> Back to Top <-]</a> <a href="#table-of-content">[-> Back to TOC <-]</a></div>
