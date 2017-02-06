from subprocess import Popen,PIPE,call

from urllib import urlopen,urlencode
from urlparse import parse_qsl

import sys,os,json,time
import xml.etree.ElementTree as ET

def scan_for_next_token(f):
    while True:
        byte = f.read(1)
        if byte == '':
            raise EOFError
        if not byte.isspace():
            return byte

def parse_quoted_token(f):
    ret = ''
    while True:
        byte = f.read(1)
        if byte == '':
            raise EOFError
        if byte == '"':
            return ret
        ret += byte

class AcfNode(dict):
    def __init__(self, f):
        while True:
            try:
                token_type = scan_for_next_token(f)
            except EOFError:
                return
            if token_type == '}':
                return
            if token_type != '"':
                raise TypeError('Error parsing ACF format - missing node name?')
            name = parse_quoted_token(f)

            token_type = scan_for_next_token(f)
            if token_type == '"':
                self[name] = parse_quoted_token(f)
            elif token_type == '{':
                self[name] = AcfNode(f)
            else:
                assert(False)

def parse_acf(filename):
    with open(filename, 'r') as f:
        return AcfNode(f)

class SteamAPI(object):
    WINE_PATH=str()
    LINUX_PATH=str()
    PUBLIC_ID=str()
    #GET_APP_INFO = "https://steampics-mckay.rhcloud.com/info?apps=200900&prettyprint=1"
    ALL_GAMES = 'http://api.steampowered.com/ISteamApps/GetAppList/v0002/?format=xml'
    LINUX_GAMES = 'https://raw.githubusercontent.com/SteamDatabase/SteamLinux/master/GAMES.json'
    
    LIBRARY=dict()
    profilefolder=str()
    LIBRARY.setdefault("LIBRARY",[])
    LIBRARY.setdefault("WINE",[])
    LIBRARY.setdefault("LINUX",[])
    
    def __init__(self,wine,public_id,profiles_folder):
        #Verification is did outside
        profilefolder = profiles_folder
        self.LINUX_PATH=os.getenv('HOME')+"/.steam/steam/"
        self.WINE_PATH=wine
        self.PUBLIC_ID=public_id
        self.LIBRARY["LIBRARY"] = self.getOwnedGames()
        self.LIBRARY["WINE"] = self.getInstalledGames()
        self.LIBRARY["LINUX"] = self.getInstalledGames()
    
    def linux(self,command):
        logfile = open(os.getenv("HOME")+"/_linux_.log","a")
        pid = os.fork()
        steam = pgrep("Steam.exe")
        if(steam):
            os.system("wine %sSteam.exe -shutdown"%(self.path2UNIX(self.WINE_PATH)))
            while(pgrep("Steam.exe")):
                time.sleep(1)
        if pid == 0:
            # PIPE : stderr > stdout > logfile
            os.dup2(logfile.fileno(),1)
            os.dup2(1,2)
            os.system("steam -applaunch %s -silent"%command)
            time.sleep(5)
            #sys.exit("Another Running Game: AppID:%s - Time"%command)
            
    def wine(self,command):
        logfile = open(os.getenv("HOME")+"/_wine_.log","a")
        pid = os.fork()
        steam = pgrep("steam")
        if(steam):
            os.system("steam -shutdown")
            while(pgrep("steam")):
                    time.sleep(1)
        if pid == 0:
            # PIPE : stderr > stdout > logfile
            os.dup2(logfile.fileno(),1)
            os.dup2(1,2)
            os.system("wine %sSteam.exe -applaunch %s -silent"%(self.path2UNIX(self.WINE_PATH),command))
            time.sleep(5)
            #sys.exit("Another Running Game: AppID:%s - Time"%command)
    #def isInstalled(appID):
    def getInstalledGames(self):
        AUX = dict()
        """
        AUX['linux']=dict()
        AUX['windows']=dict()
        if os.exists(profiles_folder+"/"+self.PUBLIC_ID+"_installed.xml"):
            #Get Info of the xml file
            for get all games:
            if get platform is "windows":
                AUX[platform] = 
        else:
            #continue to the following profile
        """
        client_wine = self.WINE_PATH + "steamapps/"
        client_linux = self.LINUX_PATH + "steamapps/"
        my_list ={"linux":client_linux,"windows":client_wine}
    
        for client in my_list:
            for file in os.listdir(my_list[client]):
                if file.endswith(".acf"):
                    acf=parse_acf(my_list[client]+file)
                    AUX.setdefault('name',[]).append({'name':acf['AppState']['name']})
                    AUX.setdefault('appID',[]).append({'appID':acf['AppState']['appid']})
                    header = "http://cdn.edgecast.steamstatic.com/steam/apps/%s/header.jpg"%acf['AppState']['appid']
                    AUX.setdefault('logo',[]).append({'logo':header})
                    AUX.setdefault('platform',[]).append({"platform":client})
        return AUX

    def getOwnedGames(self):
        
        owned_games = "http://steamcommunity.com/id/%s/games?tab=all&xml=1"%self.PUBLIC_ID
        tree=ET.ElementTree(file=urlopen(owned_games))
        root = tree.getroot()
        Owned = dict()
        
        for game in root.iter('game'):
            Owned.setdefault('name',[]).append({'name':game.find('name').text})
            Owned.setdefault('appID',[]).append({'appID':game.find('appID').text})
            Owned.setdefault('logo',[]).append({'logo':game.find('logo').text})
            Owned.setdefault('platform',[]).append({'platform':"not installed"})
        return Owned
        
    def path2UNIX(self,path):
        aux=str()
        for index in range(0,len(path)):
            if path[index] == '\'':
                aux=aux+'\\'
            elif path[index] == ' ':
                aux=aux+'\\'
            aux=aux+path[index]
            index=index+1
        return aux

def pgrep(pattern):
    pid=str()
    process = Popen(['pgrep',pattern],stdout=PIPE,stderr=PIPE)
    out = str(process.communicate()).split()
    
    if out is not None:
        for digit in out[0]:
            if digit.isdigit():
                pid=pid+digit
    return pid

"""The wine() and linux() function inside the API class will return game's launching name... For that we will need to parse the game's info from the follow URL:
https://steampics-mckay.rhcloud.com/info?apps=<appID>&prettyprint=1

and then get some info from the game:
    from common:
        *name;
        *logo;
        *icon;
        *oslist;
        *controller_support;
    from extended:
        *gamedir;
        *validoslist;
        *pablisher;
    from config/launch;
        will be hard to get info from this key.
        *executable

"""
