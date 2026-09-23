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

# (list) Application requirements
# Schlank gehalten: urllib aus der Python-Standardbibliothek wird in main.py genutzt
requirements = python3,kivy==2.2.1,pyjnius

# (str) Custom source folders for requirements
p4a.branch = master

# (str) Custom application icon (falls nicht vorhanden, bleibt die Zeile auskommentiert)
# icon.filename = %(source.dir)s/icon.png

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 1

# (list) Permissions
permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, FOREGROUND_SERVICE

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (bool) Skip update of Android SDK
android.skip_update = False

# (bool) Automatically accept SDK licenses
android.accept_sdk_license = True

# (str) Android architecture
android.archs = arm64-v8a


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
