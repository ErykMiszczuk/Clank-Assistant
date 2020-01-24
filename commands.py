import webbrowser
import os
import re
import ctypes
import getpass
import requests
import psutil
from bs4 import BeautifulSoup
import time
import subprocess

import patterns


username = getpass.getuser()
homeDir = os.path.expanduser('~\\')
homeMusicDir = homeDir + 'Music/'
homePicturesDir = homeDir + 'Pictures/'


def openWebsite(website, openMode = ''):
    if openMode == 'NEW_TAB':
        webbrowser.open_new_tab(website)
    elif openMode == 'NEW_WINDOW':
        webbrowser.open_new(website)
    else:
        webbrowser.open(website)


def openYoutube(openMode = ''):
    url = r'https://www.youtube.com/'
    openWebsite(url, openMode)


def openYoutubeWithSearch(searchQuery, openMode = ''):
    print(searchQuery)
    url = f'https://www.youtube.com/results?search_query={searchQuery}'
    openWebsite(url, openMode)


def openGoogleWithSearch(searchQuery, openMode = ''):
    url = f'https://www.google.com/search?q={searchQuery}'
    openWebsite(url, openMode)


def openFileInExternalProgram(path):
    if os.path.exists:
        os.startfile(path)
    else:
        print("File did not exists") # Ask user if he want to create file


def playMusic(path):
    if os.path.exists(path):
        elementsInDir = os.listdir(path)
        music = list(filter(filterMP3, elementsInDir))
        os.startfile(path + music[0])
    else:
        print("Directory Music did not exists in home directory")


def downloadWallpaperFromWallhaven(searchPhrase):
    baseUrl = 'https://wallhaven.cc'
    # https://wallhaven.cc/search?q=cara&categories=111&purity=110&sorting=relevance&order=desc&page=4
    searchParam = r'/search?q=' + str(searchPhrase)
    general = '1'
    anime = '1'
    people = '1'
    categories = '&categories=' + general + anime + people
    swf = '1'
    sketchy = '0'
    nsfw = '0' # this last one is not used currently so i presume i could be for far more explicit content
    purity = '&purity=' + swf + sketchy + nsfw
    page = str(1)
    url = baseUrl + searchParam + categories + purity + '&sorting=relevance&order=desc&page=' + page

    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'}
    listOfWallpapersPageHtml = requests.get(url, headers=headers)

    listOfWallpapersPage = BeautifulSoup(listOfWallpapersPageHtml.content, 'html.parser')
    # print(wallpapersPage.select('section.thumb-listing-page'))
    # here i can download thumbnails of all wallpapers on page and display them to user in graphical user interface
    wallpapersLinks = listOfWallpapersPage.select('a.preview')

    time.sleep(2)
    
    print(wallpapersLinks[0]['href'])
    wallpaperPageHtml = requests.get(wallpapersLinks[0]['href'], headers=headers)
    wallpaperPage = BeautifulSoup(wallpaperPageHtml.content, 'html.parser')
    wallpaper = wallpaperPage.find(id='wallpaper')
    title = wallpaper['alt']
    src = wallpaper['src']
    file, extension = os.path.splitext(src)
    print(src, title, extension)
    file = requests.get(src)
    wallpaperPath = homePicturesDir + title + extension
    open(wallpaperPath, 'wb').write(file.content)
    
    setWallpaper(wallpaperPath)


def getNorrisJoke():
    # jokes provaided by api.chucknorris.io
    url = 'https://api.chucknorris.io/jokes/random'
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'}
    response = requests.get(url, headers=headers)
    joke = response.json()
    print(joke['value'])

def filterMP3(filename):
    if patterns.music.match(filename):
        return True
    else:
        return False


def tellOption(tokens):
    # print(tokens)
    for i, token in enumerate(tokens):
        if str(token[0]).lower() == 'joke':
            getNorrisJoke()

def find(tokens):
    # print(tokens)
    for i, token in enumerate(tokens):
        # print(i)
        if str(token[0]).lower() == 'about':
            findTarget = tokens[i + 1:]
            words, pos_tags = zip(*findTarget)
            target = ' '.join(words)
            print('Finding information about {}'.format(target))
            openYoutubeWithSearch(target)


def play(tokens):
    # print('PLAY')
    sizeOfTokens = len(tokens)
    for i, token in enumerate(tokens):
        if str(token[0]).lower() == 'music' and i == (sizeOfTokens - 1):
            playMusic(homeMusicDir) 
        elif token[0] == "on":
            musicSource = tokens[i + 1]
            if patterns.youtube.match(musicSource[0]):
                words, pos_tags = zip(*tokens)
                start = words.index('play')
                # end = words.index('on')
                dest = words[start+1:i]
                query = ' '.join(dest)
                # print(query)
                openYoutubeWithSearch(query)


def setWallpaper(path):
    if os.path.exists(path):
        ctypes.windll.user32.SystemParametersInfoW(20, 0 , str(path), 0)
    else:
        print("File did not exists")


def setOption(tokens):
    print(tokens)
    for i, token in enumerate(tokens):
        if str(token[0]).lower() == 'wallpaper':
            words, pos_tags = zip(*tokens)
            start = words.index('set')
            end = words.index('wallpaper')
            query = ' '.join(words[start+1:end-1])
            print(query)
            downloadWallpaperFromWallhaven(query)
        elif str(token[0]).lower() == 'background':
            words, pos_tags = zip(*tokens)
            start = words.index('set')
            end = words.index('background')
            query = ' '.join(words[start+1:end-1])
            print(query)
            downloadWallpaperFromWallhaven(query)

def exitExternalProgram(tokens):
    print(tokens)
    for i, token in enumerate(tokens):
        if str(token[0]).lower() == 'exit':
            programName = tokens[i+1][0]
            print(programName)
            for process in (process for process in psutil.process_iter() if process.name() == programName + '.exe'):
                process.kill()


def openExternalProgram(tokens):
    print(tokens)
    programLaunched = True
    for i, token in enumerate(tokens):
        if str(token[0]).lower() == 'steam':
            openSteam()
        elif str(token[0]).lower() == 'firefox':
            openFirefox()
        elif str(token[0]).lower() == 'vscode':
            openVSCode()
        elif str(token[0]).lower() == 'netflix':
            openNetflix()
        elif str(token[0]).lower() == 'spotify':
            openSpotify()
        elif str(token[0]).lower() == 'paint':
            openPaint3d()
        else:
            programLaunched = False
    if not programLaunched:
        print("I don't know what Im supposed to open")


def openVSCode():
    subprocess.Popen("C:\Program Files\Microsoft VS Code\Code.exe")


def openFirefox():
    subprocess.Popen("C:\Program Files\Mozilla Firefox\firefox.exe")


def openSteam():
    subprocess.Popen('C:\Program Files (x86)\Steam\Steam.exe')


def openPaint3d():
    subprocess.Popen(['explorer.exe', 'ms-paint:'])


def openNetflix():
    subprocess.Popen(['explorer.exe', 'netflix:'])


def openSpotify():
    subprocess.Popen(['explorer.exe', 'spotify:'])


commandsList = {
    'find': find,
    'play': play,
    'set': setOption,
    'exit': exitExternalProgram,
    'open': openExternalProgram,
    'start': openExternalProgram,
    'tell': tellOption
}