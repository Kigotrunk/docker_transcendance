from django.db import models
import threading, time
from random import randint
import asyncio
import time
import random
from math import *
from django.db import models
from django.db import models
from myaccount.models import Account
from django.conf import settings
import random 

class partie(models.Model):
    player1 = models.ForeignKey(Account, related_name='partie_as_user1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(Account, related_name='partie_as_user2', on_delete=models.CASCADE)
    score_player1 = models.IntegerField()       
    score_player2 = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player1} vs {self.player2}"

    class Meta:
        verbose_name = "Game"
        verbose_name_plural = "Games"
        ordering = ['-time']



class algorithm() : 
    
            #Pythagor my friend
            #xd = ball.xSpeed * ball.xSpeed
            #pd = ball.ySpeed * ball.ySpeed
            #truc = sqrt(xd + pd)
            #print(truc)
            #if ball.ySpeed < 0 :
            #    distanceMur = ball.y
            #elif ball.ySpeed > 0 :
            #    distanceMur = 600 - ball.y
            #bounce = ((distanceMur) / ball.ySpeed) * truc
            #angle = truc / sqrt(pd)
            #print(bounce)
            #print(" andgle ", angle)
            #if  ball.y + ball.ySpeed > 589 or ball.y + ball.ySpeed < 11 :
                #print("BOING INC", ball.y + ball.ySpeed)    
            #print("X", ball.x + ball.xSpeed)
            #self.actionTab = [self.loosingMove() ]

    def __init__(self, ball, pad, diff, playerPad) :
            self.diff = diff
            self.replace = 0
            self.playerPad = playerPad
            self.gotPlayerPad = False
            self.hitHeight = self.getLandingPlace(ball, pad)
            self.thd = threading.Thread(target=self.monitoringIaView, args=(ball, pad), daemon=True)
            self.thd.start()
            #self.previousShot = self.hitHeight
            self.rng = 7
            self.unlucky = -1
            self.dedge = False
            if self.diff == 4 :
                self.surv_score = 0
                self.thd_surv_score = threading.Thread(target=self.monitoring_score_survival, args=(), daemon=True)
                self.thd_surv_score.start()
            #self.thd.join()


    def getThread():
        return self.thd
        
    def getDiff(self) :
        return self.diff

    #def getPlayerPad(self, playerPad) :
        #if self.gotPlayerPad == False :
            #self.playerPad = playerPad
            #self.gotPlayerPad = True

    def getLandingPlace(self, ball, Pad):
        travelTime = (Pad.x - (ball.x + ball.rad)) / ball.xSpeed
        hitHeight = ball.y + ball.ySpeed * travelTime
        #if self.playerPad != None :
            #print(self.playerPad.y)
        if self.diff == 1:
            rF = random.uniform(0.90, 1.10)
            rF *= 600
            rF -= 600
            hitHeight +=rF
            self.rng = 7
            self.unlucky = randint(0, self.rng)
            hitHeight += self.chooseAction(hitHeight, self.playerPad)
        elif self.diff == 2:
            rF = random.uniform(0.91, 1.09)
            rF *= 600
            rF -= 600
            if hitHeight > 600 - ball.rad:
                hitHeight += rF
                hitHeight =  600 - ball.rad - (hitHeight - 600 - ball.rad)
            elif hitHeight < 0 + ball.rad:
                hitHeight += rF
                hitHeight = sqrt((hitHeight - ball.rad) * (hitHeight - ball.rad))
            self.rng = 15
            self.unlucky = randint(0, self.rng)
            hitHeight += self.chooseAction(hitHeight, self.playerPad)
        elif self.diff == 3 :
            rF = random.uniform(0.92, 1.08)
            rF *= 600
            rF -= 600
            self.rng = 22
            self.unlucky = randint(0, self.rng)
            if hitHeight > 600 - ball.rad:
                hitHeight += rF
                hitHeight =  600 - ball.rad - (hitHeight - 600 - ball.rad)
            elif hitHeight < 0 + ball.rad:
                hitHeight += rF
                hitHeight = sqrt((hitHeight - ball.rad) * (hitHeight - ball.rad))
            hitHeight += self.chooseAction(hitHeight, self.playerPad)
        elif self.diff == 4 :
            self.rng = 100
            self.unlucky = randint(0, self.rng)
            if hitHeight > 600 - ball.rad:
                hitHeight =  600 - ball.rad - (hitHeight - 600 - ball.rad)
            elif hitHeight < 0 + ball.rad:
                hitHeight = sqrt((hitHeight - ball.rad) * (hitHeight - ball.rad))
            hitHeight += self.chooseAction(hitHeight, self.playerPad)

            #print("POST RF", hitHeight)
        #else :
            #hitHeight = ball.x
        
            #changer pour Calculer les rebons a l'avance#
        #print("Pre SMARTSHOT : ",hitHeight)
        #hitHeight += self.smartShot(ball, Pad.algorithm.playerPad, Pad)
        #print("Post SMARTSHOT : ",hitHeight)
        return hitHeight
        #print(self.hitHeight)
        #self.ePointList.append(self.endpoint)
        #print("AAA")
    
    #def yoyoyo(self, ball, playerPad, rightPad)
    def monitoring_score_survival(self) :
        while True:
            self.surv_score += 1
            time.sleep(0.1)
            if self.dedge == True :
                return



    def monitoringIaView(self, ball, Pad) :
        while True :
            self.hitHeight = self.getLandingPlace(ball, Pad)
            time.sleep(0.6)
            if self.dedge == True :
                return
            
    def whereSmartShot(self, playerPad, rightPad, ball) :
        negativHH = (((ball.x - ball.rad) - playerPad.x) / ball.xSpeed) * ball.ySpeed
        #print( "negHH: ", negativHH)
        if negativHH < 0 or negativHH > 600 :
            test = (((playerPad.y / (600 - playerPad.height)) * playerPad.height) - 50 + self.hitHeight)
        else : 
            test = (((playerPad.y / (600 - playerPad.height)) * playerPad.height) - 50 * 0.5 + self.hitHeight)
        #print("test :", test)

    def smartShot(self, hitHeight, playerPad):
        #if hitHeight > 150 or hitHeight < 430 :
            #value = 20
        #elif hitHeight >
        if hitHeight < 115 and playerPad.y < 200 :
            return -20
        elif hitHeight < 115 and playerPad.y > 400 :
            return 0
        if hitHeight > 480 and playerPad.y > 400 :
            return 20
        elif hitHeight > 480 and playerPad.y < 200 :
            return 0
        if hitHeight > 115 and  hitHeight < 480 :
            if playerPad.y < 300 :
                if playerPad.y < 200 :
                    if playerPad.y < 105 :
                        return 24
                    return 16
                return 8
            elif playerPad.y > 300 :
                if playerPad.y > 200 :
                    if playerPad.y > 100 :
                        return -24
                    return - 16
                return -8
        return 0
            #elif hitHeight < 400 and self.playerPad.y > 200 :
            #print("ICI")
            #return 50
        #else :
            #return 0

        hhneg = 300
        if self.playerPad.y < 200 :
            hhneg = 499
        elif self.playerPad.y > 400 :
            hhneg = 101
        midPad = self.playerPad.y + 50
        #diff = midPad - ball.y
        reduc = (self.playerPad.height / 2) / ball.maxSpeed
        #Hhneg = 0
        TTneg = ((ball.x - ball.rad) - self.playerPad.x ) / ball.xSpeed
        ballYSpeedSet = (hhneg - ball.y) / TTneg 
        truc = (ballYSpeedSet * reduc) + ball.y - 50

        return truc
        prout = 0
        if playerPad.y < 205 :
            if rightPad.algorithm.hitHeight <= 125 :
                prout = - 40
            elif  rightPad.algorithm.hitHeight > 125 and rightPad.algorithm.hitHeight < 475 :
                prout = - 15
        elif playerPad.y > 395 : 
            if rightPad.algorithm.hitHeight >= 475 :
                prout = 40
            elif rightPad.algorithm.hitHeight < 475 and rightPad.algorithm.hitHeight > 125 :
                prout = 15

        return prout

       #     return (0)
        #elif playerPad.y > 395 :
        #    return (1)
        #else :
        #    return (2)
    def suvivalImprovement(self, algorithm, ball) :
        if ball.x > 800 :
            algorithm.data[3] += 1
        
    def assistanceLowerDificulty(self, leftScore, rightScore) :
        tmp = leftScore
        tmp2 = rightScore
        while leftScore == tmp :
            if rightScore > leftScore + 3 :
                #ASK IF PLAYER WANTS The game to be easier ???
                self.data[3] -= 3
                self.data[2] -= 2
                if self.data[2] < 9 :
                    self.data[5] = False


    def loosingMove(self) :
        tmp = randint(0,1)
        if tmp == 1 :
            return 20
        elif tmp == 0 :
            return -20
    
    def chooseAction(self, hitHeight, playerPad) :
        tmp = 0
        if self.canLoseRng() == True:
            tmp = self.loosingMove()
        elif self.canSmartShot() == True and self.playerPad != None and self.diff > 2:
            tmp = self.smartShot(hitHeight, playerPad)
            #self.hitHeight = self.loosingMove()
        #elif self.canSmartShot() == True:
            #return 2
        return tmp

    def canLoseRng(self) :
        if self.unlucky == self.rng - 1:
            return True
        else :
            return False


    def canSmartShot(self):
        if self.rng > 5 and self.rng <= 8:
            tmp = self.rng / 2
        elif self.rng > 8 :
            tmp = (self.rng / 2) + (self.rng / 3)
        else :
            tmp = 2
        i = 0
        while i <= tmp :
            if self.unlucky == i :
                return True
            i += 1
        return False


    
        
    def whereToGoAi(self, ball, Pad):
        #rng = 4
        travelTime = (Pad.x - ball.x) / ball.xSpeed
        Pad.algorithm.hitHeight = ball.y + ball.ySpeed * Pad.travelTime


    def getReadyReplace(self, ball, pad) :
        #if self.replace == 0 :
        if ball.xSpeed < 0 :
            if pad.y + 50 > 350 :
                pad.move(up = True)
                self.replace = 1
                #if self.replace != 0 :
                #self.hitHeight = pad.y + 50
                #pad.algorithm.hitHeight = 300
                #print("ICI")
                #self.hitHeight = 350
                #self.replace = 1
            elif pad.y + 50 < 250 :
                pad.move(up = False)
                self.replace = 2
                #if self.replace != 0 :
                #self.hitHeight = pad.y + 50
                    #pad.algorithm.hitHeight = 300
                    #print("ICI")
                    #self.hitHeight = 250
                    #self.replace = 2
        #self.hitHeight = 300

class   pad:

    speed = 4
    move_task = None

        
    def __init__(self, x, y, width, height, bal, diff, playerPad) :

        self.x = self.ogX = x
        self.y = self.ogY = y
        self.width = width
        self.height = height
        self.travelTime = 0
        self.direction = 0
        #self.algorithm = algorithm(bal, self, diff, playerPad)

    def sprite(self, win, color):

        pygame.draw.rect(win, color, (self.x, self.y, self.width, self.height))

    def move(self):
        if self.direction == 1:
            if self.y > 0 :
                self.y -= self.speed
        elif self.direction == -1:
            if self.y < 520 :
                self.y += self.speed

    """
    async def move_loop(self, direction):
        if (direction == 1):
            while self.y > 0:
                self.y -= 5
                print(self.y)
                await asyncio.sleep(0.01)
                
        elif (direction == -1):
            while self.y < 520:
                self.y += 5
                print(self.y)
                await asyncio.sleep(0.01)
    """

class   pad_ai:

    speed = 4
    move_task = None

    def __init__(self, x, y, width, height, bal, diff, playerPad) :

        self.x = self.ogX = x
        self.y = self.ogY = y
        self.width = width
        self.height = height
        self.travelTime = 0
        self.direction = 0
        self.algorithm = algorithm(bal, self, diff, playerPad)

    def sprite(self, win, color):

        pygame.draw.rect(win, color, (self.x, self.y, self.width, self.height))

    def move(self, up = True):
        if up :
            if self.y > 0 :
                self.y -= 4
        else :
            if self.y < 520 :
                self.y += 4

    def reset(self):

        self.x = self.ogX
        self.y = self.ogY

class   ball:

    maxSpeed = 5
    move_task = None

    def __init__(self, x, y, rad):

        self.x = self.ogX = x
        self.y = self.ogY = y
        self.rad = rad
        self.xSpeed = self.maxSpeed
        self.ySpeed = 0

    def sprite(self, win, color):

        pygame.draw.circle(win, color, (self.x, self.y), self.rad)

    def move(self):

        self.x += self.xSpeed
        self.y += self.ySpeed

    def reset(self):

        self.x = self.ogX
        self.y = self.ogY
        #self.xSpeed = self.maxSpeed
        if self.xSpeed > 5 :
            self.xSpeed = 5
        elif self.xSpeed < -5 :
            self.xSpeed = -5
        self.ySpeed = 0

    def getxSpeed(self):
        return self.xSpeed
