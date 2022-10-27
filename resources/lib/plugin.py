# -*- coding: utf-8 -*-
import routing
import os
import xbmcaddon
import xbmcvfs
import xbmc
import time
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory


ADDON = xbmcaddon.Addon()
plugin = routing.Plugin()

addon_path = ADDON.getAddonInfo("path")
addon_profile = ADDON.getAddonInfo("profile")

IMAGE_1 = os.path.join(addon_path, "resources", "images", "kodilogotransparent.png")
IMAGE_2 = os.path.join(addon_path, "resources", "images", "matrixbackground.png")

@plugin.route('/')
def root():

    # Add icon 1 listitem
    liz = ListItem("[B]Image 1[/B] - Kodi logo transparent")
    liz.setArt({
        "thumb": IMAGE_1
    })
    addDirectoryItem(
        plugin.handle,
        IMAGE_1,
        liz
    )

    # Add icon 2 listitem
    liz = ListItem("[B]Image 2[/B] - Matrix background")
    liz.setArt({
        "thumb": IMAGE_2
    })
    addDirectoryItem(
        plugin.handle,
        IMAGE_2,
        liz
    )

    # merge both icons using PIL
    IMAGE_3 = mergeimages(IMAGE_1, IMAGE_2)

    # finally add the image 3 (result from merging img 1 and img 2)
    liz = ListItem("[B]Image 3[/B] - Merged with PIL")
    liz.setArt({
        "thumb": IMAGE_3
    })
    addDirectoryItem(
        plugin.handle,
        IMAGE_3,
        liz
    )

    endOfDirectory(plugin.handle)


def mergeimages(img1, img2):
    if not os.path.exists(addon_profile):
        xbmcvfs.mkdirs(addon_profile)

    # generate image (PIL block)
    from PIL import Image
    kodilogo = Image.open(img1)
    background = Image.open(img2)
    background.paste(kodilogo, (0, 0), kodilogo)

    # save to profile folder
    final_path = os.path.join(xbmcvfs.translatePath(addon_profile), "img%s.png" % time.time())
    background.save(final_path, "PNG")
    return final_path


def run():
	plugin.run()
