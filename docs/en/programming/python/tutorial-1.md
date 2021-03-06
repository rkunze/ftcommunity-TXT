---
nav-title: The First App
nav-pos: 1
---
# Programming in Python: The First App

Warning: This tutorial is outdated and needs to be updated!

This tutorial is meant to give a basic introduction on how an application
for the Community Firmware of the Fischertechnik TXT controller is being
written.

An app consists of at least three files:

 * The application program (executable) itself. This is typically a
   python script. But it could equally well be a native binary or a
   script in any other language supported by the TXT. Since
   [python](https://www.python.org) has become the de-facto standard
   for software written for the TXT this tutorial will also use the
   python language

 * A manifest file. This is a small text file containing additonal
   information about the App like its display name, its author and the
   name of the executable.

 * A icon. This should be a 64x64 pixel PNG file which is being used
   in the launcher as well as the web interface.

## The application program

The application program can be any script or binary the TXT is able to
execute. Since apps are usually started from the TXTs launcher on the
user will expect some output on the screen. Thus the program should include
a minimalistic GUI.

Currently all apps use the [Qt Toolkit](http://www.qt.io/) for their user
interface. We'll thus also use Qt. A minimal python application opening
a TXT styled window looks like this:

```
#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
import sys
from TxtStyle import *

class FtcGuiApplication(TxtApplication):
    def __init__(self, args):
        TxtApplication.__init__(self, args)

        # create the empty main window
        w = TxtWindow("Test")
        w.show()
        self.exec_()        

if __name__ == "__main__":
    FtcGuiApplication(sys.argv)
```

Please save this file under the name [`test.py`](https://raw.githubusercontent.com/ftCommunity/ftcommunity-apps/master/packages/app_tutorial_1/test.py)

This app subclasses the TxtApplication class which was imported from
TxtStyle. It creates a window labeled "Test", shows that window and
hands over execution to the window so it can interact with the user
until it's closed.

## The manifest

The manifest file is a simple text file containing various fields
describing the app.

```
[app]
name: Test
category: Tests
author: Joe Developer
icon: icon.png
desc: TXT app tutorial #1
url: https://github.com/ftCommunity/ftcommunity-TXT/wiki/FTC-FW-App-Tutorial-1
exec: test.py
managed: yes
uuid: 191fe5a6-313b-4083-af65-d1ad7fd6d281
version: 1.0
firmware: 0.9
```

The mandatory fields are name, icon, desc, exec, uuid and managed.

 * **name** is the display name of the app as used e.g. in the
   launcher. It should be short enough to fit below the icon.
 * **icon** is name of the icon file. This is usually `icon.png`
 * **desc** is a short description of the app. This is currently
   only used in the web interface
 * **exec** is the name of the executable. In this example it refers
   to our test.py python script.
 * **uuid** is a unique id used to identify this app. You can generate
   one for your app e.g. online with services like [this](https://www.famkruithof.net/uuid/uuidgen). The uuid identifies an app, so all versions of an app must use the same uuid. The uuid is also used to generate the apps unique directory on the TXT.
 * **managed** is currently unused and should be set to yes. This tells
   the launcher that the app has a Qt GUI. In the future this will
   allow the launcher to support apps using a different GUI toolkit.
 * **version** is the current version number of this app.
 * **firmware** is the firmware version number this app has been tested for. Currently only 0.9 exists. Later this will allow ranges like 0.9-1.1

Some optional fields are also used:

 * **category** is used to group apps in the launcher
 * **author** gives information about the developer of this app
 * **url** can be used to link to a web page. This will then be
   acccesible through the TXTs web interface
 * **set** optionally refers to the Fischertechnik set related to a model the app can be used for. E.g. `524328 ROBOTICS TXT Discovery Set`
 * **model** optionally refers to the english model name from the set. E.g. `Pedestrian Light`

The **set** and **model** entries are currently unused but may be used in the future to allow the user to find apps relating to a specific model he e.g. just built.

Please save this file under the name [`manifest`](https://raw.githubusercontent.com/ftCommunity/ftcommunity-apps/master/packages/app_tutorial_1/manifest)

# The icon

The icon can be any file in JPG or PNG format. It should be 64x64 pixels in
size.

![icon.png](https://raw.githubusercontent.com/ftCommunity/ftcommunity-apps/master/packages/app_tutorial_1/icon.png)

An example file can be found at [here](https://raw.githubusercontent.com/ftCommunity/ftcommunity-apps/master/packages/app_tutorial_1/icon.png)

This icon has been created using the [Inkscape](https://inkscape.org/) but most other paint programs will also do. The inkscape SVG file for this icon is also available [here](https://raw.githubusercontent.com/ftCommunity/ftcommunity-apps/master/packages/app_tutorial_1/icon.svg)

# Package it up

Now we have the three mandatory files

 * `test.py` the app programm code itself
 * `manifest` the text file describing the app
 * `icon.png` the icon for the launcher

To get these installed on the TXT they'll need to be put into a ZIP
archive. Any program like WinZIP should work. All three files should be
in the toplevel of the ZIP and not e.g. in some subfolder.

A prepared archive of our little demo app is also [available](https://github.com/ftCommunity/ftcommunity-apps/raw/master/packages/app_tutorial_1.zip)

# Upload it to the TXT

Now use your PC's web browser to connect to the TXT. The main web page will
show all installed apps:

![tut1_img1.jpg](tut1_img1.jpg)

Use the file dialog to select our test.zip archive and hit upload:

![tut1_img2.jpg](tut1_img2.jpg)

The app is now being intalled on the TXT and becomes visible in the
TXTs launcher:

![tut1_img6.jpg](tut1_img6.jpg)

The app can be launched like any other app by clicking it:

![tut1_img4.jpg](tut1_img4.jpg)

It's now also visible in the web interface:

![tut1_img3.jpg](tut1_img3.jpg)

Selecting it shows some of the details from the manifest file:

![tut1_img5.jpg](tut1_img5.jpg)

The app can also be deleted from there.

Continue reading [Programming Python: Development](tutorial-2.md)
