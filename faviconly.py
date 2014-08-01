import os
import PIL.Image # sudo pip install pillow
# PIL (pillow) is needed to convert ICO to PNG

# Enumerate all "*.desktop" files in and below user's directory (or in ~/Desktop and below) 
# Look at the lines:
#   Type=Link  ('Link' must be present)
#   URL=https://news.ycombinator.com/blabla  (to derive favico.ico location from)
#   Icon=/home/user/.cache/favicon/news.ycombinator.com.png (this program should set this)
import ConfigParser
import urlparse


def process(fn):
    # Read the .desktop file, in INI format.
    config = ConfigParser.RawConfigParser()
    config.optionxform = str
    config.read(fn)

    # See if the .desktop file contains the right section.
    try:
        shortcuttype = config.get("Desktop Entry", "Type")
    except ConfigParser.NoSectionError:
        shortcuttype = ""

    # Only process web links desktop shortcuts.
    if shortcuttype != "Link":
        return 

    # See if there's already an 'Icon' value defined.
    try:
        iconfn = config.get("Desktop Entry", "Icon")
    except ConfigParser.NoOptionError:
        iconfn = ""

    # Check for a symbolic name, like "mate-fs-bookmark" for example.
    if iconfn and not "/" in iconfn:
        return 

    # The Icon value is probably a filename. See if it already represents a valid image file.
    if os.path.exists(iconfn):
        img = PIL.Image.open(iconfn)
        w, h = img.size
        if w > 0 and h > 0:
            return # Icon is already referring to a valid picture
    # TODO: Catch image loading errors, in case Icon is a filename isn't a loadable image.
    
    url = config.get("Desktop Entry", "URL")
    components = urlparse.urlparse(url)
    faviconurl = components.scheme + "://" + components.netloc + "/favicon.ico" # TODO: https -> http ?
    print faviconurl

    f = open(fn + ".new.desktop", "w")
    config.write(f)
    


homedir = os.path.expanduser("~")
rootdir = os.path.join(homedir, "Desktop")
for dirname, subdirnames, filenames in os.walk(rootdir):
    for filename in filenames:
        fullfilename = os.path.join(dirname, filename)
        if fullfilename.endswith(".desktop"):
            process(fullfilename)

# TODO: Download ICO from website
img = PIL.Image.open(os.path.join(homedir, ".cache", "favicon", "news.ycombinator.com.ico"))
img.save(os.path.join(homedir, ".cache", "favicon", "news.ycombinator.com.png"))
# TODO: Refresh desktop
