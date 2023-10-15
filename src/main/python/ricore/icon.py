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
<svg width="{wid}mm" height="{hig}mm" viewBox="0 0 {swid} {shig}" version="1.1"><g>
{context}
</g></svg>
"""

__SVG_WHEEL__ = """
<path style="fill:#{backcolor};fill-opacity:{lowopacity};stroke:#{forecolor};stroke-width:0;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" d="M 18.18,18.180195 50,5.000001 V 50 L 18.18,18.180195" />
<path style="fill:#{backcolor};fill-opacity:{lowopacity};stroke:#{forecolor};stroke-width:0;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" d="M 5,50 18.18,18.180195 50,50 H 5" />
<path style="fill:#{backcolor};fill-opacity:{lowopacity};stroke:#{forecolor};stroke-width:0;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" d="M 18.18,81.819805 5,50 H 50 L 18.18,81.819805" />
<path style="fill:#{backcolor};fill-opacity:{lowopacity};stroke:#{forecolor};stroke-width:0;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" d="M 50,94.999997 18.18,81.819805 50,50 v 44.999997" />
<path style="fill:#{backcolor};fill-opacity:{lowopacity};stroke:#{forecolor};stroke-width:0;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" d="M 81.819998,81.819805 50,94.999997 V 50 l 31.819998,31.819805" />
<path style="fill:#{backcolor};fill-opacity:{lowopacity};stroke:#{forecolor};stroke-width:0;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" d="M 94.999997,50 81.819998,81.819805 50,50 h 44.999997" />
<path style="fill:#{backcolor};fill-opacity:{lowopacity};stroke:#{forecolor};stroke-width:0;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" d="M 81.819998,18.180195 94.999997,50 H 50 Z" />
<path style="fill:#{backcolor};fill-opacity:{lowopacity};stroke:#{forecolor};stroke-width:0;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" d="M 50,5.000001 81.819998,18.180195 50,50 V 5.000001" />
<path style="fill:none;fill-opacity:0;stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" d="M 18.18,18.180195 50,5.000001 81.819998,18.180195 94.999997,50 81.819998,81.819805 50,94.999997 18.18,81.819805 5,50 Z" />
<path style="fill:#{backcolor};fill-opacity:{higopacity};stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" d="M 28.749633,55.694018 55.694,28.749633 65.556,65.556349 Z" />
"""

__SVG_IMAGE__ = """
<rect style="fill:#{backcolor};fill-opacity:{lowopacity};stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;paint-order:markers fill stroke" width="90.000244" height="67.000565" x="4.9998775" y="16.499878" />
<path style="display:inline;fill:#{backcolor};fill-opacity:{higopacity};stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" d="M 44.058367,83.500326 68.471103,41.216196 92.883454,83.500443 Z" />
<path style="display:inline;fill:#{backcolor};fill-opacity:{higopacity};stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" d="M 22.811893,83.500361 39.85613,53.978856 56.900098,83.500443 Z" />
<ellipse style="fill:#{backcolor};fill-opacity:{higopacity};stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;paint-order:markers fill stroke" cx="24.699829" cy="35.657875" rx="10.998136" ry="10.998135" />
"""

__SVG_BOARD__ = """
<rect style="display:inline;fill:#{backcolor};fill-opacity:{lowopacity};stroke:#{forecolor};stroke-width:0;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers" width="29.999998" height="29.999992" x="5.0000005" y="5.0000072" />
<rect style="display:inline;fill:#{backcolor};fill-opacity:{lowopacity};stroke:#{forecolor};stroke-width:0;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers" width="29.999998" height="29.999992" x="5.0000014" y="35.000004" />
<rect style="display:inline;fill:#{backcolor};fill-opacity:{higopacity};stroke:#{forecolor};stroke-width:0;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers" width="29.999998" height="29.999992" x="5.0000024" y="64.999992" />
<rect style="display:inline;fill:#{backcolor};fill-opacity:{higopacity};stroke:#{forecolor};stroke-width:0;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers" width="29.999998" height="29.999992" x="35" y="5.0000005" />
<rect style="display:inline;fill:#{backcolor};fill-opacity:{lowopacity};stroke:#{forecolor};stroke-width:0;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers" width="29.999998" height="29.999992" x="35" y="35" />
<rect style="display:inline;fill:#{backcolor};fill-opacity:{higopacity};stroke:#{forecolor};stroke-width:0;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers" width="29.999998" height="29.999992" x="35" y="64.999992" />
<rect style="display:inline;fill:#{backcolor};fill-opacity:{lowopacity};stroke:#{forecolor};stroke-width:0;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers" width="29.999998" height="29.999992" x="65" y="5.0000091" />
<rect style="display:inline;fill:#{backcolor};fill-opacity:{higopacity};stroke:#{forecolor};stroke-width:0;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers" width="29.999998" height="29.999992" x="65" y="35.000008" />
<rect style="display:inline;fill:#{backcolor};fill-opacity:{lowopacity};stroke:#{forecolor};stroke-width:0;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers" width="29.999998" height="29.999992" x="65" y="65.000008" />
<path style="fill:none;stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers" d="m 5.0000005,5.0000071 89.9999985,1.9e-6 v 89.99999 l -89.9999966,-1.6e-5 z" />
<path style="fill:none;stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers" d="m 5.0000013,35.000004 89.9999977,-6e-6" />
<path style="fill:none;stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers" d="m 5.0000013,64.999999 89.9999977,8e-6" />
<path style="fill:none;stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers" d="M 64.999999,5.000009 V 94.999983" />
<path style="fill:none;stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers" d="M 34.999998,5.0000071 V 94.999983" />
"""

__SVG_DEPOT__ = """
<path style="display:inline;fill:#{backcolor};fill-opacity:{higopacity};stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:normal" d="M 11.672646,5 C 7.975874,5 5.0000006,7.9758686 5.0000006,11.672637 v 28.862815 c 0,3.696773 2.9758734,6.672641 6.6726454,6.672641 H 23.944973 A 26.204675,26.204663 0 0 1 47.208116,23.944412 V 11.672637 C 47.208116,7.9758686 44.232246,5 40.535473,5 Z" />
<path style="display:inline;fill:#{backcolor};fill-opacity:{higopacity};stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:normal" d="m 59.464528,5 c -3.69677,0 -6.672643,2.9758686 -6.672643,6.672637 V 23.944961 A 26.204675,26.204663 0 0 1 76.05557,47.208093 h 12.271785 c 3.696777,0 6.672644,-2.975868 6.672644,-6.672641 V 11.672637 C 94.999999,7.9758686 92.024132,5 88.327355,5 Z" />
<path style="display:inline;fill:#{backcolor};fill-opacity:{higopacity};stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:normal" d="m 11.672646,52.79186 c -3.696772,0 -6.6726454,2.975868 -6.6726454,6.672637 v 28.862821 c 0,3.696764 2.9758734,6.67263 6.6726454,6.67263 h 28.862827 c 3.696773,0 6.672643,-2.975866 6.672643,-6.67263 V 76.05499 A 26.204675,26.204663 0 0 1 23.944426,52.79186 Z" />
<path style="display:inline;fill:#{backcolor};fill-opacity:{higopacity};stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;paint-order:normal" d="M 76.055027,52.79186 A 26.204675,26.204663 0 0 1 52.791885,76.055537 v 12.271781 c 0,3.696764 2.975873,6.67263 6.672643,6.67263 h 28.862827 c 3.696777,0 6.672644,-2.975866 6.672644,-6.67263 V 59.464497 c 0,-3.696769 -2.975867,-6.672637 -6.672644,-6.672637 z" />
"""

__SVG_ABOUT__ = """
<path d="M 50.000017,95.000036 C 25.146497,95.000036 5,74.853525 5,50.000013 5,25.146498 25.146497,5 50.000017,5 c 24.85352,0 45.000019,20.146498 45.000019,45.000013 0,24.853512 -20.146499,45.000023 -45.000019,45.000023 z" style="fill:#{backcolor};fill-opacity:{lowopacity};stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" />
<path d="m 45.500025,27.499998 h 8.999994 v 9.000009 h -8.999994 z m 0,18.000019 h 8.999994 v 27.000008 h -8.999994 z" style="display:inline;fill:#{forecolor};fill-opacity:{higopacity};stroke:#{forecolor};stroke-width:1;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" />
"""

__SVG_INFO__ = """
<path d="M20.2426 4.75736C22.5053 7.02472 22.583 10.637 20.4786 12.993L11.9999 21.485L3.52138 12.993C1.41705 10.637 1.49571 7.01901 3.75736 4.75736C6.02157 2.49315 9.64519 2.41687 12.001 4.52853C14.35 2.42 17.98 2.49 20.2426 4.75736ZM5.17157 6.17157C3.68183 7.66131 3.60704 10.0473 4.97993 11.6232L11.9999 18.6543L19.0201 11.6232C20.3935 10.0467 20.319 7.66525 18.827 6.1701C17.3397 4.67979 14.9458 4.60806 13.3743 5.98376L9.17157 10.1869L7.75736 8.77264L10.582 5.946L10.5002 5.87701C8.92545 4.61197 6.62322 4.71993 5.17157 6.17157Z" fill="#{forecolor}"></path>
"""

__SVG_SETTINGS__ = """
<path d="m 5.9703482,59.267535 c -1.2938074,-6.11061 -1.2938074,-12.424424 0,-18.535035 4.9936948,0.584916 9.3575898,-1.066273 10.7790678,-4.503299 1.426578,-3.441565 -0.486293,-7.692919 -4.435647,-10.810576 3.405753,-5.235132 7.869828,-9.699226 13.104944,-13.104995 3.113131,3.945448 7.368883,5.861926 10.810513,4.435823 3.441639,-1.426066 5.092657,-5.785461 4.503327,-10.7791107 6.110581,-1.2937996 12.42436,-1.2937996 18.53494,0 -0.584915,4.9936497 1.066103,9.3574817 4.503317,10.7791107 3.441631,1.426069 7.692968,-0.485954 10.810523,-4.435823 5.235112,3.40577 9.699185,7.869864 13.104934,13.104995 -3.94544,3.113152 -5.861883,7.369011 -4.435646,10.810576 1.426575,3.441602 5.785373,5.092648 10.779067,4.503299 1.293808,6.110611 1.293808,12.424425 0,18.535035 -4.993694,-0.584906 -9.357589,1.066282 -10.779067,4.50329 -1.426578,3.441574 0.486293,7.692929 4.435646,10.810588 -3.405749,5.23513 -7.869822,9.699223 -13.104934,13.104992 -3.11314,-3.94545 -7.368892,-5.86194 -10.810523,-4.435818 -3.441638,1.426064 -5.092656,5.78546 -4.503317,10.779107 -6.11058,1.2938 -12.424359,1.2938 -18.53494,0 0.584906,-4.993647 -1.066112,-9.357486 -4.503327,-10.779107 -3.44163,-1.426075 -7.692968,0.485953 -10.810513,4.435818 -5.235115,-3.405768 -9.699191,-7.869861 -13.104944,-13.104992 3.94527,-3.113159 5.861884,-7.369014 4.435647,-10.810588 -1.426575,-3.441582 -5.785373,-5.092639 -10.7790678,-4.50329 z" style="fill:#{backcolor};fill-opacity:{lowopacity};stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" />
<path d="m 50.000019,63.496392 c -7.453839,0 -13.496355,-6.042536 -13.496355,-13.496379 0,-7.453843 6.042516,-13.496379 13.496355,-13.496379 7.453838,0 13.496354,6.042536 13.496354,13.496379 0,7.453843 -6.042516,13.496379 -13.496354,13.496379 z" style="display:inline;fill:#{backcolor};fill-opacity:{higopacity};stroke:#{forecolor};stroke-width:{stroke};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" />
"""

__SVG_SAVE__ = """
<path d="M18 19H19V6.82843L17.1716 5H16V9H7V5H5V19H6V12H18V19ZM4 3H18L20.7071 5.70711C20.8946 5.89464 21 6.149 21 6.41421V20C21 20.5523 20.5523 21 20 21H4C3.44772 21 3 20.5523 3 20V4C3 3.44772 3.44772 3 4 3ZM8 14V19H16V14H8Z" fill="#{forecolor}"></path>
"""

__SVG_OPEN__ = """
<path d="M3 21C2.44772 21 2 20.5523 2 20V4C2 3.44772 2.44772 3 3 3H10.4142L12.4142 5H20C20.5523 5 21 5.44772 21 6V9H19V7H11.5858L9.58579 5H4V16.998L5.5 11H22.5L20.1894 20.2425C20.0781 20.6877 19.6781 21 19.2192 21H3ZM19.9384 13H7.06155L5.56155 19H18.4384L19.9384 13Z" fill="#{forecolor}"></path>
"""

__SVG_QUIT__ = """
<path d="M5 22C4.44772 22 4 21.5523 4 21V3C4 2.44772 4.44772 2 5 2H19C19.5523 2 20 2.44772 20 3V6H18V4H6V20H18V18H20V21C20 21.5523 19.5523 22 19 22H5ZM18 16V13H11V11H18V8L23 12L18 16Z" fill="#{forecolor}"></path>
"""

__SVG_HOME__ = """
<path d="M19 21.0001H5C4.44772 21.0001 4 20.5524 4 20.0001V11.0001L1 11.0001L11.3273 1.61162C11.7087 1.26488 12.2913 1.26488 12.6727 1.61162L23 11.0001L20 11.0001V20.0001C20 20.5524 19.5523 21.0001 19 21.0001ZM6 19.0001H18V9.15757L12 3.70302L6 9.15757V19.0001ZM8 15.0001H16V17.0001H8V15.0001Z" fill="#{forecolor}"></path>
"""

__SVG_UPDATE__ = """
<path d="M12 4C9.25144 4 6.82508 5.38626 5.38443 7.5H8V9.5H2V3.5H4V5.99936C5.82381 3.57166 8.72764 2 12 2C17.5228 2 22 6.47715 22 12H20C20 7.58172 16.4183 4 12 4ZM4 12C4 16.4183 7.58172 20 12 20C14.7486 20 17.1749 18.6137 18.6156 16.5H16V14.5H22V20.5H20V18.0006C18.1762 20.4283 15.2724 22 12 22C6.47715 22 2 17.5228 2 12H4Z" fill="#{forecolor}"></path>
"""

__SVG_FORUM__ = """
<path d="M2 8.99374C2 5.68349 4.67654 3 8.00066 3H15.9993C19.3134 3 22 5.69478 22 8.99374V21H8.00066C4.68659 21 2 18.3052 2 15.0063V8.99374ZM20 19V8.99374C20 6.79539 18.2049 5 15.9993 5H8.00066C5.78458 5 4 6.78458 4 8.99374V15.0063C4 17.2046 5.79512 19 8.00066 19H20ZM14 11H16V13H14V11ZM8 11H10V13H8V11Z" fill="#{forecolor}"></path>
"""

__SVG_UP__ = """
<path style="fill:none;stroke:#{forecolor};stroke-width:2.4;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:{higopacity};stroke-miterlimit:4;stroke-dasharray:none" d="m 5.6652622,8.3644365 6.3347398,-6.3346739 6.33474,6.3346739" />
"""

__SVG_DOWN__ = """
<path style="fill:none;stroke:#{forecolor};stroke-width:2.4;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:{higopacity};stroke-miterlimit:4;stroke-dasharray:none" d="m 5.665258,3.6355811 6.33474,6.3346733 6.33474,-6.3346733" />
"""

__SVG_LEFT__ = """
<path style="fill:none;stroke:#{forecolor};stroke-width:2.4;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:{higopacity};stroke-miterlimit:4;stroke-dasharray:none" d="m 8.3644365,5.665258 -6.3346739,6.33474 6.3346739,6.33474" />
"""

__SVG_RIGHT__ = """
<path style="fill:none;stroke:#{forecolor};stroke-width:2.4;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:{higopacity};stroke-miterlimit:4;stroke-dasharray:none" d="m 3.6355811,5.6652622 6.3346733,6.3347398 -6.3346733,6.33474" />
"""

__SVG_ZOOM_IN__ = """
<path d="M18.031 16.6168L22.3137 20.8995L20.8995 22.3137L16.6168 18.031C15.0769 19.263 13.124 20 11 20C6.032 20 2 15.968 2 11C2 6.032 6.032 2 11 2C15.968 2 20 6.032 20 11C20 13.124 19.263 15.0769 18.031 16.6168ZM16.0247 15.8748C17.2475 14.6146 18 12.8956 18 11C18 7.1325 14.8675 4 11 4C7.1325 4 4 7.1325 4 11C4 14.8675 7.1325 18 11 18C12.8956 18 14.6146 17.2475 15.8748 16.0247L16.0247 15.8748ZM10 10V7H12V10H15V12H12V15H10V12H7V10H10Z" fill="#{forecolor}"></path>
"""

__SVG_ZOOM_OUT__ = """
<path d="M18.031 16.6168L22.3137 20.8995L20.8995 22.3137L16.6168 18.031C15.0769 19.263 13.124 20 11 20C6.032 20 2 15.968 2 11C2 6.032 6.032 2 11 2C15.968 2 20 6.032 20 11C20 13.124 19.263 15.0769 18.031 16.6168ZM16.0247 15.8748C17.2475 14.6146 18 12.8956 18 11C18 7.1325 14.8675 4 11 4C7.1325 4 4 7.1325 4 11C4 14.8675 7.1325 18 11 18C12.8956 18 14.6146 17.2475 15.8748 16.0247L16.0247 15.8748ZM7 10H15V12H7V10Z" fill="#{forecolor}"></path>
"""

__SVG_RESET__ = """
<path d="M12 4C9.25144 4 6.82508 5.38626 5.38443 7.5H8V9.5H2V3.5H4V5.99936C5.82381 3.57166 8.72764 2 12 2C17.5228 2 22 6.47715 22 12H20C20 7.58172 16.4183 4 12 4ZM4 12C4 16.4183 7.58172 20 12 20C14.7486 20 17.1749 18.6137 18.6156 16.5H16V14.5H22V20.5H20V18.0006C18.1762 20.4283 15.2724 22 12 22C6.47715 22 2 17.5228 2 12H4Z" fill="#{forecolor}"></path>
"""

__SVG_LAYOUT_L__ = """
<path d="M3 21C2.44772 21 2 20.5523 2 20V4C2 3.44772 2.44772 3 3 3H21C21.5523 3 22 3.44772 22 4V20C22 20.5523 21.5523 21 21 21H3ZM7 10H4V19H7V10ZM20 10H9V19H20V10ZM20 5H4V8H20V5Z" fill="#{forecolor}"></path>
"""

__SVG_LAYOUT_R__ = """
<path d="M3 21C2.44772 21 2 20.5523 2 20V4C2 3.44772 2.44772 3 3 3H21C21.5523 3 22 3.44772 22 4V20C22 20.5523 21.5523 21 21 21H3ZM15 10H4V19H15V10ZM20 10H17V19H20V10ZM20 5H4V8H20V5Z" fill="#{forecolor}"></path>
"""

__SVG_FLOAT__ = """
<path style="fill:none;stroke:#{forecolor};stroke-width:2.3;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" d="M 1.1759623,6.3462621 V 22.798078 H 17.647324 V 6.3462621 H 1.1759623" />
<path style="fill:none;stroke:#{forecolor};stroke-width:2.3;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" d="M 8.7057274,1.1756913 H 22.824037 V 15.277248" />
"""

__SVG_CLOSE__ = """
<path style="fill:none;stroke:#{forecolor};stroke-width:2.3;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" d="M 1.169074,1.1686236 22.830926,22.797538" />
<path style="fill:none;stroke:#{forecolor};stroke-width:2.3;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" d="M 22.830926,1.1686236 1.169074,22.797538" />
"""

import os
from PyQt5.QtGui import QIcon


def get_icon(name, forecolor, backcolor, higopacity, lowopacity, temp_dir, default):
    name_dict = {
        "sel_wheel": __SVG_WHEEL__,
        "sel_image": __SVG_IMAGE__,
        "sel_board": __SVG_BOARD__,
        "sel_depot": __SVG_DEPOT__,
        "wheel": __SVG_WHEEL__,
        "image": __SVG_IMAGE__,
        "board": __SVG_BOARD__,
        "depot": __SVG_DEPOT__,
        "about": __SVG_ABOUT__,
        "info": __SVG_INFO__,
        "settings": __SVG_SETTINGS__,
        "save": __SVG_SAVE__,
        "open": __SVG_OPEN__,
        "quit": __SVG_QUIT__,
        "home": __SVG_HOME__,
        "update": __SVG_UPDATE__,
        "forum": __SVG_FORUM__,
        "sel_up": __SVG_UP__,
        "sel_down": __SVG_DOWN__,
        "box_up": __SVG_UP__,
        "box_down": __SVG_DOWN__,
        "box_left": __SVG_LEFT__,
        "box_right": __SVG_RIGHT__,
        "up": __SVG_UP__,
        "down": __SVG_DOWN__,
        "left": __SVG_LEFT__,
        "right": __SVG_RIGHT__,
        "reset": __SVG_RESET__,
        "zoom_in": __SVG_ZOOM_IN__,
        "zoom_out": __SVG_ZOOM_OUT__,
        "layout_l": __SVG_LAYOUT_L__,
        "layout_r": __SVG_LAYOUT_R__,
        "float": __SVG_FLOAT__,
        "close": __SVG_CLOSE__,
    }

    wid = hig = 100
    swid = shig = 24

    if name in ("sel_wheel", "sel_image", "sel_board", "sel_depot", "wheel", "image", "board", "depot", "about", "settings",):
        swid = shig = "100"

    elif name in ("sel_up", "sel_down", "box_up", "box_down", "up", "down"):
        hig = hig / 2
        shig = shig / 2

    elif name in ("box_left", "box_right", "left", "right"):
        wid = wid / 2
        swid = swid / 2

    if os.path.isdir(temp_dir) and name in name_dict:
        with open(os.sep.join([temp_dir, "{}.svg".format(name)]), "w") as f:
            context = name_dict[name].format(forecolor=forecolor, backcolor=backcolor, stroke=6, higopacity=higopacity, lowopacity=lowopacity)
            f.write(__SVG_FMT__.format(context=context, wid=wid, hig=hig, swid=swid, shig=shig)[1:])

        return QIcon(os.sep.join([temp_dir, "{}.svg".format(name)]))
    return default
