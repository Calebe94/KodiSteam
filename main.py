# -*- coding: utf-8 -*-
# Module: default
# Author: Roman V. M.
# Created on: 28.11.2014
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
from urllib.request import urlopen
from collections import defaultdict
from xml.dom import minidom
from lxml import etree
import xml.etree.ElementTree as ET
import xml.sax
import os

import argparse

import sys
import urllib
from urllib.parse import parse_qsl
import xbmcgui
import xbmcplugin

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

# Free sample videos are provided by www.vidsplay.com
# Here we use a fixed set of properties simply for demonstrating purposes
# In a "real life" plugin you will need to get info and links to video files/streams
# from some web-site or online service.
def getAppID(str):
	str1 = str.split('_')
	str2 = str1[1]
	str3 = str2.split('.')
	return str3[0]

def getName(search_appID):
	for appID in range(0,len(LIBRARY['appID'])):
		if search_appID == LIBRARY['appID'][appID]['appID']:
			return LIBRARY['name'][appID]['name']


def getInstalledGames_wine(path):
    AUX_WINE=dict()
    for file in os.listdir(path):
        if file.endswith(".acf"):
            appID = getAppID(file)
            header = "http://cdn.edgecast.steamstatic.com/steam/apps/%s/header.jpg"%appID
            AUX_WINE.setdefault('WINE',[]).append({'name':getName(appID),'appID':appID,'thumb':header})
            """AUX_DICT.setdefault('name',[]).append({'name':getName(appID)})
            AUX_DICT.setdefault('appID',[]).append({'appID':appID})
            header = "http://cdn.edgecast.steamstatic.com/steam/apps/%s/header.jpg"%appID
            AUX_DICT.setdefault('header',[]).append({'header':header})"""
    return AUX_WINE

def getInstalledGames_linux(path):
    AUX_LINUX=dict()
    for file in os.listdir(path):
        if file.endswith(".acf"):
            appID = getAppID(file)
            header = "http://cdn.edgecast.steamstatic.com/steam/apps/%s/header.jpg"%appID
            AUX_LINUX.setdefault('LINUX',[]).append({'name':getName(appID),'appID':appID,'thumb':header})
            """AUX_DICT.setdefault('name',[]).append({'name':getName(appID)})
            AUX_DICT.setdefault('appID',[]).append({'appID':appID})
            header = "http://cdn.edgecast.steamstatic.com/steam/apps/%s/header.jpg"%appID
            AUX_DICT.setdefault('header',[]).append({'header':header})"""
    return AUX_LINUX

def getOwnedGames(steamid):
    owned_games = "http://steamcommunity.com/id/%s/games?tab=all&xml=1"%steamid
    tree = ET.ElementTree(file=urlopen(owned_games))
    root = tree.getroot()
    
    Owned=dict()
    for game in root.iter('game'):
	    Owned.setdefault('OWNED',[]).append({'name':game.find('name').text,'appID':game.find('appID').text,'thumb':game.find('logo').text})
    return Owned


VIDEOS = dict()
VIDEOS.setdefault('OWNED',[])
VIDEOS.setdefault('WINE',[])
VIDEOS.setdefault('LINUX',[])
VIDEOS['OWNED']=getOwnedGames("calebenovequatro")
VIDEOS['WINE']=getInstalledGames_wine(STEAM_WINE_PATH)
VIDEOS['LINUX']=getInstalledGames_linux(STEAM_LINUX_PATH)
"""
VIDEOS = {'Steam_LINUX': [{'name': 'Cave Story+',
                       'thumb': 'http://cdn.akamai.steamstatic.com/steamcommunity/public/images/apps/200900/a242e0465a65ffafbf75eeb521812fb575990a33.jpg',
                       'video': 'http://www.vidsplay.com/vids/crab.mp4',
                       'genre': 'Action'},
                      {'name': 'Castle of Illusion',
                       'thumb': 'http://cdn.akamai.steamstatic.com/steamcommunity/public/images/apps/227600/cdbc2581c46fa378baa8f48e28513a1668b30941.jpg',
                       'video': 'http://www.vidsplay.com/vids/alligator.mp4',
                       'genre': 'Action'},
                      {'name': 'Black Mesa',
                       'thumb': 'http://cdn.akamai.steamstatic.com/steamcommunity/public/images/apps/362890/07165fb02e18a4cf544125c1bd350fe300aef362.jpg',
                       'video': 'http://www.vidsplay.com/vids/turtle.mp4',
                       'genre': 'Action'}
                      ],
            'Steam_WINE': [{'name': 'Postal Truck',
                      'thumb': 'http://www.vidsplay.com/vids/us_postal.jpg',
                      'video': 'http://www.vidsplay.com/vids/us_postal.mp4',
                      'genre': 'Cars'},
                     {'name': 'Traffic',
                      'thumb': 'http://www.vidsplay.com/vids/traffic1.jpg',
                      'video': 'http://www.vidsplay.com/vids/traffic1.avi',
                      'genre': 'Cars'},
                     {'name': 'Traffic Arrows',
                      'thumb': 'http://www.vidsplay.com/vids/traffic_arrows.jpg',
                      'video': 'http://www.vidsplay.com/vids/traffic_arrows.mp4',
                      'genre': 'Cars'}
                     ],
            'Food': [{'name': 'Chicken',
                      'thumb': 'http://www.vidsplay.com/vids/chicken.jpg',
                      'video': 'http://www.vidsplay.com/vids/bbqchicken.mp4',
                      'genre': 'Food'},
                     {'name': 'Hamburger',
                      'thumb': 'http://www.vidsplay.com/vids/hamburger.jpg',
                      'video': 'http://www.vidsplay.com/vids/hamburger.mp4',
                      'genre': 'Food'},
                     {'name': 'Pizza',
                      'thumb': 'http://www.vidsplay.com/vids/pizza.jpg',
                      'video': 'http://www.vidsplay.com/vids/pizza.mp4',
                      'genre': 'Food'}
                     ]}
"""

def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :type kwargs: dict
    :return: plugin call URL
    :rtype: str
    """
    return '{0}?{1}'.format(_url, urllib.urlencode(kwargs))


def get_categories():
    """
    Get the list of video categories.

    Here you can insert some parsing code that retrieves
    the list of video categories (e.g. 'Movies', 'TV-shows', 'Documentaries' etc.)
    from some site or server.

    .. note:: Consider using `generator functions <https://wiki.python.org/moin/Generators>`_
        instead of returning lists.

    :return: The list of video categories
    :rtype: list
    """
    return VIDEOS.iterkeys()


def get_videos(category):
    """
    Get the list of videofiles/streams.

    Here you can insert some parsing code that retrieves
    the list of video streams in the given category from some site or server.

    .. note:: Consider using `generators functions <https://wiki.python.org/moin/Generators>`_
        instead of returning lists.

    :param category: Category name
    :type category: str
    :return: the list of videos in the category
    :rtype: list
    """
    return VIDEOS[category]


def list_categories():
    """
    Create the list of video categories in the Kodi interface.
    """
    # Get video categories
    categories = get_categories()
    # Iterate through categories
    for category in categories:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category)
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': VIDEOS[category][0]['thumb'],
                          'icon': VIDEOS[category][0]['thumb'],
                          'fanart': VIDEOS[category][0]['thumb']})
        # Set additional info for the list item.
        # Here we use a category name for both properties for for simplicity's sake.
        # setInfo allows to set various information for an item.
        # For available properties see the following link:
        # http://mirrors.xbmc.org/docs/python-docs/15.x-isengard/xbmcgui.html#ListItem-setInfo
        list_item.setInfo('video', {'title': category, 'genre': category})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action='listing', category=category)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def list_videos(category):
    """
    Create the list of playable videos in the Kodi interface.

    :param category: Category name
    :type category: str
    """
    # Get the list of videos in the category.
    videos = get_videos(category)
    # Iterate through videos.
    for video in videos:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=video['name'])
        # Set additional info for the list item.
        list_item.setInfo('video', {'title': video['name'], 'genre': video['genre']})
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb'], 'fanart': video['thumb']})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/vids/crab.mp4
        url = get_url(action='play', video=video['video'])
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def play_video(path):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    params = dict(parse_qsl(paramstring))
    if params:
        if params['action'] == 'listing':
            list_videos(params['category'])

        elif params['action'] == 'play':
            print("Has Member")
        else:
            #raise ValueError("Invalid Paramstring:{0}!".format(paramstring))
            list_categories()
    else:   
        list_categories()

def main():
    """Here comes my main function, that will do what I want"""

if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
