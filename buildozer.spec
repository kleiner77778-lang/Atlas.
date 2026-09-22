[app]

# (str) Title of your application
title = Atlas E-Lkw Tracker

# (str) Package name
package.name = elkwtracker

# (str) Package domain (needed for android packaging)
package.domain = org.elkw

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning
version = 1.0.0

# Abgestimmte Requirements: Keine externen C-Bibliotheken
requirements = python3,kivy==2.2.1,pyjnius

# Icon-Einbindung (muss als icon.png im Ordner liegen)
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (bool) Accept SDK license automatically
android.accept_sdk_license = True

# (list) The Android archs to build for
android.archs = arm64-v8a

[buildozer]

# (int) Log level
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
