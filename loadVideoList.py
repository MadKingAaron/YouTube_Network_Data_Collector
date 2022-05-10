

def loadVideoList(videoListDoc:str)->tuple:
    list_file = open(videoListDoc, 'r')
    return tuple(list_file.readlines())