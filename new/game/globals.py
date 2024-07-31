#VALUE = CLASSE

games = {}
cups = {}

def  setGame(key, value):
    games[key]=value


def getGame(key):
    if key in games :
        return games[key]
    else :
        return None
    
def removeGame(key):
    del games[key]

def setCups(key, value):
    cups[key]=value

def getCup(key):
    if key in cups :
        return cups[key]
    else :
        return None
    
def removeCup(key):
    del cups[key]

