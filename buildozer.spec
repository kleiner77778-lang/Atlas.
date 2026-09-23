[app]

# (str) Title of your application
title = Atlas

# (str) Package name
package.name = elkwtracker

# (str) Package domain (needed for android packaging)
package.domain = org.elkw

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (process one by one)
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
# pyjnius ist hier exakt richtig geschrieben und sichert die Java-Schnittstelle ab
requirements = python3,kivy==2.2.1,pyjnius

# (str) Custom source folders for requirements
# Allows to feed custom source code to python-for-android
p4a.branch = master

# (list) Permissions
permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, FOREGROUND_SERVICE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip trying to update the android sdk
android.skip_update = False

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) The Android arch to build for
android.archs = arm64-v8a

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Orientation
orientation = portrait


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = disable, 1 = enable)
warn_on_root = 1
