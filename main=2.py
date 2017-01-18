import sys
from urllib import urlencode
from urlparse import parse_qsl
import xbmcgui
import xbmcplugin

from urllib import urlopen
import xml.etree.ElementTree as ET
import os

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])
VIDEOS = dict()
LIBRARY = dict()
GET_APP_INFO = "https://steampics-mckay.rhcloud.com/info?apps=200900&prettyprint=1"

ALL_GAMES = 'http://api.steampowered.com/ISteamApps/GetAppList/v0002/?format=xml'
LINUX_GAMES = 'https://raw.githubusercontent.com/SteamDatabase/SteamLinux/master/GAMES.json'

STEAM_WINE_PATH = "/home/calebe945/PlayOnLinux's virtual drives/calebe945/drive_c/Program Files/Steam/steamapps/"
STEAM_LINUX_PATH = "/home/calebe945/.steam/steam/steamapps/"

def getAppID(str):
	str1 = str.split('_')
	str2 = str1[1]
	str3 = str2.split('.')
	return str3[0]

def getName(search_appID):
	for appID in range(0,len(LIBRARY['appID'])):
		if search_appID == LIBRARY['appID'][appID]['appID']:
			return LIBRARY['name'][appID]['name']

def getInstalledGames(path):
    AUX_DICT=dict()
    for file in os.listdir(path):
        if file.endswith(".acf"):
            appID = getAppID(file)
            AUX_DICT.setdefault('name',[]).append({'name':getName(appID)})
            AUX_DICT.setdefault('appID',[]).append({'appID':appID})
            header = "http://cdn.edgecast.steamstatic.com/steam/apps/%s/header.jpg"%appID
            AUX_DICT.setdefault('logo',[]).append({'logo':header})
    return AUX_DICT

def getInstalledGames_wine(path):
    AUX_WINE=dict()
    for file in os.listdir(path):
        if file.endswith(".acf"):
            appID = getAppID(file)
            header = "http://cdn.edgecast.steamstatic.com/steam/apps/%s/header.jpg"%appID
            #AUX_WINE.setdefault('WINE',[]).append({'name':getName(appID),'appID':appID,'logo':header})
            AUX_WINE.setdefault('name',[]).append({'name':getName(appID)})
            AUX_WINE.setdefault('appID',[]).append({'appID':appID})
            header = "http://cdn.edgecast.steamstatic.com/steam/apps/%s/header.jpg"%appID
            AUX_WINE.setdefault('logo',[]).append({'logo':header})
    return AUX_WINE

def getInstalledGames_linux(path):
    AUX_LINUX=dict()
    for file in os.listdir(path):
        if file.endswith(".acf"):
            appID = getAppID(file)
            header = "http://cdn.edgecast.steamstatic.com/steam/apps/%s/header.jpg"%appID
            #AUX_LINUX.setdefault('LINUX',[]).append({'name':getName(appID),'appID':appID,'logo':header})
            AUX_LINUX.setdefault('name',[]).append({'name':getName(appID)})
            AUX_LINUX.setdefault('appID',[]).append({'appID':appID})
            header = "http://cdn.edgecast.steamstatic.com/steam/apps/%s/header.jpg"%appID
            AUX_LINUX.setdefault('logo',[]).append({'logo':header})
    return AUX_LINUX

def getOwnedGames(steamid):
    owned_games = "http://steamcommunity.com/id/%s/games?tab=all&xml=1"%steamid
    tree = ET.ElementTree(file=urlopen(owned_games))
    root = tree.getroot()
    
    Owned=dict()
    for game in root.iter('game'):
	    #Owned.setdefault('OWNED',[]).append({'name':game.find('name').text,'appID':game.find('appID').text,'logo':game.find('logo').text})
        Owned.setdefault('name',[]).append({'name':game.find('name').text})
        Owned.setdefault('appID',[]).append({'appID':game.find('appID').text})
        Owned.setdefault('logo',[]).append({'logo':game.find('logo').text})
    return Owned
LIBRARY.setdefault('appID',[])
VIDEOS = {'Animals': [{'name': 'Crab',
                       'thumb': 'http://www.vidsplay.com/vids/crab.jpg',
                       'video': 'http://www.vidsplay.com/vids/crab.mp4',
                       'genre': 'Animals'},
                      {'name': 'Alligator',
                       'thumb': 'http://www.vidsplay.com/vids/alligator.jpg',
                       'video': 'http://www.vidsplay.com/vids/alligator.mp4',
                       'genre': 'Animals'},
                      {'name': 'Turtle',
                       'thumb': 'http://www.vidsplay.com/vids/turtle.jpg',
                       'video': 'http://www.vidsplay.com/vids/turtle.mp4',
                       'genre': 'Animals'}
                      ],
            'Cars': [{'name': 'Postal Truck',
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


def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def get_categories():
    return VIDEOS.iterkeys()


def get_videos(category):
    return VIDEOS[category]


def list_categories():
    categories = get_categories()
    for category in categories:
        list_item = xbmcgui.ListItem(label=category)
        list_item.setArt({'thumb': VIDEOS[category][0]['thumb'],
                          'icon': VIDEOS[category][0]['thumb'],
                          'fanart': VIDEOS[category][0]['thumb']})
        list_item.setInfo('video', {'title': category, 'genre': category})
        url = get_url(action='listing', category=category)
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


def list_videos(category):
    videos = get_videos(category)
    for video in videos:
        list_item = xbmcgui.ListItem(label=video['name'])
        list_item.setInfo('video', {'title': video['name'], 'genre': video['genre']})
        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb'], 'fanart': video['thumb']})
        list_item.setProperty('IsPlayable', 'true')
        url = get_url(action='play', video=video['video'])
        is_folder = False
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


def play_video(path):
    play_item = xbmcgui.ListItem(path=path)
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    params = dict(parse_qsl(paramstring))
    if params:
        if params['action'] == 'listing':
            list_videos(params['category'])
        elif params['action'] == 'play':
            play_video(params['video'])
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        list_categories()


if __name__ == '__main__':
    router(sys.argv[2][1:])
