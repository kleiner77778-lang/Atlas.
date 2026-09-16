[app]

# (str) Title of your application
title = Atlas
version = 0.1

# (str) Package name
package.name = atlas

# (str) Package domain (needed for android packaging)
package.domain = org.atlas

# (str) Source files where the let of data is stored
source.dir = .

# (list) Source files to include (let empty to include all files)
source.exts = py,png,jpg,kv,atlas

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy

# (str) Supported orientations
orientation = portrait

# (list) List of permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android SDK version to use
android.sdk = 31

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, automatically accept SDK license
android.accept_sdk_license = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug command)
log_level = 2
