import SteamAPI
from urlparse import parse_qsl
from urllib import urlencode
import xbmcgui,xbmcplugin,xbmcaddon,xbmc,xbmcvfs
import os

_url = sys.argv[0]
_handle = int(sys.argv[1])

def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def categories(categories):
    DEBUG = open("/home/calebe945/KODISTEAM.dbg",'w')
    command = os.getcwd()
    DEBUG.write(command)
    DEBUG.close()
    for category in categories.iterkeys():
        list_item=xbmcgui.ListItem(label=category)
        list_item.setArt({'thumb':categories[category]["logo"][0]["logo"],'icon':categories[category]["logo"][0]["logo"],'fanart':categories[category]["logo"][0]["logo"]})
        list_item.setInfo('video',{'title':category,'genre':category})
        xbmcplugin.addDirectoryItem(_handle,get_url(action='listing', category=category),list_item,True)
    xbmcplugin.addSortMethod(_handle,xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)
    
    
def list_games(steam,categories):
    games = steam.LIBRARY[categories]
    for game in range(0,len(games['name'])):
        list_item = xbmcgui.ListItem(label=games['name'][game]['name'])
        list_item.setInfo('video', {'title': games['name'][game]['name'], 'genre': games['appID'][game]['appID']})
        list_item.setArt({'thumb':games['logo'][game]['logo'],'icon':games['logo'][game]['logo'],'fanart':games['logo'][game]['logo']})
        xbmcplugin.addDirectoryItem(_handle,get_url(action='play',category=categories,game=games['appID'][game]['appID']),list_item,False)
    xbmcplugin.addSortMethod(_handle,xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)
    
def main(paramstring):
    params = dict(parse_qsl(paramstring))
    # First of all I need to Verify the settings before put it into the class
    #_settings = xbmcaddon.Addon(id="plugin.video.kodisteam")
    _settings = xbmcaddon.Addon()
    dialog = xbmcgui.DialogProgress()
    dialog.create("Xteam... Iniciando o Cliente!","Carregando Biblioteca")
    addonID = _settings.getAddonInfo('id')
    addonPath = _settings.getAddonInfo('path')
    userdata = xbmc.translatePath('special://profile/addon_data/'+addonID)
    profilesFolder = os.path.join(userdata,"profiles")
    #Parsing Folders
    if not os.path.isdir(userdata):
        os.mkdir(userdata)
    if not os.path.isdir(profilesFolder):
        os.mkdir(profilesFolder)
    WINE = _settings.getSetting("steam_wine")
    steamID = _settings.getSetting("steam_id")
    steam = SteamAPI.SteamAPI(WINE,steamID)
    dialog.close()
    
    if params:
        if params['action'] == 'listing':
            list_games(steam,params['category'])
        elif params['action'] == 'play':
            if params['category'] == "LINUX":
                steam.linux(params['game'])
            elif params['category'] == "WINE":
                steam.wine(params['game'])
            else:
                list_games(steam,params['category'])
        else:
            raise ValueError("Invalid Paramstring:{0}!".format(paramstring))
    else:
        categories(steam.LIBRARY)

if __name__ == "__main__":
    main(sys.argv[2][1:])
