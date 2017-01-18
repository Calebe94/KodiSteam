"""
19:02:11 T:139784625813248   ERROR: GetDirectory - Error getting
19:02:17 T:139783560996608   ERROR: EXCEPTION Thrown (PythonToCppException) : -->Python callback/script returned the following error<--
                                             - NOTE: IGNORING THIS CAN LEAD TO MEMORY LEAKS!
                                            Error Type: <type 'exceptions.ImportError'>
                                            Error Contents: No module named request
                                            Traceback (most recent call last):
                                              File "/home/calebe945/.kodi/addons/plugin.video.kodisteam/main.py", line 6, in <module>
                                                from urllib.request import urlopen
                                            ImportError: No module named request
                                            -->End of Python script error report<--
19:02:17 T:139785043280256   ERROR: GetDirectory - Error getting plugin://plugin.video.example/
19:02:17 T:139785043280256   ERROR: CGUIMediaWindow::GetDirectory(plugin://plugin.video.example/) failed
19:03:34 T:139783594567424  NOTICE: script.tv.show.next.aired: ### no prior data found
19:03:36 T:139783594567424  NOTICE: script.tv.show.next.aired: ### starting data update"""
from urllib.request import urlopen
from collections import defaultdict
from xml.dom import minidom
from lxml import etree
import xml.etree.ElementTree as ET
import xml.sax
import os

import sys
import argparse

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
            AUX_DICT.setdefault('header',[]).append({'header':header})
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
            AUX_WINE.setdefault('header',[]).append({'header':header})
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
            AUX_LINUX.setdefault('header',[]).append({'header':header})
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

""" We must open the config file and get the Steam public ID, and get the full paths to  Steam_Linux and Stem_Wine"""

tree = ET.ElementTree(file=urlopen('http://steamcommunity.com/id/calebenovequatro/games?tab=all&xml=1'))
root = tree.getroot()

LIBRARY=dict()

for game in root.iter('game'):
	#LIBRARY.setdefault('GAMES',[]).append({'name':game.find('name').text,'appID':game.find('appID').text,'logo':game.find('logo').text})
	LIBRARY.setdefault('name',[]).append({'name':game.find('name').text})
	LIBRARY.setdefault('appID',[]).append({'appID':game.find('appID').text})
	LIBRARY.setdefault('logo',[]).append({'logo':game.find('logo').text})

"""for index in range(0,len(LIBRARY['appID'])):
	print(LIBRARY['appID'][index]['appID'])"""
"""I can made this routine a module to get the installed game's appID """

STEAM_WINE = getInstalledGames(STEAM_WINE_PATH)
print("Jogos WINE:\n",STEAM_WINE['name'])

STEAM_LINUX = getInstalledGames(STEAM_LINUX_PATH)
print("Jogos LINUX:\n",STEAM_LINUX['name'])

print("Número de Jogos LINUX:",len(STEAM_LINUX['name']))
print("Número de Jogos WINE:",len(STEAM_WINE['name']))
print("Total de Jogos:",len(LIBRARY['appID']))
print("Chaves da Biblioteca:",LIBRARY.keys())
print("Chaves dos Jogos LINUX:",STEAM_LINUX.keys())
print("Chaves dos Jogos WINE:",STEAM_WINE.keys())


"""And this is the routine to search the game name with the AppID ,
and then I can build a new Dictionary with these information (Linux_GAMES,WINE_GAMES)"""

search_appID = STEAM_LINUX['appID'][1]['appID']
print("INÍCIO da PESQUISA do APPID:",search_appID)
print(getName(search_appID))



print("Aqui inicia Outro Teste!")
print("Teste com Dicionário com as seguintes chaves")
print("OWNED,WINE,LINUX")
"""
TESTE = dict()
TESTE.setdefault('OWNED',[])
TESTE.setdefault('WINE',[])
TESTE.setdefault('LINUX',[])
TESTE['OWNED']=getOwnedGames("calebenovequatro")
TESTE['WINE']=getInstalledGames_wine(STEAM_WINE_PATH)
TESTE['LINUX']=getInstalledGames_linux(STEAM_LINUX_PATH)
print("JOGOS WINE",TESTE['WINE'])
print("JOGOS LINUX",TESTE['LINUX'])
"""
VIDEOS=dict()
VIDEOS.setdefault("OWNED",[])
VIDEOS['OWNED'] = getOwnedGames("calebenovequatro")
VIDEOS.setdefault("WINE",[])
VIDEOS['WINE'] = getInstalledGames_wine(STEAM_WINE_PATH)
VIDEOS.setdefault("LINUX",[])
VIDEOS['LINUX'] = getInstalledGames_linux(STEAM_LINUX_PATH)
"""
VIDEOS = getOwnedGames("calebenovequatro")
VIDEOS = getInstalledGames_wine(STEAM_WINE_PATH)
VIDEOS = getInstalledGames_linux(STEAM_LINUX_PATH)
"""
print(VIDEOS['WINE'].keys())
TESTE = dict()
TESTE = VIDEOS['OWNED']
print(TESTE.keys())
print(TESTE['appID'][1]['appID'])
print("Numero de Jogos:",len(VIDEOS['OWNED']['appID']))
print(getName('200900'))
