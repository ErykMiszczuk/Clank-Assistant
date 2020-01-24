import sys
import nltk
import getpass
import os
import random

import re

import commands
import speech
import patterns

stemmer = nltk.stem.PorterStemmer()

username = getpass.getuser()
homeDir = os.path.expanduser('~\\')
homeMusicDir = homeDir + 'Music/'
homePicturesDir = homeDir + 'Pictures/'


def main():
    swears = 0
    print('Hello ' + username)
    
    for line in sys.stdin:
        if patterns.swearing.search(line):
            swears = swears + 1
            if swears > 3:
                print("I dont want to talk to you anymore")
                break
            print("Do not use this language")
        elif line == "Bye!\n":
            print("Goodbye!")
            break
        elif line == "/say\n":
            print("I'm listening...")
            text = speech.asrGoogle()
            if patterns.swearing.search(text):
                swears = swears + 1
                if swears > 3:
                    print("I dont want to talk to you anymore")
                    break
                print("Do not use this language")
            else:
                processText(text)
        elif line == "/commands\n":
            showHelp()
        else:
            processText(line)


def showHelp():
    print("/commands - print available commands and this help")
    print("/say - start listening for commands using microphone")
    print("")
    print("List of commands:")
    for command in commands.commandsList.keys():
        print(command)
    print("")
    print("Shall we continue?")


def processText(text):
    if text == None:
        print("Could you enter some txt, please?")
    elif patterns.question.match(text):
        commands.openGoogleWithSearch(text)
    else:
        commandFounded = False
        tokens = nltk.word_tokenize(text)
        tokens_pos_tags = nltk.pos_tag(tokens)
        print(tokens_pos_tags)
        for token in tokens_pos_tags:
            if patterns.verb.match(token[1]):
                print(patterns.verb.match(token[1]))
                commandFounded = True
                comm = stemmer.stem(token[0])
                if comm in list(commands.commandsList.keys()):
                    commands.commandsList[str(comm)](tokens_pos_tags)
        if commandFounded == True:
            print(random.choice(nextTaskResponses))
        elif commandFounded == False:
            print(f"{text} ^ I didn' know what to do. Try something else :)")
        else:
            print("I don't understand")


nextTaskResponses = [
    "Something else?",
    "Anything more?",
    "Are you want to do something else?",
    "Next task?",
    "Anything more to do?",
    "Something else to do?",
    "How can I help you?",
    "Can I assist you with this matter?",
    "What to do next?",
    "What are you wanted to do next?"
]


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

    # commands.playMusic(homeMusicDir)
    # commands.setWallpaper(homePicturesDir + 'vanessa_hudgens.jpg')
    # commands.setWallpaper(homePicturesDir + 'renfri_geralt.jpg')
    # commands.setWallpaper(homePicturesDir + 'panda_trueno.jpg')
    # commands.setWallpaper(homePicturesDir + 'caged.jpg')
    # print("Wallpaper set")