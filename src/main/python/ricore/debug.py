# -*- coding: utf-8 -*-

"""
Rickrack is a free software, which is distributed in the hope that it will 
be useful, but WITHOUT ANY WARRANTY. You can redistribute it and/or modify 
it under the terms of the GNU General Public License as published by the 
Free Software Foundation. See the GNU General Public License for more details.

Please visit https://github.com/eigenmiao/Rickrack for more 
infomation about Rickrack.

Copyright (c) Eigenmiao 2019-2024. All Rights Reserved.
"""


def get_sender_and_name(senders, names, idx):
    sender = ""
    name = ""

    if isinstance(idx, int):
        sid = idx // 100
        nid = idx % 100

        if sid < len(senders):
            sender = senders[sid]

        if sid < len(names) and nid < len(names[sid]):
            name = names[sid][nid]

    if not sender or not name:
        debug_error(3, "Cannot find debug index: {}".format(idx))

    return sender, name

def debug_error(idx, err):
    """
    Print Error.
    """

    senders = (
        "Main",     # 0, Main
        "Rickrack", # 1, Rickrack
        "Splash",   # 2, Splash
        "Args",     # 3, Args
        "Wheel",    # 4, Wheel
        "Image",    # 5, Image
        "Board",    # 6, Board
        "Depot",    # 7, Depot
        "Server",   # 8, Server
        "",
    )

    names = (
        (         # 0, Main

            "Debug Info Failed",             # 0
            "Import Failed",                 # 1
            "Rickrack Abnormal Exit",        # 2
            "Catch Debug Failed",            # 3
            "",

        ), (      # 1, Rickrack
            "Load Geometry Settings Failed", # 100
            "Open Input File Failed",        # 101
            "Restore Main State Failed",     # 102
            "Restore Main Geometry Failed",  # 103
            "Load Style Sheet Failed",       # 104
            "Save Settings.JSON Failed",     # 105
            "",

        ), (      # 2, Splash
            "Load Settings.JSON Failed",     # 200
            "",

        ), (      # 3, Args
            "Load User-Dirs.DIRS Failed",    # 300
            "Load Settings.JSON Failed",     # 301
            "Create User Color Dir Failed",  # 302
            "Create User Image Dir Failed",  # 303
            "Write L Settings.JSON Failed",  # 304
            "Write U Settings.JSON Failed",  # 305
            "Read Settings.JSON Failed",     # 306
            "Format Num-P in Scope Failed",  # 307
            "Format Num in Scope Failed",    # 308
            "Format Value Failed",           # 309
            "Format RGB Color Failed",       # 310
            "Format Stab Failed",            # 311
            "Remove Temporary Dir Failed",   # 312
            "",

        ), (      # 4, Wheel
            "",

        ), (      # 5, Image
            "Save Temporary Image Failed",   # 500
            "Load Temporary Image Failed",   # 501
            "Convert RGB Image Failed",      # 502
            "Convert HSV Image Failed",      # 503
            "",

        ), (      # 6, Board
            "",

        ), (      # 7, Depot
            "",

        ), (      # 8, Server
            "Init Socket Failed",            # 800
            "Text to Color Failed",          # 801
            "",
        )

    )

    sender, name = get_sender_and_name(senders, names, idx)
    tag = "ERROR" if idx < 100 else "WARNING"
    print()
    print("[> {} {:0>5d} <] ({}) {}:\n{}".format(tag, idx, sender, name, str(err)))
    print("[> TRACEBACK {:0>5d} <]".format(idx))
    print()
    import sys
    import traceback
    traceback.print_tb(sys.exc_info()[2])
    traceback.clear_frames(sys.exc_info()[2])

def debug_info(idx, value, func=None):
    """
    Print Information.
    """

    senders = (
        "Main",     # 0, Main
        "Rickrack", # 1, Rickrack
        "Splash",   # 2, Splash
        "Args",     # 3, Args
        "Wheel",    # 4, Wheel
        "Image",    # 5, Image
        "Board",    # 6, Board
        "Depot",    # 7, Depot
        "Server",   # 8, Server
        "",
    )

    names = (
        (         # 0, Main

            "",
        ), (      # 1, Rickrack

            "Resources",              # 100
            "Style Sheet File",       # 101
            "Temporary Dir",          # 102
            "Input File",             # 103
            "Args",                   # 104
            "",

        ), (      # 2, Splash
            "Args",                   # 200
            "User Settings",          # 201
            "Device Pixel Ratio",     # 202
            "Resources",              # 203
            "Display Locale",         # 204
            "Default Locale",         # 205
            "",

        ), (      # 3, Args
            "Resources",              # 300
            "Settings.JSON",          # 301
            "Info Version",           # 302
            "Info Date",              # 303
            "Args",                   # 304
            "Args",                   # 305
            "Args",                   # 306
            "Args",                   # 307
            "Args",                   # 308
            "Args",                   # 309
            "Args",                   # 310
            "Use Lang",               # 311
            "Resetall",               # 312
            "User Languages",         # 313
            "User Store Dir",         # 314
            "Document Dir name",      # 315
            "Picture Dir name",       # 316
            "User-Dirs.DIRS",         # 317
            "",

        ), (      # 4, Wheel
            "",

        ), (      # 5, Image
            "Run Category",           # 500
            "Run Args",               # 501
            "",

        ), (      # 6, Board
            "",

        ), (      # 7, Depot
            "",

        ), (      # 8, Server
            "Socket Rec Name",        # 800
            "Socket Rec Text",        # 801
            "Socket Ans Text",        # 802
            "",
        )

    )

    sender, name = get_sender_and_name(senders, names, idx)
    try:
        if func:
            print("[> INFO {:0>5d} <] ({}) {}\n{}".format(idx, sender, name, str(func(value))))

        else:
            print("[> INFO {:0>5d} <] ({}) {}\n{}".format(idx, sender, name, str(value)))

    except Exception as err:
        print("[> INFO {:0>5d} <] ({}) {} (Failed)".format(idx, sender, name))
        debug_error(0, err)

def debug_action(idx):
    """
    Print Action.
    """

    senders = (
        "Main",     # 0, Main
        "Rickrack", # 1, Rickrack
        "Splash",   # 2, Splash
        "Args",     # 3, Args
        "Wheel",    # 4, Wheel
        "Image",    # 5, Image
        "Board",    # 6, Board
        "Depot",    # 7, Depot
        "Server",   # 8, Server
        "",
    )

    names = (
        (         # 0, Main

            "Rickrack Terminated",          # 0
            "Enter Rickrack Debug Mode",    # 1
            "Start Rickrack",               # 2
            "Rickrack Finished",            # 3
            "Load Command Args",            # 4
            "Set High DPI Scaling",         # 5
            "Init PyQt",                    # 6
            "Init Splash",                  # 7
            "Init Rickrack",                # 8
            "Splash Done",                  # 9
            "Rickrack Done",                # 10
            "",

        ), (      # 1, Rickrack
            "Set Accept-Touch-Events",      # 100
            "Init Rickrack",                # 101
            "Setup Workarea",               # 102
            "Setup Rule",                   # 103
            "Setup Mode",                   # 104
            "Setup Operation",              # 105
            "Setup Script",                 # 106
            "Setup Channel",                # 107
            "Setup Transformation",         # 108
            "Init Qt Args",                 # 109
            "Setup Result",                 # 110
            "Setup Settings",               # 111
            "Setup Geometry",               # 112
            "Setup Shortkeys",              # 113
            "Init Dock Windows",            # 114
            "Init Menu Actions",            # 115
            "Init History Container",       # 116
            "Init Translations",            # 117
            "Load Work from Last Exit",     # 118
            "Load Geometry from Last Exit", # 119
            "Connect Actions",              # 120
            "Load Interface Style",         # 121
            "Rickrack Done",                # 122
            "Remove Temporary Directory",   # 123
            "Close Windows",                # 124
            "Print Final Results",          # 125
            "",

        ), (      # 2, Splash
            "Init Splash",                  # 200
            "Splash Done",                  # 201
            "",

        ), (      # 3, Args
            "Init Args",                    # 300
            "Args Done",                    # 301
            "Init Global Args",             # 302
            "",

        ), (      # 4, Wheel
            "",

        ), (      # 5, Image
            "Run Image Pro",                # 500
            "",

        ), (      # 6, Board
            "",

        ), (      # 7, Depot
            "",

        ), (      # 8, Server
            "Init Socket Server",           # 800
            "Socket Server Done",           # 801
            "",
        )

    )

    sender, name = get_sender_and_name(senders, names, idx)
    print("[> ACTION {:0>5d} <] ({}) {}".format(idx, sender, name))

def debug_free(*args, **kwargs):
    """
    Don't Print.
    """

    pass
