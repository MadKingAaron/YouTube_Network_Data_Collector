import random

def loadVideoList(videoListDoc:str)->tuple:
    list_file = open(videoListDoc, 'r')
    links = list_file.readlines()
    random.shuffle(links)
    return tuple(links)