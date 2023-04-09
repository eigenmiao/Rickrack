# -*- coding: utf-8 -*-

"""
Real-time Color Kit (Rickrack) is a free software, which is distributed 
in the hope that it will be useful, but WITHOUT ANY WARRANTY. You can 
redistribute it and/or modify it under the terms of the GNU General Public 
License as published by the Free Software Foundation. See the GNU General 
Public License for more details.

Please visit https://github.com/eigenmiao/Rickrack for more 
infomation about Rickrack.

NOTICE:
  The wheel (__SVG_WHEEL__), image (__SVG_IMAGE__), board (__SVG_BOARD__) 
  and depot (__SVG_DEPOT__) svg images in this script are copyrighted to 
  Eigenmiao.
  Other svg images are obtained and modified from Remix Icon, Copyright 
  (c) 2020 by Remix Design. See: http://remixicon.cn/.

Copyright (c) 2019-2022 by Eigenmiao. All Rights Reserved.
"""

__SVG_FMT__ = """
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="100mm" height="100mm" viewBox="0 0 100 100" version="1.1">
{context}
</svg>
"""

__SVG_WHEEL__ = """
  <g>
    <path
       style="fill:#{backcolor};fill-opacity:0.5;stroke:#{forecolor};stroke-width:0;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
       d="M 18.18,18.180195 50,5.000001 V 50 L 18.18,18.180195" />
    <path
       style="fill:#{backcolor};fill-opacity:0.3;stroke:#{forecolor};stroke-width:0;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
       d="M 5,50 18.18,18.180195 50,50 H 5" />
    <path
       style="fill:#{backcolor};fill-opacity:0.5;stroke:#{forecolor};stroke-width:0;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
       d="M 18.18,81.819805 5,50 H 50 L 18.18,81.819805" />
    <path
       style="fill:#{backcolor};fill-opacity:0.3;stroke:#{forecolor};stroke-width:0;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
       d="M 50,94.999997 18.18,81.819805 50,50 v 44.999997" />
    <path
       style="fill:#{backcolor};fill-opacity:0.5;stroke:#{forecolor};stroke-width:0;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
       d="M 81.819998,81.819805 50,94.999997 V 50 l 31.819998,31.819805" />
    <path
       style="fill:#{backcolor};fill-opacity:0.3;stroke:#{forecolor};stroke-width:0;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
       d="M 94.999997,50 81.819998,81.819805 50,50 h 44.999997" />
    <path
       style="fill:#{backcolor};fill-opacity:0.5;stroke:#{forecolor};stroke-width:0;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
       d="M 81.819998,18.180195 94.999997,50 H 50 Z" />
    <path
       style="fill:#{backcolor};fill-opacity:0.3;stroke:#{forecolor};stroke-width:0;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
       d="M 50,5.000001 81.819998,18.180195 50,50 V 5.000001" />
    <path
       style="fill:none;fill-opacity:1;stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
       d="M 18.18,18.180195 50,5.000001 81.819998,18.180195 94.999997,50 81.819998,81.819805 50,94.999997 18.18,81.819805 5,50 Z" />
    <path
       style="fill:#{backcolor};fill-opacity:1;stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
       d="M 28.749633,55.694018 55.694,28.749633 65.556,65.556349 Z" />
  </g>
"""

__SVG_IMAGE__ = """
  <g>
    <rect
       style="fill:#{backcolor};fill-opacity:{opacity};stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;paint-order:markers fill stroke"
       width="90.000244" height="67.000565" x="4.9998775" y="16.499878" />
    <path
       style="display:inline;fill:#{backcolor};fill-opacity:{opacity};stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
       d="M 44.058367,83.500326 68.471103,41.216196 92.883454,83.500443 Z" />
    <path
       style="display:inline;fill:#{backcolor};fill-opacity:1.0;stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
       d="M 22.811893,83.500361 39.85613,53.978856 56.900098,83.500443 Z" />
    <ellipse
       style="fill:#{backcolor};fill-opacity:{opacity};stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;paint-order:markers fill stroke"
       cx="24.699829" cy="35.657875" rx="10.998136" ry="10.998135" />
  </g>
"""

__SVG_BOARD__ = """
  <g>
    <rect
       style="display:inline;fill:#{backcolor};fill-opacity:0.3;stroke:#{forecolor};stroke-width:0;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers"
       width="29.999998" height="29.999992" x="5.0000005" y="5.0000072" />
    <rect
       style="display:inline;fill:#{backcolor};fill-opacity:0.5;stroke:#{forecolor};stroke-width:0;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers"
       width="29.999998" height="29.999992" x="5.0000014" y="35.000004" />
    <rect
       style="display:inline;fill:#{backcolor};fill-opacity:0.8;stroke:#{forecolor};stroke-width:0;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers"
       width="29.999998" height="29.999992" x="5.0000024" y="64.999992" />
    <rect
       style="display:inline;fill:#{backcolor};fill-opacity:0.9;stroke:#{forecolor};stroke-width:0;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers"
       width="29.999998" height="29.999992" x="35" y="5.0000005" />
    <rect
       style="display:inline;fill:#{backcolor};fill-opacity:0.4;stroke:#{forecolor};stroke-width:0;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers"
       width="29.999998" height="29.999992" x="35" y="35" />
    <rect
       style="display:inline;fill:#{backcolor};fill-opacity:0.6;stroke:#{forecolor};stroke-width:0;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers"
       width="29.999998" height="29.999992" x="35" y="64.999992" />
    <rect
       style="display:inline;fill:#{backcolor};fill-opacity:0.5;stroke:#{forecolor};stroke-width:0;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers"
       width="29.999998" height="29.999992" x="65" y="5.0000091" />
    <rect
       style="display:inline;fill:#{backcolor};fill-opacity:0.8;stroke:#{forecolor};stroke-width:0;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers"
       width="29.999998" height="29.999992" x="65" y="35.000008" />
    <rect
       style="display:inline;fill:#{backcolor};fill-opacity:1;stroke:#{forecolor};stroke-width:0;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers"
       width="29.999998" height="29.999992" x="65" y="65.000008" />
    <path
       style="fill:none;stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers"
       d="m 5.0000005,5.0000071 89.9999985,1.9e-6 v 89.99999 l -89.9999966,-1.6e-5 z" />
    <path
       style="fill:none;stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers"
       d="m 5.0000013,35.000004 89.9999977,-6e-6" />
    <path
       style="fill:none;stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers"
       d="m 5.0000013,64.999999 89.9999977,8e-6" />
    <path
       style="fill:none;stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers"
       d="M 64.999999,5.000009 V 94.999983" />
    <path
       style="fill:none;stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers"
       d="M 34.999998,5.0000071 V 94.999983" />
  </g>
"""

__SVG_DEPOT__ = """
  <g>
    <path
       style="display:inline;fill:#{backcolor};fill-opacity:{opacity};stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:normal"
       d="M 11.672646,5 C 7.975874,5 5.0000006,7.9758686 5.0000006,11.672637 v 28.862815 c 0,3.696773 2.9758734,6.672641 6.6726454,6.672641 H 23.944973 A 26.204675,26.204663 0 0 1 47.208116,23.944412 V 11.672637 C 47.208116,7.9758686 44.232246,5 40.535473,5 Z" />
    <path
       style="display:inline;fill:#{backcolor};fill-opacity:{opacity};stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:normal"
       d="m 59.464528,5 c -3.69677,0 -6.672643,2.9758686 -6.672643,6.672637 V 23.944961 A 26.204675,26.204663 0 0 1 76.05557,47.208093 h 12.271785 c 3.696777,0 6.672644,-2.975868 6.672644,-6.672641 V 11.672637 C 94.999999,7.9758686 92.024132,5 88.327355,5 Z" />
    <path
       style="display:inline;fill:#{backcolor};fill-opacity:{opacity};stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:normal"
       d="m 11.672646,52.79186 c -3.696772,0 -6.6726454,2.975868 -6.6726454,6.672637 v 28.862821 c 0,3.696764 2.9758734,6.67263 6.6726454,6.67263 h 28.862827 c 3.696773,0 6.672643,-2.975866 6.672643,-6.67263 V 76.05499 A 26.204675,26.204663 0 0 1 23.944426,52.79186 Z" />
    <path
       style="display:inline;fill:#{backcolor};fill-opacity:{opacity};stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:normal"
       d="M 76.055027,52.79186 A 26.204675,26.204663 0 0 1 52.791885,76.055537 v 12.271781 c 0,3.696764 2.975873,6.67263 6.672643,6.67263 h 28.862827 c 3.696777,0 6.672644,-2.975866 6.672644,-6.67263 V 59.464497 c 0,-3.696769 -2.975867,-6.672637 -6.672644,-6.672637 z" />
  </g>
"""

__SVG_ABOUT__ = """
  <g>
    <path
       d="M 50.000017,95.000036 C 25.146497,95.000036 5,74.853525 5,50.000013 5,25.146498 25.146497,5 50.000017,5 c 24.85352,0 45.000019,20.146498 45.000019,45.000013 0,24.853512 -20.146499,45.000023 -45.000019,45.000023 z"
       style="fill:#{backcolor};fill-opacity:{opacity};stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" />
    <path
       d="m 45.500025,27.499998 h 8.999994 v 9.000009 h -8.999994 z m 0,18.000019 h 8.999994 v 27.000008 h -8.999994 z"
       style="display:inline;fill:#{forecolor};fill-opacity:1;stroke:#{forecolor};stroke-width:1;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" />
  </g>
"""

__SVG_SETTINGS__ = """
  <g>
    <path
       d="m 5.9703482,59.267535 c -1.2938074,-6.11061 -1.2938074,-12.424424 0,-18.535035 4.9936948,0.584916 9.3575898,-1.066273 10.7790678,-4.503299 1.426578,-3.441565 -0.486293,-7.692919 -4.435647,-10.810576 3.405753,-5.235132 7.869828,-9.699226 13.104944,-13.104995 3.113131,3.945448 7.368883,5.861926 10.810513,4.435823 3.441639,-1.426066 5.092657,-5.785461 4.503327,-10.7791107 6.110581,-1.2937996 12.42436,-1.2937996 18.53494,0 -0.584915,4.9936497 1.066103,9.3574817 4.503317,10.7791107 3.441631,1.426069 7.692968,-0.485954 10.810523,-4.435823 5.235112,3.40577 9.699185,7.869864 13.104934,13.104995 -3.94544,3.113152 -5.861883,7.369011 -4.435646,10.810576 1.426575,3.441602 5.785373,5.092648 10.779067,4.503299 1.293808,6.110611 1.293808,12.424425 0,18.535035 -4.993694,-0.584906 -9.357589,1.066282 -10.779067,4.50329 -1.426578,3.441574 0.486293,7.692929 4.435646,10.810588 -3.405749,5.23513 -7.869822,9.699223 -13.104934,13.104992 -3.11314,-3.94545 -7.368892,-5.86194 -10.810523,-4.435818 -3.441638,1.426064 -5.092656,5.78546 -4.503317,10.779107 -6.11058,1.2938 -12.424359,1.2938 -18.53494,0 0.584906,-4.993647 -1.066112,-9.357486 -4.503327,-10.779107 -3.44163,-1.426075 -7.692968,0.485953 -10.810513,4.435818 -5.235115,-3.405768 -9.699191,-7.869861 -13.104944,-13.104992 3.94527,-3.113159 5.861884,-7.369014 4.435647,-10.810588 -1.426575,-3.441582 -5.785373,-5.092639 -10.7790678,-4.50329 z"
       style="fill:#{backcolor};fill-opacity:{opacity};stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" />
    <path
       d="m 50.000019,63.496392 c -7.453839,0 -13.496355,-6.042536 -13.496355,-13.496379 0,-7.453843 6.042516,-13.496379 13.496355,-13.496379 7.453838,0 13.496354,6.042536 13.496354,13.496379 0,7.453843 -6.042516,13.496379 -13.496354,13.496379 z"
       style="display:inline;fill:#{backcolor};fill-opacity:0.8;stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" />
  </g>
"""

__SVG_SAVE__ = """
  <g>
    <path
       d="m 80.000087,85.000029 h 4.999995 V 24.140008 L 75.860085,15.00001 H 70.000076 V 35.000012 H 25.000058 V 15.00001 h -9.999991 v 70.000019 h 4.999996 V 50.000018 H 80.000087 Z M 10.000053,5 H 80.000087 L 93.53509,18.535004 a 5.0000019,5.0000019 0 0 1 1.464946,3.534994 V 90.000042 A 5.0000019,5.0000019 0 0 1 90.00004,95.000038 H 9.9999956 A 5.0000019,5.0000019 0 0 1 5,90.000042 V 9.9999956 A 5.0000019,5.0000019 0 0 1 9.9999956,5 Z M 30.000072,60.000028 V 85.000029 H 70.000076 V 60.000028 Z"
       style="fill:#{forecolor};fill-opacity:0.8;stroke:#{backcolor};stroke-width:0;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers" />
  </g>
"""

__SVG_OPEN__ = """
  <g>
    <path
       d="M 9.3902078,89.512495 A 4.3902535,4.3902772 0 0 1 5.0000049,85.122219 V 14.877781 A 4.3902535,4.3902772 0 0 1 9.3902078,10.487505 H 41.939525 l 8.780567,8.780553 h 33.304475 a 4.3902535,4.3902772 0 0 1 4.390203,4.390278 V 36.82917 H 79.634203 V 28.048614 H 47.084877 L 38.30448,19.268058 H 13.780401 V 71.942606 L 20.365866,45.609722 H 95.000065 L 84.858706,86.189055 a 4.3902535,4.3902772 0 0 1 -4.258613,3.32344 z M 83.752275,54.390277 H 27.223454 l -6.585465,26.341665 h 56.52899 z"
       style="fill:#{forecolor};fill-opacity:0.8;stroke:#{backcolor};stroke-width:0;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers" />
  </g>
"""

__SVG_QUIT__ = """
  <g>
    <path
       d="M 10.99911,94.999998 A 4.4999963,4.5000007 0 0 1 6.4990005,90.500011 V 9.4999964 A 4.4999963,4.5000007 0 0 1 10.99911,5.0000005 h 62.999836 a 4.4999963,4.5000007 0 0 1 4.50011,4.4999959 V 22.999997 H 69.499007 V 13.99999 H 15.499049 V 86.000011 H 69.499007 V 77.00001 h 9.000049 v 13.500001 a 4.4999963,4.5000007 0 0 1 -4.50011,4.499987 z M 69.499007,68 V 54.499998 H 37.999084 V 45.500007 H 69.499007 V 32.000005 l 22.500036,17.999998 z"
       style="fill:#{forecolor};fill-opacity:0.8;stroke:#{backcolor};stroke-width:0;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers" />
  </g>
"""

__SVG_HOME__ = """
  <g>
    <path
       d="M 78.636617,90.184507 H 21.363388 c -2.25937,5e-6 -4.090955,-1.831568 -4.090956,-4.09093 V 49.275221 H 4.9995953 L 47.246788,10.869572 c 1.560775,-1.420149 3.945656,-1.420149 5.50643,0 L 95.000405,49.275221 H 82.727572 v 36.818356 c -10e-7,2.259362 -1.831584,4.090934 -4.090955,4.09093 z M 33.636226,65.638932 h 32.727549 v 8.181864 H 33.636226 Z"
       style="fill:#{backcolor};fill-opacity:{opacity};stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" />
  </g>
"""

__SVG_UPDATE__ = """
  <g>
    <path
       d="M 20.583486,15.948524 A 44.824523,44.824523 0 0 1 50,5.0000236 c 24.853509,0 45.000016,20.1465004 45.000016,45.0000214 0,9.612004 -3.015011,18.522007 -8.145012,25.83 l -14.354987,-25.83 H 86.000022 A 36.000017,36.000017 0 0 0 25.069979,24.026027 Z M 79.41651,84.051558 A 44.824523,44.824523 0 0 1 50,95.000059 c -24.85352,0 -45.00002,-20.146505 -45.00002,-45.000014 0,-9.61201 3.014987,-18.522014 8.14499,-25.830013 L 27.499979,50.000045 H 13.999972 a 36.000017,36.000017 0 0 0 60.930045,25.974009 z"
       style="fill:#{forecolor};fill-opacity:0.8;stroke:#{backcolor};stroke-width:0;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers" />
  </g>
"""

import os
from PyQt5.QtGui import QIcon


def get_icon(name, forecolor, backcolor, temp_dir, default):
    name_dict = {
        "wheel": __SVG_WHEEL__,
        "image": __SVG_IMAGE__,
        "board": __SVG_BOARD__,
        "depot": __SVG_DEPOT__,
        "about": __SVG_ABOUT__,
        "settings": __SVG_SETTINGS__,
        "save": __SVG_SAVE__,
        "open": __SVG_OPEN__,
        "quit": __SVG_QUIT__,
        "home": __SVG_HOME__,
        "update": __SVG_UPDATE__,
    }

    if os.path.isdir(temp_dir) and name in name_dict:
        with open(os.sep.join([temp_dir, "{}.svg".format(name)]), "w") as f:
            context = name_dict[name].format(forecolor=forecolor, backcolor=backcolor, stroke=6, opacity=0.3)
            f.write(__SVG_FMT__.format(context=context)[1:])

        return QIcon(os.sep.join([temp_dir, "{}.svg".format(name)]))

    return default
