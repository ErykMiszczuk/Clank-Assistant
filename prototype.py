import sys
import nltk
import getpass
import os

import re

import commands

stemmer = nltk.stem.PorterStemmer()

verbPattern = re.compile(r'VB.?')

username = getpass.getuser()
homeDir = os.path.expanduser('~\\')
homeMusicDir = homeDir + 'Music/'
homePicturesDir = homeDir + 'Pictures/'

def main():
    print('Hello ' + username)
    # commands.openPaint3d()
    # commands.openNetflix()
    # commands.openSpotify()
    # print('home directory ' + homeDir)
    # print(os.listdir(homeDir))
    # commands.playMusic(homeMusicDir)
    # commands.setWallpaper(homePicturesDir + 'vanessa_hudgens.jpg')
    # commands.setWallpaper(homePicturesDir + 'renfri_geralt.jpg')
    # commands.setWallpaper(homePicturesDir + 'panda_trueno.jpg')
    # commands.setWallpaper(homePicturesDir + 'caged.jpg')
    # print("Wallpaper set")
    
    for line in sys.stdin:
        tokens = nltk.word_tokenize(line)
        # tk = []
        # for token in tokens:
        #     tk.append(token.lower())
        # print(tk)
        tokens_pos_tags = nltk.pos_tag(tokens)
        # print(tokens_pos_tags)
        for token in tokens_pos_tags:
            # print(token)
            # if verbPattern.match(token[1]):
            comm = stemmer.stem(token[0])
            print(comm, token[1])
            # print(comm)
            # if comm in list(commands.commandsList.keys()):
            #     commands.commandsList[str(comm)](tokens_pos_tags)


    # commands.openYoutubeWithSearch('Discord')
    # commands.openYoutubeWithSearch('Max Covieri')
    # commands.openYoutubeWithSearch('One Time Full Time')

if __name__ == '__main__':
    main()

# Example commands
# I need to find some information about daybreak
# Play some music
# Play discord on youtube
# I want to listen dave rodgers all i want for christmas
# Tell me something about the witcher
# I want to play witcher
# Launch steam